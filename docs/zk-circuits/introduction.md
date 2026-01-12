---
title: Introduction to ZK Circuits
sidebar_position: 1
---

# Introduction to ZK Circuits

ZK Circuits are the cryptographic foundation of Veilfi's privacy layer, enabling users to prove statements about their data without revealing the data itself.

## What are ZK Circuits?

**ZK Circuits** are programmable cryptographic proofs written in specialized languages like **Circom**. They define the logic for Zero-Knowledge proof generation and verification.

### Analogy: Circuit as a Lock

```
Traditional Program:
Input → Compute → Output (all visible)

ZK Circuit:
Secret Input → Compute → Proof (output visible, input hidden)
              ↓
         Verifier checks: Proof valid? ✅/❌
         Verifier CANNOT see: Secret input
```

## Veilfi's ZK Circuits

### 1. KYC Verification Circuit

**Purpose**: Prove user is KYC-verified without revealing identity.

**Inputs**:

- 🔒 Private: `userId`, `kycHash`, `timestamp`, `signature`
- 🔓 Public: `isValid` (1 or 0)

**Logic**: Verify cryptographic signature matches KYC certificate.

**Use Case**: Institutional compliance.

### 2. Balance Proof Circuit

**Purpose**: Prove balance ≥ threshold without revealing exact amount.

**Inputs**:

- 🔒 Private: `actualBalance`
- 🔓 Public: `minRequired`, `sufficient` (1/0)

**Logic**: Check `actualBalance >= minRequired`.

**Use Case**: Lending applications (prove solvency).

### 3. Deposit Proof Circuit (Future)

**Purpose**: Hide deposit amount during private deposits.

**Inputs**:

- 🔒 Private: `depositAmount`, `userSecret`
- 🔓 Public: `commitment`

**Logic**: Generate commitment = `hash(amount + secret)`.

**Use Case**: Financial privacy.

## Circuit Workflow

```
┌──────────────────────────────────────────┐
│  1. Circuit Design (Circom)              │
│     Write .circom file                   │
└──────────────┬───────────────────────────┘
               ↓
┌──────────────────────────────────────────┐
│  2. Compilation                          │
│     circom → R1CS + WASM + Witness       │
└──────────────┬───────────────────────────┘
               ↓
┌──────────────────────────────────────────┐
│  3. Trusted Setup                        │
│     Generate proving/verification keys   │
└──────────────┬───────────────────────────┘
               ↓
┌──────────────────────────────────────────┐
│  4. Proof Generation (User's Browser)    │
│     Input → WASM → Proof (~10 seconds)   │
└──────────────┬───────────────────────────┘
               ↓
┌──────────────────────────────────────────┐
│  5. Verification (Smart Contract)        │
│     Proof → Groth16Verifier → ✅/❌      │
└──────────────────────────────────────────┘
```

## Technology Stack

### Circom Language

Domain-specific language for ZK circuits:

```circom
pragma circom 2.0.0;

template Example() {
    signal input a;      // Private input
    signal input b;      // Private input
    signal output c;     // Public output

    c <== a * b;         // Constraint: c must equal a*b
}

component main = Example();
```

**Features**:

- Declarative syntax
- Constraint-based (R1CS)
- Compile to WASM + witness generator

### SnarkJS

JavaScript/TypeScript library for proof generation:

```javascript
import { groth16 } from "snarkjs";

// Generate proof
const { proof, publicSignals } = await groth16.fullProve(
  input,
  "circuit.wasm",
  "circuit_final.zkey"
);

// Verify proof (off-chain)
const verified = await groth16.verify(verificationKey, publicSignals, proof);
```

### Groth16 Proof System

**Properties**:

- Proof size: ~200 bytes (constant)
- Verification: ~5ms (~300k gas on-chain)
- Setup: Trusted ceremony required

**Trade-off**: Small proofs + fast verification, but needs trusted setup.

## Circuit Components (Building Blocks)

Veilfi uses `circomlib` for common operations:

### Hash Functions

```circom
include "circomlib/poseidon.circom";

component hasher = Poseidon(2);
hasher.inputs[0] <== value1;
hasher.inputs[1] <== value2;
output <== hasher.out;
```

### Comparators

```circom
include "circomlib/comparators.circom";

component gt = GreaterThan(64);
gt.in[0] <== a;
gt.in[1] <== b;
// gt.out = 1 if a > b, else 0
```

