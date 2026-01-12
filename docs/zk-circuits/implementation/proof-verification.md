---
title: Proof Verification
sidebar_position: 3
---

# Proof Verification

On-chain proof verification validates Zero-Knowledge proofs submitted by users, ensuring cryptographic soundness before executing sensitive operations.

## Verification Flow

```
User generates proof (off-chain)
        ↓
Submit to smart contract
        ↓
Contract calls Groth16Verifier
        ↓
Elliptic curve pairing check
        ↓
Returns true/false
        ↓
Execute action if valid
```

## Solidity Verifier

### Auto-Generated Contract

Exported from SnarkJS:

```bash
snarkjs zkey export solidityverifier \
    keys/kyc_verification_final.zkey \
    contracts/KYCVerifier.sol
```

### Verifier Structure

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract Groth16Verifier {
    using Pairing for *;

    struct VerifyingKey {
        Pairing.G1Point alfa1;
        Pairing.G2Point beta2;
        Pairing.G2Point gamma2;
        Pairing.G2Point delta2;
        Pairing.G1Point[] IC;
    }

    function verificationKey() internal pure returns (VerifyingKey memory vk) {
        // Hard-coded verification key from trusted setup
        vk.alfa1 = Pairing.G1Point(...);
        vk.beta2 = Pairing.G2Point(...);
        // ... more parameters
    }

    function verify(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[1] memory input
    ) public view returns (bool r) {
        Proof memory proof;
        proof.A = Pairing.G1Point(a[0], a[1]);
        proof.B = Pairing.G2Point([b[0][0], b[0][1]], [b[1][0], b[1][1]]);
        proof.C = Pairing.G1Point(c[0], c[1]);

        VerifyingKey memory vk = verificationKey();

        // Pairing check
        return pairing(
            proof.A, proof.B,
            vk.alpha, vk.beta,
            vk.gamma, proof.C,
            vk.delta
        );
    }
}
```

### Pairing Precompile

Uses bn256 pairing at address `0x08`:

```solidity
function pairing(...) internal view returns (bool) {
    uint256 inputSize = 24 * 192;  // 6 points × 32 bytes × 6 coords

    bool success;
    uint256 result;

    assembly {
        success := staticcall(
            gas(),
            8,           // Precompiled contract address
            input,
            inputSize,
            result,
            0x20
        )
    }

    return success && (result != 0);
}
```

**Gas Cost**: ~280k-320k per verification

## Integration Example

### ComplianceManager Integration

```solidity
contract ComplianceManagerV2 {
    IGroth16Verifier public kycVerifier;

    mapping(address => KYCStatus) public kycStatus;
    mapping(bytes32 => bool) public usedProofs;

    constructor(address _kycVerifier) {
        kycVerifier = IGroth16Verifier(_kycVerifier);
    }

    function submitKYCProof(
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[1] memory publicSignals  // [isValid]
    ) external {
        // 1. Verify proof hasn't been used
        bytes32 proofHash = keccak256(abi.encode(a, b, c));
        require(!usedProofs[proofHash], "Proof already used");

        // 2. Verify ZK proof
        bool proofValid = kycVerifier.verify(a, b, c, publicSignals);
        require(proofValid, "Invalid ZK proof");

        // 3. Check output signal
        require(publicSignals[0] == 1, "KYC not valid");

        // 4. Store KYC status
        kycStatus[msg.sender] = KYCStatus({
            verified: true,
            expiryTimestamp: block.timestamp + 365 days,
            proofHash: proofHash
        });

        // 5. Mark proof as used
        usedProofs[proofHash] = true;

        emit KYCVerified(msg.sender, block.timestamp);
    }

    function isKYCVerified(address user) external view returns (bool) {
        KYCStatus memory status = kycStatus[user];
        return status.verified && block.timestamp < status.expiryTimestamp;
    }
}
```

## Frontend Integration

### Submit Proof from React

```typescript
import { ethers } from "ethers";

async function submitKYCProof(proof, publicSignals) {
  const complianceContract = new ethers.Contract(
    COMPLIANCE_MANAGER_ADDRESS,
    COMPLIANCE_ABI,
    signer
  );

  try {
    // Format proof for Solidity
    const tx = await complianceContract.submitKYCProof(
      [proof.pi_a[0], proof.pi_a[1]],
      [
        [proof.pi_b[0][1], proof.pi_b[0][0]],
        [proof.pi_b[1][1], proof.pi_b[1][0]],
      ],
      [proof.pi_c[0], proof.pi_c[1]],
      publicSignals
    );

    console.log("Transaction sent:", tx.hash);

    // Wait for confirmation
    const receipt = await tx.wait();
    console.log("Proof verified on-chain!", receipt);

    return receipt;
  } catch (error) {
    if (error.message.includes("Invalid ZK proof")) {
      throw new Error("Proof verification failed");
    } else if (error.message.includes("Proof already used")) {
      throw new Error("This proof has already been submitted");
    } else {
      throw error;
    }
  }
}
```

## Off-Chain Verification (Testing)

### Verify Before Submitting

```javascript
import { groth16 } from "snarkjs";

