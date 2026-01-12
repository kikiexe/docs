---
title: Private Withdrawals
sidebar_position: 2
---

# Private Withdrawals

Withdraw funds using Zero-Knowledge proofs to hide withdrawal amounts (future feature).

## Current Status

⚠️ **Coming Soon**: Private withdrawals are planned for v2.

**Current**: Standard withdrawals (amounts visible on-chain)

## Planned Implementation

### How It Will Work

```
User wants to withdraw 5 ETH privately:

1. Generate ownership proof
   Prove: "I own ≥ 5 ETH worth of shares"
   Without revealing: Exact share balance

2. Submit proof to contract
   Contract verifies proof
   Burns shares privately

3. Receive ETH
   Withdrawal event emitted (amount hidden)
```

### Technical Design

```circom
template WithdrawalProof() {
    signal private input userShares;       // HIDDEN
    signal private input sharePrice;       // HIDDEN
    signal public input minWithdrawal;     // PUBLIC
    signal public output canWithdraw;      // PUBLIC

    // Prove: userShares × sharePrice ≥ minWithdrawal
    signal userValue <== userShares * sharePrice;

    component check = GreaterEqThan(64);
    check.in[0] <== userValue;
    check.in[1] <== minWithdrawal;

    canWithdraw <== check.out;
}
```

## Workaround (Current)

For privacy-conscious users:

1. **Withdraw to fresh address**

   ```
   Create new wallet → Withdraw to new address
   → Break link to deposit address
   ```

2. **Use mixer after withdrawal**

   ```
   Withdraw → Send to Tornado Cash/Railgun
   → Enhanced privacy
   ```

3. **Batch withdrawals**
   ```
   Wait for other users to withdraw
   → Your withdrawal hidden in batch
   ```

## Roadmap

- **Q2 2024**: Design & audit withdrawal proof circuit
- **Q3 2024**: Testnet deployment
- **Q4 2024**: Mainnet launch

---

**Congratulations!** You've completed the **Core Flow** section.

**Next**: Explore [Key Features](../../key-features/multi-strategy-vault), [Smart Contracts](../../technical-details/overview), or other sections.
