---
title: Zero-Knowledge Proofs
sidebar_position: 2
---

# Zero-Knowledge Proofs

Zero-Knowledge Proofs (ZKPs) are cryptographic methods that allow one party to prove knowledge of information **without revealing the information itself**. Veilfi uses ZK-SNARKs to enable privacy-preserving DeFi.

## What are Zero-Knowledge Proofs?

### The Core Concept

**Definition**: A ZK proof lets you prove a statement is true without revealing why it's true.

**Classic Example**: Ali Baba's Cave

```
Problem: You want to prove you know a secret password
         WITHOUT revealing the password itself.

Solution:
1. Enter the cave through entrance A or B
2. Exit through the opposite side
3. Observer sees you went in A, came out B
4. Only way to do this: You know the secret door password
5. Password never revealed, but knowledge proven!
```

### Mathematical Example

**Prove you know x where x² = 9, without revealing x**:

```
Standard proof: "x = 3" → REVEALS the value

Zero-Knowledge proof:
Prover: "I know a value x such that x² = 9"
Verifier: "Prove it without telling me x"
Prover:
  - Generates cryptographic commitment C
  - Creates proof π that proves "C encrypts a value x where x² = 9"
  - Sends (C, π) to verifier
Verifier:
  - Checks proof π is valid
  - Learns NOTHING about x itself
  - Convinced x exists and satisfies x² = 9
```

**Result**: Statement proven, secret never revealed.

## ZK-SNARKs (What Veilfi Uses)

### Definition

**SNARK** = **S**uccinct **N**on-interactive **AR**gument of **K**nowledge

**Properties**:

- **Succinct**: Proofs are tiny (~200 bytes), verification fast
- **Non-interactive**: No back-and-forth (prover generates proof once)
- **Argument**: Computationally sound (breaking requires immense computing power)
- **of Knowledge**: Proves you know a secret, not just that it exists

### Why SNARKs vs Other ZK Systems?

| ZK System     | Proof Size    | Verification Speed | Setup Needed     | Best For                       |
| ------------- | ------------- | ------------------ | ---------------- | ------------------------------ |
| **zk-SNARKs** | 🟢 ~200 bytes | 🟢 ~5ms            | ⚠️ Yes (trusted) | Blockchain (Veilfi uses this!) |
| zk-STARKs     | 🟡 ~100KB     | 🟡 ~50ms           | ✅ No            | Post-quantum security          |
| Bulletproofs  | 🟡 ~1-2KB     | 🔴 ~500ms          | ✅ No            | Confidential transactions      |

**Veilfi Choice**: SNARKs for smallest on-chain footprint and fastest verification.

## How Veilfi Uses Zero-Knowledge Proofs

### Use Case 1: Private Deposit Amounts

**Problem**: Standard deposit reveals amount on-chain.

```solidity
// ❌ Public deposit
function deposit(uint256 amount) public {
    // Everyone sees: "Alice deposited 10 ETH"
}
```

**Veilfi Solution**: Prove deposit without revealing amount.

```circom
// ZK Circuit (simplified)
template DepositProof() {
    signal private input depositAmount;  // HIDDEN
    signal private input userSecret;      // HIDDEN
    signal public output  commitment;     // PUBLIC

    // Prove: "I deposited SOME amount" without revealing it
    commitment <== hash(depositAmount, userSecret);
}
```

**On-Chain Verification**:

```solidity
function depositWithProof(
    uint256[2] memory a,      // Proof component A
    uint256[2][2] memory b,   // Proof component B
    uint256[2] memory c,      // Proof component C
    uint256[3] memory publicSignals  // Public outputs
) external payable {
    // Verify proof is valid
    require(zkVerifier.verifyProof(a, b, c, publicSignals), "Invalid proof");

    // Deposit processed, amount never revealed on-chain
    _mint(msg.sender, shares);
}
```

**Result**: Blockchain knows "a valid deposit occurred" but not the amount.

