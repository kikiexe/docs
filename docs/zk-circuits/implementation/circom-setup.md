---
title: Circom Setup
sidebar_position: 1
---

# Circom Setup

Complete guide to setting up the Circom development environment for building and testing ZK circuits.

## Prerequisites

### Required Software

```bash
# Node.js (v16+)
node --version  # v16.0.0 or higher

# npm or yarn
npm --version

# Rust (for circom compiler)
rustc --version
```

### Installation

#### 1. Install Circom Compiler

```bash
# Clone circom repository
git clone https://github.com/iden3/circom.git
cd circom

# Build from source (requires Rust)
cargo build --release
cargo install --path circom

# Verify installation
circom --help
```

**Alternative (Pre-built Binary)**:

```bash
# Download from releases
wget https://github.com/iden3/circom/releases/download/v2.1.6/circom-linux-amd64
chmod +x circom-linux-amd64
sudo mv circom-linux-amd64 /usr/local/bin/circom
```

#### 2. Install SnarkJS

```bash
npm install -g snarkjs

# Verify
snarkjs --help
```

#### 3. Install Development Dependencies

```bash
# In your project directory
npm init -y

npm install --save-dev \
    circomlib \
    circom_tester \
    chai \
    mocha
```

## Project Structure

```
veilfi-circuits/
├── circuits/
│   ├── kyc_verification.circom
│   ├── balance_proof.circom
│   └── lib/
│       └── custom_templates.circom
│
├── build/
│   ├── kyc_verification.r1cs
│   ├── kyc_verification.wasm
│   └── kyc_verification.sym
│
├── keys/
│   ├── powersOfTau28_hez_final.ptau
│   ├── kyc_verification_0000.zkey
│   └── kyc_verification_final.zkey
│
├── contracts/
│   └── KYCVerifier.sol
│
├── test/
│   ├── kyc_verification.test.js
│   └── balance_proof.test.js
│
└── scripts/
    ├── compile.sh
    ├── setup.sh
    └── generate_proof.js
```

## Circuit Compilation

### Compile Command

```bash
# Basic compilation
circom circuits/kyc_verification.circom \
    --r1cs \
    --wasm \
    --sym \
    -o build/

# Outputs:
# - build/kyc_verification.r1cs  (constraint system)
# - build/kyc_verification_js/kyc_verification.wasm  (witness generator)
# - build/kyc_verification.sym (debug symbols)
```

### Compilation Script

Create `scripts/compile.sh`:

```bash
#!/bin/bash

CIRCUIT_NAME=$1

echo "Compiling $CIRCUIT_NAME..."

circom circuits/${CIRCUIT_NAME}.circom \
    --r1cs \
    --wasm \
    --sym \
    -o build/

echo "✅ Compilation complete!"

# Print constraint count
snarkjs r1cs info build/${CIRCUIT_NAME}.r1cs
```

**Usage**:

```bash
chmod +x scripts/compile.sh
./scripts/compile.sh kyc_verification
```

## Trusted Setup

### Phase 1: Powers of Tau (Universal)

```bash
# Download pre-computed Powers of Tau
wget https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_21.ptau \
    -O keys/powersOfTau28_hez_final.ptau

# OR generate your own (time-consuming)
snarkjs powersoftau new bn128 12 keys/pot12_0000.ptau -v
snarkjs powersoftau contribute keys/pot12_0000.ptau keys/pot12_0001.ptau \
    --name="First contribution" -v
snarkjs powersoftau beacon keys/pot12_0001.ptau keys/pot12_beacon.ptau \
    0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f 10 -n="Final Beacon"
snarkjs powersoftau prepare phase2 keys/pot12_beacon.ptau keys/powersOfTau28_hez_final.ptau -v
```

### Phase 2: Circuit-Specific Setup

```bash
CIRCUIT=kyc_verification

# Generate initial zkey
snarkjs groth16 setup \
    build/${CIRCUIT}.r1cs \
    keys/powersOfTau28_hez_final.ptau \
    keys/${CIRCUIT}_0000.zkey

# Contribute to ceremony
snarkjs zkey contribute \
    keys/${CIRCUIT}_0000.zkey \
    keys/${CIRCUIT}_0001.zkey \
    --name="Contribution 1" \
    -v

# Apply random beacon
snarkjs zkey beacon \
    keys/${CIRCUIT}_0001.zkey \
    keys/${CIRCUIT}_final.zkey \
    0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f \
    10 \
    -n="Final Beacon phase2"

# Verify final zkey
snarkjs zkey verify \
    build/${CIRCUIT}.r1cs \
    keys/powersOfTau28_hez_final.ptau \
    keys/${CIRCUIT}_final.zkey
```