### Signature Verification

```circom
include "circomlib/ecdsa.circom";

component sigCheck = ECDSAVerify();
sigCheck.signature <== providedSignature;
sigCheck.message <== messageHash;
// sigCheck.valid = 1 if signature valid
```

## Security

### Soundness

**Guarantee**: If statement is false, attacker cannot generate valid proof (except with negligible probability).

**Example**: Cannot prove `balance ≥ 100 ETH` if actual balance is 50 ETH.

### Zero-Knowledge

**Guarantee**: Proof reveals nothing beyond the statement's truth.

**Example**: Proof of "balance ≥ 50 ETH" doesn't reveal if balance is 50, 100, or 1000 ETH.

### Completeness

**Guarantee**: If statement is true, honest user can always generate valid proof.

**Example**: If user has 100 ETH, they CAN prove "balance ≥ 50 ETH".

## Performance Considerations

### Proof Generation Time

| Circuit Complexity   | Constraints | Generation Time |
| -------------------- | ----------- | --------------- |
| **KYC Verification** | ~1,000      | ~3-5 seconds    |
| **Balance Proof**    | ~500        | ~2-3 seconds    |
| **Complex Logic**    | ~10,000     | ~15-30 seconds  |

**Optimization**: Use Web Workers to avoid blocking UI.

### Gas Costs

| Operation                | Gas Cost       |
| ------------------------ | -------------- |
| **Proof Verification**   | 280-320k gas   |
| **Standard Transaction** | ~21k gas       |
| **Overhead**             | ~13x expensive |

**Trade-off**: Privacy costs extra gas, but worth it for sensitive operations.

## Development Tools

### Circom Compiler

```bash
# Install
npm install -g circom

# Compile circuit
circom circuit.circom --r1cs --wasm --sym

# Outputs:
# - circuit.r1cs (constraint system)
# - circuit.wasm (witness generator)
# - circuit.sym (debug symbols)
```

### SnarkJS CLI

```bash
# Install
npm install -g snarkjs

# Setup trusted ceremony
snarkjs groth16 setup circuit.r1cs powersOfTau.ptau circuit_0000.zkey

# Generate verification key
snarkjs zkey export verificationkey circuit_final.zkey vkey.json

# Export Solidity verifier
snarkjs zkey export solidityverifier circuit_final.zkey Verifier.sol
```

## Circuit Design Best Practices

### 1. Minimize Constraints

```circom
// ❌ Bad: Unnecessary constraints
signal a, b, c, d;
c <== a + b;
d <== c * 2;  // Extra constraint

// ✅ Good: Direct computation
signal a, b, d;
d <== (a + b) * 2;  // Single constraint
```

**Impact**: Fewer constraints = faster proof generation.

### 2. Use Efficient Hash Functions

```circom
// ❌ Avoid: SHA-256 (expensive in ZK)
// Requires ~25,000 constraints

// ✅ Use: Poseidon (ZK-friendly)
// Requires ~150 constraints
include "circomlib/poseidon.circom";
```

### 3. Proper Input Validation

```circom
// Ensure inputs are within valid range
component rangeCheck = Num2Bits(64);
rangeCheck.in <== userInput;
// Forces userInput to be 64-bit number
```

## Testing Circuits

### Unit Testing

```javascript
const wasm_tester = require("circom_tester").wasm;

describe("KYC Circuit", () => {
  it("Should verify valid KYC", async () => {
    const circuit = await wasm_tester("kyc_verification.circom");

    const input = {
      userId: 12345,
      kycHash: "0x...",
      timestamp: 1704067200,
    };

    const witness = await circuit.calculateWitness(input);
    await circuit.checkConstraints(witness);

    // Check output is valid (1)
    expect(witness[1]).toBe(1);
  });
});
```

## Audit Considerations

ZK circuits require specialized audits:

- **Logic errors**: Incorrect constraints allow invalid proofs
- **Under-constrained**: Missing constraints enable attacks
- **Trusted setup**: Ensure ceremony participants are honest

**Veilfi Status**: Circuits audited by [Auditor Name] (planned).

---

**Next Steps**:

- [KYC Verification Circuit](./circuit-design/kyc-verification) - Detailed circuit design
- [Circom Setup](./implementation/circom-setup) - Development environment setup
