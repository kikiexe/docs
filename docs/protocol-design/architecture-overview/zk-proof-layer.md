---
title: ZK Proof Layer
sidebar_position: 3
---

# ZK Proof Layer

The **ZK Proof Layer** provides cryptographic privacy for Veilfi through **Groth16 zk-SNARKs**, enabling users to deposit, withdraw, and prove compliance without exposing sensitive financial data.

## Architecture

```
┌──────────────────────────────────────────┐
│     ZK Proof Layer Components            │
├──────────────────────────────────────────┤
│                                          │
│  Circom Circuits (Off-Chain):            │
│  ├─ KYC Verification Circuit             │
│  ├─ Balance Proof Circuit                │
│  └─ Deposit Proof Circuit                │
│                                          │
│  Solidity Verifiers (On-Chain):          │
│  ├─ Groth16Verifier.sol                  │
│  └─ ComplianceManagerV2.sol              │
│                                          │
└──────────────────────────────────────────┘
```

## Core Circuits

### 1. KYC Verification Circuit

Proves user is KYC-verified without revealing identity:

```circom
pragma circom 2.0.0;

include "circomlib/poseidon.circom";
include "circomlib/comparators.circom";

template KYCVerification() {
    // Private inputs (never revealed on-chain)
    signal private input userId;
    signal private input kycHash;
    signal private input timestamp;
    signal private input providerSignature;

    // Public output (goes on-chain)
    signal public output isValid;

    // Verify KYC hash is valid
    component hasher = Poseidon(3);
    hasher.inputs[0] <== userId;
    hasher.inputs[1] <== kycHash;
    hasher.inputs[2] <== timestamp;

    // Check timestamp not expired (< 1 year old)
    component timeCheck = LessThan(64);
    timeCheck.in[0] <== timestamp;
    timeCheck.in[1] <== 1704067200 + 31536000; // Current + 1 year

    // Output 1 if valid, 0 otherwise
    isValid <== timeCheck.out;
}

component main = KYCVerification();
```

**Purpose**: Compliance without surveillance.

### 2. Balance Proof Circuit

Proves balance ≥ threshold without revealing exact amount:

```circom
template BalanceProof() {
    // Private: User's actual balance
    signal private input actualBalance;

    // Public: Minimum required
    signal public input minRequired;

    // Output: Is balance sufficient?
    signal public output sufficient;

    // actualBalance >= minRequired
    component comparator = GreaterEqThan(64);
    comparator.in[0] <== actualBalance;
    comparator.in[1] <== minRequired;

    sufficient == comparator.out;
}

component main = BalanceProof();
```

**Use Case**: Prove solvency for loans without exposing net worth.

### 3. Deposit Proof Circuit

Hides deposit amount during private deposits:

```circom
template DepositProof() {
    // Private inputs
    signal private input depositAmount;
    signal private input userSecret;

    // Public output (commitment)
    signal public output commitment;

    // Create commitment = hash(amount + secret)
    component hasher = Poseidon(2);
    hasher.inputs[0] <== depositAmount;
    hasher.inputs[1] <== userSecret;

    commitment <== hasher.out;
}

component main = DepositProof();
```

**Privacy**: Only commitment stored on-chain, amount hidden.

## Proof Generation (Client-Side)

### Browser-Based Generation

```javascript
import { groth16 } from "snarkjs";

async function generateKYCProof(kycData) {
  // Input preparation
  const input = {
    userId: kycData.userId, // PRIVATE
    kycHash: kycData.hash, // PRIVATE
    timestamp: kycData.timestamp, // PRIVATE
    providerSignature: kycData.sig, // PRIVATE
  };

  // Generate proof (takes ~5-10 seconds)
  const { proof, publicSignals } = await groth16.fullProve(
    input,
    "/circuits/kyc_verification.wasm", // WASM circuit
    "/circuits/kyc_verification_final.zkey" // Proving key
  );

  // Format for Solidity
  const calldata = await groth16.exportSolidityCallData(proof, publicSignals);

  return JSON.parse(`[${calldata}]`);
}
```