async function verifyProofOffChain(proof, publicSignals) {
  // Load verification key
  const vKey = await fetch("/circuits/kyc_verification_vkey.json").then((r) =>
    r.json()
  );

  // Verify proof
  const isValid = await groth16.verify(vKey, publicSignals, proof);

  if (!isValid) {
    throw new Error("Proof is invalid - won't submit to chain");
  }

  console.log("✅ Proof valid off-chain");
  return true;
}

// Usage
const { proof, publicSignals } = await generateKYCProof(inputs);

// Verify locally first (saves gas if invalid)
await verifyProofOffChain(proof, publicSignals);

// Submit to blockchain
await submitKYCProof(proof, publicSignals);
```

## Gas Optimization

### Batch Verification

```solidity
// Verify multiple proofs in one transaction
function batchVerifyKYC(
    uint256[2][] memory a,
    uint256[2][2][] memory b,
    uint256[2][] memory c,
    uint256[1][] memory inputs
) external {
    require(a.length == b.length, "Length mismatch");

    for (uint i = 0; i < a.length; i++) {
        bool valid = kycVerifier.verify(a[i], b[i], c[i], inputs[i]);
        require(valid, "Invalid proof in batch");

        // Process KYC...
    }

    // Saves ~21k gas per proof vs separate transactions
}
```

### Proof Caching

```solidity
// Cache verification results
mapping(bytes32 => bool) public verifiedProofs;

function verifyWithCache(...) external {
    bytes32 proofHash = keccak256(abi.encode(a, b, c, input));

    // Check cache first
    if (verifiedProofs[proofHash]) {
        return true;  // Already verified
    }

    // Verify ZK proof
    bool valid = kycVerifier.verify(a, b, c, input);

    if (valid) {
        verifiedProofs[proofHash] = true;
    }

    return valid;
}
```

## Security Considerations

### Replay Attack Prevention

```solidity
// Prevent proof reuse
mapping(bytes32 => bool) public usedProofHashes;

modifier proofNotUsed(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c
) {
    bytes32 proofHash = keccak256(abi.encode(a, b, c));
    require(!usedProofHashes[proofHash], "Proof already used");
    _;
    usedProofHashes[proofHash] = true;
}
```

### Input Validation

```solidity
function submitKYCProof(...) external {
    // Verify public signals are in valid range
    require(publicSignals[0] <= 1, "Invalid isValid value");

    // Verify proof
    require(kycVerifier.verify(a, b, c, publicSignals));

    // Process...
}
```

## Testing Verification

### Hardhat Test

```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");
const { groth16 } = require("snarkjs");

describe("KYC Verification", function () {
  let verifier, complianceManager;

  before(async function () {
    // Deploy verifier
    const Verifier = await ethers.getContractFactory("Groth16Verifier");
    verifier = await Verifier.deploy();

    // Deploy compliance manager
    const Compliance = await ethers.getContractFactory("ComplianceManagerV2");
    complianceManager = await Compliance.deploy(verifier.address);
  });

  it("Should verify valid KYC proof", async function () {
    // Generate proof
    const inputs = {
      userId: "12345",
      kycHash: "98765",
      timestamp: "1704067200",
      providerSignature: "11111",
    };

    const { proof, publicSignals } = await groth16.fullProve(
      inputs,
      "circuits/kyc_verification.wasm",
      "circuits/kyc_verification_final.zkey"
    );

    // Submit to contract
    await complianceManager.submitKYCProof(
      [proof.pi_a[0], proof.pi_a[1]],
      [
        [proof.pi_b[0][1], proof.pi_b[0][0]],
        [proof.pi_b[1][1], proof.pi_b[1][0]],
      ],
      [proof.pi_c[0], proof.pi_c[1]],
      publicSignals
    );

    // Check KYC status
    const [signer] = await ethers.getSigners();
    const isVerified = await complianceManager.isKYCVerified(signer.address);
    expect(isVerified).to.be.true;
  });
});
```

## Performance Metrics

| Operation              | Gas Cost | Time  |
| ---------------------- | -------- | ----- |
| **Proof Verification** | 280-320k | ~5ms  |
| **KYC Submission**     | ~350k    | ~10ms |
| **Batch (10 proofs)**  | ~3M      | ~50ms |

**Optimization**: Use L2 (Mantle) for 10-100x cheaper verification.

---

**Congratulations!** You've completed the **ZK Circuits** section.

**Next Steps**:

- [DeFi Strategies](../../defi-strategies/overview) - Explore yield generation
- [Core Flow](../../core-flow/user-flow/wallet-connection) - User interaction flows
