---
title: Private Deposits
sidebar_position: 1
---

# Private Deposits

Deposit funds with Zero-Knowledge proofs to hide deposit amounts from public view.

## How It Works

```
User wants to deposit 10 ETH privately:

1. Generate ZK proof locally (in browser)
   Input: depositAmount = 10 ETH (PRIVATE)
   Output: commitment = hash(amount, secret)

2. Submit proof + commitment to blockchain
   Blockchain sees: "Valid deposit proof"
   Blockchain CANNOT see: Actual 10 ETH amount

3. Receive vault shares
   Share balance visible, but deposit amount hidden
```

## Implementation

```tsx
import { generateDepositProof } from "@veilfi/zk-circuits";

async function privateDeposit(amount) {
  // 1. Generate proof (5-10 seconds)
  setStatus("Generating proof...");

  const proof = await generateDepositProof({
    depositAmount: parseEther(amount),
    userSecret: generateRandomSecret(),
  });

  // 2. Submit to contract
  setStatus("Submitting to blockchain...");

  const tx = await vault.depositWithProof(
    proof.a,
    proof.b,
    proof.c,
    proof.publicSignals,
    { value: parseEther(amount) }
  );

  await tx.wait();

  setStatus("✅ Private deposit complete!");
}
```

## Privacy vs Standard Deposit

| Aspect                | Standard | Private                 |
| --------------------- | -------- | ----------------------- |
| **Amount Visibility** | Public   | Hidden                  |
| **Gas Cost**          | ~100k    | ~350k (ZK verification) |
| **Time**              | Instant  | +10s (proof generation) |
| **Privacy**           | None     | Full                    |

## Use Cases

- Large deposits (hide net worth)
- Institutional treasuries (conceal strategy)
- Privacy-conscious users (general privacy)

---

**Next**: [Private Withdrawals](./private-withdrawals)