### Export Verification Key

```bash
# Generate verification key (for on-chain verification)
snarkjs zkey export verificationkey \
    keys/kyc_verification_final.zkey \
    keys/kyc_verification_vkey.json
```

## Generate Solidity Verifier

```bash
# Export Solidity verifier contract
snarkjs zkey export solidityverifier \
    keys/kyc_verification_final.zkey \
    contracts/KYCVerifier.sol
```

**Output (`KYCVerifier.sol`)**:

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract Groth16Verifier {
    // ... auto-generated verification code

    function verifyProof(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[1] memory input
    ) public view returns (bool r) {
        // Pairing verification
    }
}
```

## Development Workflow

### 1. Write Circuit

```circom
// circuits/example.circom
pragma circom 2.0.0;

template Example() {
    signal input a;
    signal input b;
    signal output c;

    c <== a * b;
}

component main = Example();
```

### 2. Compile & Test

```bash
# Compile
./scripts/compile.sh example

# Run tests
npm test
```

### 3. Setup Ceremony

```bash
# Generate keys
./scripts/setup.sh example
```

### 4. Generate Verifier

```bash
# Export Solidity contract
snarkjs zkey export solidityverifier \
    keys/example_final.zkey \
    contracts/ExampleVerifier.sol
```

## Testing Setup

### Install Test Dependencies

```bash
npm install --save-dev \
    circom_tester \
    chai \
    mocha
```

### Test File Example

`test/kyc_verification.test.js`:

```javascript
const { assert } = require("chai");
const wasm_tester = require("circom_tester").wasm;

describe("KYC Verification Circuit", function () {
  let circuit;

  this.timeout(100000); // Long timeout for circuit loading

  before(async () => {
    circuit = await wasm_tester("circuits/kyc_verification.circom");
  });

  it("Should generate witness successfully", async () => {
    const input = {
      userId: "12345",
      kycHash: "98765432109876543210",
      timestamp: "1704067200",
      providerSignature: "11111111111111111111",
    };

    const witness = await circuit.calculateWitness(input);
    await circuit.checkConstraints(witness);
  });

  it("Should output valid for correct inputs", async () => {
    const input = {
      userId: "12345",
      kycHash: "98765432109876543210",
      timestamp: "1704067200",
      providerSignature: "11111111111111111111",
    };

    const witness = await circuit.calculateWitness(input);

    // Check output signal (index 1 = first output)
    assert(witness[1] === 1n, "isValid should be 1");
  });
});
```

### Run Tests

```bash
# Run all tests
npm test

# Run specific test
npx mocha test/kyc_verification.test.js
```

## Environment Variables

Create `.env`:

```bash
# Circuit paths
CIRCUITS_DIR=./circuits
BUILD_DIR=./build
KEYS_DIR=./keys

# SnarkJS settings
POWERS_OF_TAU_FILE=powersOfTau28_hez_final.ptau
ENTROPY="random-entropy-string-12345"

# Contract deployment
PRIVATE_KEY=your_private_key_here
RPC_URL=https://rpc.sepolia.mantle.xyz
```

## Common Issues & Solutions

### Issue 1: Circom Not Found

```bash
# Error: circom: command not found

# Solution: Add to PATH
export PATH=$PATH:~/.cargo/bin

# Or use full path
~/.cargo/bin/circom --version
```

### Issue 2: WASM Out of Memory

```bash
# Error: Out of memory when generating witness

# Solution: Increase Node memory limit
NODE_OPTIONS="--max-old-space-size=8192" npm test
```

### Issue 3: Constraint Count Too High

```bash
# Warning: Circuit has 100k+ constraints

# Solution: Optimize circuit
# - Remove unnecessary constraints
# - Use more efficient templates
# - Split into multiple smaller circuits
```

## Production Checklist

Before deploying to mainnet:

- [ ] Circuit audited by ZK security firm
- [ ] Trusted setup ceremony completed with multiple participants
- [ ] All tests passing
- [ ] Verification key backed up securely
- [ ] Solidity verifier contract deployed and verified
- [ ] Gas costs estimated and acceptable
- [ ] Documentation complete

---

**Next**: [Proof Generation](./proof-generation) - Generate proofs in browser.
