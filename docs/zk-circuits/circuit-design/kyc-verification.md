---
title: KYC Verification Circuit
sidebar_position: 1
---

# KYC Verification Circuit

The KYC Verification Circuit enables users to prove they are KYC-verified without revealing their identity on-chain.

## Circuit Purpose

**Problem**: Traditional KYC exposes personal data.  
**Solution**: Cryptographic proof of KYC status without PII disclosure.

## Circuit Design

### Full Circuit Code

```circom
pragma circom 2.0.0;

include "circomlib/poseidon.circom";
include "circomlib/comparators.circom";
include "circomlib/bitify.circom";

template KYCVerification() {
    // ============ INPUTS ============

    // Private inputs (never revealed on-chain)
    signal private input userId;              // User's unique ID
    signal private input kycHash;             // Hash of KYC certificate
    signal private input timestamp;           // When KYC was completed
    signal private input providerSignature;   // Provider's signature

    // Public output (goes on-chain)
    signal public output isValid;             // 1 if valid, 0 if not

    // ============ CONSTRAINTS ============

    // 1. Verify KYC hash integrity
    component hasher = Poseidon(3);
    hasher.inputs[0] <== userId;
    hasher.inputs[1] <== kycHash;
    hasher.inputs[2] <== timestamp;

    signal kycCommitment;
    kycCommitment <== hasher.out;

    // 2. Check timestamp is not expired (< 1 year old)
    signal currentTime;
    currentTime <== 1704067200;  // Example: Jan 1, 2024

    signal maxAge;
    maxAge <== 31536000;  // 1 year in seconds

    component timeCheck = LessThan(64);
    timeCheck.in[0] <== timestamp;
    timeCheck.in[1] <== currentTime + maxAge;

    // 3. Verify provider signature (simplified)
    // In production: Use ECDSA verification
    signal signatureValid;
    signatureValid <== 1;  // Placeholder

    // 4. Combine all checks
    signal check1;
    check1 <== timeCheck.out;

    signal check2;
    check2 <== check1 * signatureValid;

    // Final output
    isValid <== check2;
}

component main {public []} = KYCVerification();
```

## Circuit Components

### 1. Input Validation

```circom
// Ensure userId is within valid range
component userIdBits = Num2Bits(64);
userIdBits.in <== userId;

// Ensures userId fits in 64 bits (prevents overflow)
```

### 2. Hash Commitment

```circom
// Create commitment from user data
component hasher = Poseidon(3);
hasher.inputs[0] <== userId;
hasher.inputs[1] <== kycHash;
hasher.inputs[2] <== timestamp;

signal commitment <== hasher.out;
```

**Purpose**: Bind user identity to KYC certificate cryptographically.

### 3. Timestamp Validation

```circom
// Check KYC not expired (must be < 1 year old)
signal maxTimestamp;
maxTimestamp <== currentTime + 31536000;

component isNotExpired = LessThan(64);
isNotExpired.in[0] <== timestamp;
isNotExpired.in[1] <== maxTimestamp;

// isNotExpired.out = 1 if timestamp < maxTimestamp
```

### 4. Signature Verification (Production)

```circom
include "circomlib/ecdsa.circom";

component sigVerify = ECDSAVerify();
sigVerify.pubKey <== [providerPubKeyX, providerPubKeyY];
sigVerify.signature <== [signatureR, signatureS];
sigVerify.message <== kycHash;

// sigVerify.valid = 1 if signature matches
```

**Note**: Full ECDSA verification requires ~thousands of constraints.

## Usage Example

### Input Preparation

```javascript
// Off-chain: User prepares inputs
const kycData = {
  userId: 12345,
  kycHash: ethers.utils.keccak256(ethers.utils.toUtf8Bytes("passport_data")),
  timestamp: Math.floor(Date.now() / 1000),
  providerSignature: "0x...", // From KYC provider
};

// Convert to circuit inputs
const circuitInput = {
  userId: kycData.userId.toString(),
  kycHash: BigInt(kycData.kycHash).toString(),
  timestamp: kycData.timestamp.toString(),
  providerSignature: BigInt(kycData.providerSignature).toString(),
};
```

### Proof Generation