### Use Case 2: KYC Without Identity Exposure

**Problem**: Proving you're KYC-verified exposes identity.

**Veilfi's ZK-KYC Circuit**:

```circom
template KYCVerification() {
    signal private input userId;        // Your ID (HIDDEN)
    signal private input kycHash;       // KYC certificate hash (HIDDEN)
    signal private input timestamp;     // When KYC was done (HIDDEN)
    signal public output  isValid;      // Result: 1 or 0 (PUBLIC)

    // Check: KYC hash matches registered hash for userId
    component checker = KYCChecker();
    checker.userId <== userId;
    checker.kycHash <== kycHash;
    checker.timestamp <== timestamp;

    // Output 1 if valid, 0 if not
    isValid <== checker.valid;
}
```

**What's Stored On-Chain**:

```
✅ Proof hash: 0x7a3f8b2... (meaningless to outsiders)
✅ isValid: 1 (yes, user is KYC'd)
❌ NO name, passport, address, or PII
```

**Result**: Compliance without doxxing.

### Use Case 3: Balance Proof (Prove Solvency)

**Problem**: Prove you have > $X without revealing exact balance.

**Circuit**:

```circom
template BalanceProof() {
    signal private input actualBalance;    // Your real balance (HIDDEN)
    signal public input  minRequired;      // Minimum needed (PUBLIC)
    signal public output sufficient;       // Result (PUBLIC)

    // Check actualBalance >= minRequired
    component comparator = GreaterEqThan(64);
    comparator.in[0] <== actualBalance;
    comparator.in[1] <== minRequired;

    sufficient <== comparator.out;  // 1 if sufficient, 0 if not
}
```

**Example**:

```
Alice's actual balance: 100 ETH (HIDDEN)
Loan requires: 50 ETH (PUBLIC)

Alice generates proof:
  Input: actualBalance = 100 ETH (private)
  Input: minRequired = 50 ETH (public)
  Output: sufficient = 1 (public)

Lender sees: "Alice has >= 50 ETH"
Lender CANNOT see: Her exact 100 ETH balance
```

## ZK Proof Lifecycle in Veilfi

### Step 1: Circuit Design (Developer)

```circom
// developers/circuits/balance_proof.circom
template BalanceProof() {
    // Define computation
    signal private input secretValue;
    signal public output result;

    // Prove secretValue satisfies some condition
    result <== secretValue * secretValue;
}
```

### Step 2: Trusted Setup (Powers of Tau)

```bash
# Generate proving key and verification key
circom balance_proof.circom --r1cs --wasm --sym
snarkjs groth16 setup balance_proof.r1cs powersOfTau28.ptau
snarkjs zkey export verificationkey circuit_final.zkey verification_key.json
```

**Outputs**:

- **Proving Key** (used by users to generate proofs)
- **Verification Key** (used by smart contract to verify proofs)

### Step 3: Proof Generation (User's Browser)

```javascript
// User's browser (privacy preserved - runs locally)
import { groth16 } from "snarkjs";

async function generateProof(userBalance, minRequired) {
  const input = {
    actualBalance: userBalance, // Private: hidden from blockchain
    minRequired: minRequired, // Public: will be revealed
  };

  // Generate proof locally (takes ~5-10 seconds)
  const { proof, publicSignals } = await groth16.fullProve(
    input,
    "balance_proof.wasm",
    "circuit_final.zkey"
  );

  return { proof, publicSignals };
}

// Example usage
const balanceProof = await generateProof(
  BigInt(100e18), // User has 100 ETH (PRIVATE)
  BigInt(50e18) // Minimum required 50 ETH (PUBLIC)
);
```

### Step 4: Proof Verification (Smart Contract)

```solidity
// On-chain verifier contract
contract Groth16Verifier {
    function verifyProof(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[1] memory input  // Public signals only
    ) public view returns (bool) {
        // Cryptographic verification using elliptic curve pairing
        // Takes ~300k gas, completes in milliseconds
        return pairing(...);  // Returns true if valid
    }
}
```