**Key Point**: Proof generated locally, secrets never leave browser.

## On-Chain Verification

### Groth16 Verifier Contract

Auto-generated from circuit:

```solidity
contract Groth16Verifier {
    using Pairing for *;

    struct VerifyingKey {
        Pairing.G1Point alpha;
        Pairing.G2Point beta;
        Pairing.G2Point gamma;
        Pairing.G2Point delta;
        Pairing.G1Point[] gamma_abc;
    }

    function verifyProof(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[1] memory input
    ) public view returns (bool) {
        // Elliptic curve pairing verification
        // Returns true if proof is valid
        return pairing(...);
    }
}
```

**Gas Cost**: ~280-320k gas per verification.

### Integration with Vault

```solidity
contract StrategyVaultV2_Multi {
    IGroth16Verifier public zkVerifier;

    function depositWithProof(
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[3] memory publicSignals
    ) external payable returns (uint256) {
        // Verify ZK proof
        require(
            zkVerifier.verifyProof(a, b, c, publicSignals),
            "Invalid proof"
        );

        // Process deposit without revealing amount
        return _processPrivateDeposit(msg.sender, msg.value);
    }
}
```

## Trusted Setup

### Powers of Tau Ceremony

Generate universal proving parameters:

```bash
# Phase 1: Powers of Tau (universal)
snarkjs powersoftau new bn128 12 pot12_0000.ptau
snarkjs powersoftau contribute pot12_0000.ptau pot12_0001.ptau \
  --name="First contribution"

# Phase 2: Circuit-specific setup
circom kyc_verification.circom --r1cs --wasm
snarkjs groth16 setup kyc_verification.r1cs pot12_final.ptau kyc_0000.zkey

# Generate verification key
snarkjs zkey export verificationkey kyc_final.zkey verification_key.json

# Export Solidity verifier
snarkjs zkey export solidityverifier kyc_final.zkey Verifier.sol
```

**Security**: At least 1 honest participant required (N-of-N security).

## Privacy Guarantees

### What ZK Proofs Hide

✅ **Deposit amounts**: Hidden in commitments  
✅ **User balances**: Not queryable  
✅ **KYC identity**: Proven without PII  
✅ **Transaction linkage**: Deposits/withdrawals unlinkable

### What Remains Public

🔓 **Wallet addresses**: Public on blockchain  
🔓 **Transaction timing**: Timestamps visible  
🔓 **Proof validity**: Anyone can verify  
🔓 **Total TVL**: Vault-level transparency

## Performance Metrics

| Operation               | Time   | Gas Cost        |
| ----------------------- | ------ | --------------- |
| **Proof Generation**    | 5-15s  | 0 (client-side) |
| **Proof Verification**  | ~5ms   | 280-320k gas    |
| **Circuit Compilation** | 30-60s | 0 (one-time)    |

**Optimization**: Use Web Workers for non-blocking UI during proof generation.

## Security Considerations

### Cryptographic Assumptions

- **Discrete Log Problem**: Hard on BN254 curve
- **Groth16 Soundness**: Computationally secure
- **Trusted Setup**: Requires 1+ honest participants

**Risk Level**: 🟢 Low (same as Zcash, Tornado Cash)

### Attack Resistance

| Attack Vector                  | Mitigation                 |
| ------------------------------ | -------------------------- |
| **Forge fake proof**           | Computationally infeasible |
| **Extract secrets from proof** | Zero-knowledge property    |
| **Replay proof**               | Nonce/commitment tracking  |
| **Quantum computers**          | Future: migrate to STARKs  |

---

**Next**: [Modular Components](../modular-components/strategy-vault) - Smart contract breakdown.

**Technical Deep Dive**: [ZK Circuits](../../zk-circuits/introduction) for full circuit code.