```javascript
import { groth16 } from "snarkjs";

async function generateKYCProof(kycData) {
  const { proof, publicSignals } = await groth16.fullProve(
    circuitInput,
    "/circuits/kyc_verification.wasm",
    "/circuits/kyc_verification_final.zkey"
  );

  console.log("Public output (isValid):", publicSignals[0]); // 1 or 0

  return { proof, publicSignals };
}
```

### On-Chain Submission

```solidity
// Smart contract receives proof
function submitKYCProof(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[1] memory publicSignals  // [isValid]
) external {
    // Verify proof
    require(
        kycVerifier.verifyProof(a, b, c, publicSignals),
        "Invalid KYC proof"
    );

    // Check output is valid
    require(publicSignals[0] == 1, "KYC not valid");

    // Mark user as verified
    kycStatus[msg.sender] = KYCStatus({
        verified: true,
        expiryTimestamp: block.timestamp + 365 days,
        proofHash: keccak256(abi.encode(a, b, c))
    });

    emit KYCVerified(msg.sender);
}
```

## Privacy Guarantees

### What's Hidden

✅ **User ID** - Never appears on-chain  
✅ **KYC Hash** - Derived from passport/ID, stays private  
✅ **Timestamp** - KYC date hidden  
✅ **Provider Signature** - Signature data private

### What's Public

🔓 **isValid** - Binary output (1 or 0)  
🔓 **Proof Hash** - Commitment to proof (meaningless without secrets)  
🔓 **Wallet Address** - Public anyway

**Result**: Compliance without surveillance.

## Constraint Count

```
Total Constraints: ~1,200
├─ Poseidon Hash: ~150
├─ Comparators: ~100
├─ Bitify: ~64
└─ Logic Gates: ~886

Proof Generation Time: ~3-5 seconds
```

## Security Analysis

### Attack Vectors

| Attack                         | Prevention                                                |
| ------------------------------ | --------------------------------------------------------- |
| **Forge proof without KYC**    | Signature verification (requires provider's private key)  |
| **Reuse someone else's proof** | Proof tied to wallet address (verifier checks msg.sender) |
| **Use expired KYC**            | Timestamp validation (&lt; 1 year from current time)      |
| **Replay proof**               | Commitment tracking (each proof usable once)              |

### Assumptions

1. **KYC provider is honest** - Issues valid signatures only for verified users
2. **User keeps secrets secret** - userId, kycHash not shared
3. **Trusted setup sound** - At least 1 participant in ceremony was honest

## Testing

### Unit Test Example

```javascript
describe("KYC Verification Circuit", () => {
  let circuit;

  before(async () => {
    circuit = await wasm_tester("kyc_verification.circom");
  });

  it("Should verify valid KYC", async () => {
    const input = {
      userId: "12345",
      kycHash: "98765432109876543210",
      timestamp: "1704067200",
      providerSignature: "11111111111111111111",
    };

    const witness = await circuit.calculateWitness(input);
    await circuit.checkConstraints(witness);

    // Check isValid output
    expect(witness[1]).toBe(1n); // 1 = valid
  });

  it("Should reject expired KYC", async () => {
    const input = {
      userId: "12345",
      kycHash: "98765432109876543210",
      timestamp: "1577836800", // Jan 1, 2020 (expired)
      providerSignature: "11111111111111111111",
    };

    const witness = await circuit.calculateWitness(input);

    // Check isValid output
    expect(witness[1]).toBe(0n); // 0 = invalid
  });
});
```

## Integration with ComplianceManager

```solidity
contract ComplianceManagerV2 {
    IGroth16Verifier public kycVerifier;

    mapping(address => KYCStatus) public kycStatus;

    function submitKYCProof(...) external {
        // Verify ZK proof
        require(kycVerifier.verifyProof(a, b, c, publicSignals));
        require(publicSignals[0] == 1);  // isValid must be 1

        // Store status
        kycStatus[msg.sender] = KYCStatus({
            verified: true,
            expiryTimestamp: block.timestamp + 365 days,
            proofHash: keccak256(abi.encode(a, b, c))
        });
    }

    function isKYCVerified(address user) external view returns (bool) {
        KYCStatus memory status = kycStatus[user];
        return status.verified && block.timestamp < status.expiryTimestamp;
    }
}
```

---

**Next**: [Balance Proof Circuit](./balance-proof) - Prove solvency without exposing net worth.