### Step 5: Action Execution (Vault)

```solidity
// Veilfi vault uses verification result
function depositWithBalanceProof(...) external payable {
    // Step A: Verify proof
    bool proofValid = zkVerifier.verifyProof(a, b, c, publicSignals);
    require(proofValid, "Invalid proof");

    // Step B: Execute deposit
    // Vault knows: proof is valid
    // Vault CANNOT know: exact deposit amount (it's hidden)
    _processDeposit(msg.sender, msg.value);
}
```

## Properties of ZK Proofs

### 1. Completeness

**Definition**: If a statement is true, an honest prover can always convince an honest verifier.

**Example**:

```
If Alice really deposited 10 ETH, she WILL be able to generate a valid proof.
```

### 2. Soundness

**Definition**: If a statement is false, a dishonest prover cannot convince an honest verifier (except with negligible probability).

**Example**:

```
If Bob claims he deposited 100 ETH but only sent 10 ETH,
he CANNOT generate a valid proof (computationally infeasible).
```

### 3. Zero-Knowledge

**Definition**: The proof reveals nothing beyond the validity of the statement.

**Example**:

```
Proof of "I have ≥ 50 ETH" reveals:
✅ Alice has at least 50 ETH
❌ Exact balance (could be 50, 100, or 1000 ETH)
```

## Technical Advantages

### For Users

✅ **Privacy**: Deposit amounts, balances, KYC data remain private  
✅ **Non-custodial**: Generate proofs client-side (no trusted third party)  
✅ **Verifiable**: Anyone can verify proofs without seeing secrets  
✅ **Composable**: Proofs can be reused across protocols

### For Veilfi Protocol

✅ **On-chain efficiency**: Tiny proof size (~200 bytes)  
✅ **Fast verification**: ~300k gas (~5ms on L2)  
✅ **Trustless**: Math-based security, not trust-based  
✅ **Regulatory compatible**: Compliance without surveillance

## Limitations & Trade-offs

### What ZK Proofs Don't Hide

❌ **Transaction existence**: Deposit/withdrawal events are still visible  
❌ **Wallet address**: Public on blockchain (use fresh wallet for privacy)  
❌ **Timing**: Timestamp of transactions is public  
❌ **Gas costs**: Transaction fees are visible

### Performance Considerations

⚠️ **Proof generation time**: 5-15 seconds on modern hardware  
⚠️ **Gas costs**: ~300k gas for verification (2x standard deposit)  
⚠️ **Computational requirements**: Needs decent CPU (mobile compatible but slower)  
⚠️ **Trusted setup**: Requires ceremony (potential vulnerability if compromised)

## Security Model

### Cryptographic Assumptions

Veilfi's ZK security relies on:

1. **Discrete Logarithm Problem**: Hard to solve on elliptic curves (widely accepted)
2. **Decisional Diffie-Hellman**: Standard cryptographic assumption
3. **Trusted Setup Honesty**: At least 1 participant in ceremony must be honest

**Risk Level**: 🟢 Low (same assumptions as Zcash, Tornado Cash, Aztec)

### Attack Scenarios

| Attack                        | Feasibility                               | Mitigation                  |
| ----------------------------- | ----------------------------------------- | --------------------------- |
| **Forge fake proof**          | 🟢 Computationally infeasible             | Math-based security         |
| **Extract secret from proof** | 🟢 Impossible (zero-knowledge property)   | Cryptographic guarantee     |
| **Compromise trusted setup**  | 🟡 Requires collusion of ALL participants | Multi-party ceremony        |
| **Quantum computer attack**   | 🔴 Future risk (10-20 years)              | Migrate to STARKs if needed |

---

**Next**: Explore [Privacy-Preserving DeFi](./privacy-preserving-defi) to see ZK proofs in action.

**Technical Deep Dive**: Check out [ZK Circuits](../../zk-circuits/introduction) for implementation details.
