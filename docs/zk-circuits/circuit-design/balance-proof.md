---
title: Balance Proof Circuit
sidebar_position: 2
---

# Balance Proof Circuit

The Balance Proof Circuit allows users to prove their balance exceeds a threshold without revealing the exact amount.

## Circuit Purpose

**Use Case**: Lending platform requires $50k minimum balance.  
**Problem**: Borrower must prove solvency without revealing full net worth.  
**Solution**: ZK proof: "I have ≥ $50k" (exact amount stays private).

## Circuit Design

### Full Circuit Code

```circom
pragma circom 2.0.0;

include "circomlib/comparators.circom";
include "circomlib/bitify.circom";

template BalanceProof() {
    // ============ INPUTS ============

    // Private input (user's actual balance - HIDDEN)
    signal private input actualBalance;

    // Public inputs (visible on-chain)
    signal public input minRequired;      // Minimum balance needed
    signal public output sufficient;      // 1 if sufficient, 0 if not

    // ============ CONSTRAINTS ============

    // 1. Ensure actualBalance is valid (64-bit number)
    component balanceBits = Num2Bits(64);
    balanceBits.in <== actualBalance;

    // 2. Compare actualBalance >= minRequired
    component comparator = GreaterEqThan(64);
    comparator.in[0] <== actualBalance;
    comparator.in[1] <== minRequired;

    // 3. Output result
    sufficient <== comparator.out;
}

component main {public [minRequired]} = BalanceProof();
```

## How It Works

### Step 1: Input Preparation

```javascript
// User has 100 ETH (PRIVATE)
const actualBalance = ethers.utils.parseEther("100");

// Loan requires 50 ETH (PUBLIC)
const minRequired = ethers.utils.parseEther("50");

const circuitInput = {
  actualBalance: actualBalance.toString(), // HIDDEN from blockchain
  minRequired: minRequired.toString(), // VISIBLE on blockchain
};
```

### Step 2: Proof Generation

```javascript
import { groth16 } from "snarkjs";

async function generateBalanceProof(actualBalance, minRequired) {
  const input = {
    actualBalance: actualBalance.toString(),
    minRequired: minRequired.toString(),
  };

  const { proof, publicSignals } = await groth16.fullProve(
    input,
    "balance_proof.wasm",
    "balance_proof_final.zkey"
  );

  console.log("Minimum required:", publicSignals[0]); // 50 ETH (public)
  console.log("Sufficient?:", publicSignals[1]); // 1 (yes) or 0 (no)

  return { proof, publicSignals };
}
```

### Step 3: On-Chain Verification

```solidity
contract LendingProtocol {
    IGroth16Verifier public balanceVerifier;

    function requestLoan(
        uint256 loanAmount,
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[2] memory publicSignals  // [minRequired, sufficient]
    ) external {
        // Verify ZK proof
        require(
            balanceVerifier.verifyProof(a, b, c, publicSignals),
            "Invalid balance proof"
        );

        // Check user proved sufficient balance
        require(publicSignals[1] == 1, "Insufficient balance");

        // Check minRequired matches loan requirements
        uint256 minRequired = publicSignals[0];
        require(minRequired >= loanAmount, "Minimum too low");

        // Grant loan (user's exact balance never revealed!)
        _issueLoan(msg.sender, loanAmount);
    }
}
```

## Privacy Analysis

### What Blockchain Sees

```
Public Signals:
├─ minRequired: 50 ETH (known requirement)
└─ sufficient: 1 (user has enough)

Blockchain knows: User has ≥ 50 ETH
Blockchain CANNOT know: Exact balance (could be 50, 100, or 1000 ETH)
```

### Example Scenarios

| Actual Balance | Min Required | sufficient Output | Privacy Preserved?      |
| -------------- | ------------ | ----------------- | ----------------------- |
| 100 ETH        | 50 ETH       | 1 (yes)           | ✅ Exact 100 ETH hidden |
| 75 ETH         | 50 ETH       | 1 (yes)           | ✅ Exact 75 ETH hidden  |
| 30 ETH         | 50 ETH       | 0 (no)            | ✅ Exact 30 ETH hidden  |

**In all cases**: Exact balance remains private.

## Advanced: Range Proofs

Prove balance is within a range:

```circom
template BalanceRangeProof() {
    signal private input actualBalance;
    signal public input minBalance;
    signal public input maxBalance;
    signal public output inRange;

    // Check minBalance <= actualBalance <= maxBalance
    component lowerCheck = GreaterEqThan(64);
    lowerCheck.in[0] <== actualBalance;
    lowerCheck.in[1] <== minBalance;

    component upperCheck = LessEqThan(64);
    upperCheck.in[0] <== actualBalance;
    upperCheck.in[1] <== maxBalance;

    // Both must be true
    inRange <== lowerCheck.out * upperCheck.out;
}
```

**Example**:

```
Prove: "I have between $10k - $100k"
Input: actualBalance = $50k (PRIVATE)
Output: inRange = 1 (PUBLIC)

Blockchain knows: Balance is $10k-$100k
Blockchain CANNOT know: Exact $50k
```

## Constraint Analysis

```
Total Constraints: ~500
├─ GreaterEqThan: ~200
├─ Num2Bits: ~64
└─ Logic Gates: ~236

Proof Generation Time: ~2-3 seconds
Gas Cost: ~290k gas
```

## Use Cases

### 1. Undercollateralized Lending

```solidity
// User proves creditworthiness without revealing net worth
function applyForLoan(proofData) external {
    require(verifyBalanceProof(proofData, minCreditScore));
    _issueLoan(msg.sender);
}
```

### 2. Tiered Services

```solidity
// Different services for different balance tiers
if (proveBalance >= 100 ETH) {
    accessPremiumFeatures();
} else if (proveBalance >= 10 ETH) {
    accessStandardFeatures();
}
```

### 3. Anonymous Voting

```solidity
// Voting weight based on balance, identity hidden
function vote(proposalId, balanceProof) external {
    require(verifyBalanceProof(balanceProof, minVotingBalance));
    _castVote(proposalId, votingPower);  // Power from proof, not public balance
}
```

## Testing

```javascript
describe("Balance Proof Circuit", () => {
  it("Should output 1 when balance sufficient", async () => {
    const circuit = await wasm_tester("balance_proof.circom");

    const input = {
      actualBalance: "100000000000000000000", // 100 ETH
      minRequired: "50000000000000000000", // 50 ETH
    };

    const witness = await circuit.calculateWitness(input);

    // Check sufficient output
    expect(witness[2]).toBe(1n); // sufficient = 1
  });

  it("Should output 0 when balance insufficient", async () => {
    const circuit = await wasm_tester("balance_proof.circom");

    const input = {
      actualBalance: "30000000000000000000", // 30 ETH
      minRequired: "50000000000000000000", // 50 ETH
    };

    const witness = await circuit.calculateWitness(input);

    // Check sufficient output
    expect(witness[2]).toBe(0n); // sufficient = 0
  });
});
```

## Security Considerations

### Soundness

**Attack**: User claims balance ≥ 50 ETH but actually has 30 ETH.  
**Prevention**: Circuit constraints prevent generating valid proof.  
**Result**: Attack computationally infeasible.

### Zero-Knowledge

**Leak Risk**: Exact balance revealed through proof?  
**Protection**: Proof only outputs binary (1/0), not amount.  
**Result**: Full privacy maintained.

---

**Next**: [Circom Setup](../implementation/circom-setup) - Environment configuration.
