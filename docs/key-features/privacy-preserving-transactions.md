---
title: Privacy-Preserving Transactions
sidebar_position: 1
---

# Privacy-Preserving Transactions

Veilfi enables users to deposit, earn, and withdraw while maintaining financial privacy through Zero-Knowledge proofs.

## How Privacy Works

### Traditional DeFi (Public)

```
User 0xAlice deposits 100 ETH
↓
Blockchain records: "0xAlice deposited 100 ETH"
↓
Anyone can see:
- Alice's address
- Exact deposit amount
- Current balance
- Transaction history
- Yield earnings
```

**Problem**: Complete financial transparency = No privacy

### Veilfi (Private)

```
User 0xAlice deposits 100 ETH with ZK proof
↓
Blockchain records: "0xAlice submitted valid deposit proof"
↓
Public can see:
- Alice's address ✅
- Proof hash ✅
- Vault shares minted ✅

Public CANNOT see:
- Deposit amount ❌
- Exact balance ❌
- Yield earnings ❌
```

**Solution**: Prove validity without revealing amounts

## Privacy Layers

### Layer 1: Deposit Privacy

Hide deposit amounts using ZK proofs:

```tsx
// Generate proof client-side
const proof = await generateDepositProof({
  amount: parseEther("100"), // PRIVATE
  userSecret: randomSecret(), // PRIVATE
});

// Submit only proof to contract
await vault.depositWithProof(proof.a, proof.b, proof.c, proof.publicSignals, {
  value: parseEther("100"),
});

// Blockchain sees: "Valid deposit proof" ✅
// Blockchain doesn't see: "100 ETH" ❌
```

### Layer 2: Balance Privacy

Hide exact balances through share system:

```
Standard DeFi:
Query balance → Returns "100 ETH" (PUBLIC)

Veilfi:
Query balance → Returns "90.5 shares" (amount value HIDDEN)
Share price = Only user can calculate actual value
```

### Layer 3: KYC Privacy

Prove compliance without revealing identity:

```circom
// ZK Circuit proves:
"User is KYC-verified" ✅

// Circuit doesn't reveal:
- Name ❌
- Passport number ❌
- Address ❌
- Date of birth ❌
```

## Privacy vs Transparency Trade-offs

| Aspect                  | Traditional DeFi          | Veilfi                |
| ----------------------- | ------------------------- | --------------------- |
| **Deposit Amounts**     | Public                    | Private (optional)    |
| **Withdrawal Amounts**  | Public                    | Private (v2)          |
| **Balances**            | Public                    | Semi-private (shares) |
| **KYC Identity**        | Either full KYC or no KYC | ZK-KYC (yes/no only)  |
| **Transaction History** | Fully traceable           | Partially obscured    |
| **APY Earnings**        | Calculable                | Hidden in share price |

## Technical Implementation

### ZK Proof Generation

```javascript
import { groth16 } from "snarkjs";

async function generatePrivateDepositProof(amount, secret) {
  // 1. Prepare circuit inputs (all private)
  const input = {
    depositAmount: amount,
    userSecret: secret,
  };

  // 2. Generate Groth16 proof (~10 seconds)
  const { proof, publicSignals } = await groth16.fullProve(
    input,
    "circuits/deposit.wasm",
    "circuits/deposit_final.zkey"
  );

  // 3. Proof contains no information about amount
  return { proof, publicSignals };
}
```

### On-Chain Verification

```solidity
function depositWithProof(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[1] memory publicSignals
) external payable {
    // Verify proof is valid
    require(zkVerifier.verifyProof(a, b, c, publicSignals));

    // Process deposit without storing amount
    _mint(msg.sender, _calculateShares(msg.value));

    // Event only shows proof was valid
    emit PrivateDeposit(msg.sender, publicSignals[0]);
}
```

## Privacy Guarantees

### What's Protected

✅ **Deposit amounts** - Hidden on-chain  
✅ **Withdrawal amounts** - (v2 feature)  
✅ **Exact balances** - Only share count visible  
✅ **KYC identity** - Only verification status visible  
✅ **Yield earnings** - Embedded in share price changes

### What's Still Public

🔓 **Wallet addresses** - Ethereum addresses are public  
🔓 **Transaction timing** - Block timestamps visible  
🔓 **Vault shares** - Number of shares held  
🔓 **Proof validity** - That proof was valid/invalid  
🔓 **Contract interactions** - Which functions called

## Privacy Best Practices

### For Maximum Privacy

1. **Use fresh wallet**

   ```
   Create new address → Fund via DEX
   → No link to identity
   ```

2. **Batch with others**

   ```
   Wait for multiple users to transact
   → Your transaction hidden in crowd
   ```

3. **Use VPN/Tor**

   ```
   Hide IP address when connecting wallet
   ```

4. **Private funding**

   ```
   Bridge from privacy chain (Monero/Zcash)
   → Fund Veilfi wallet
   ```

5. **Don't publicize**
   ```
   Don't share wallet address on social media
   ```

## Comparison with Alternatives

| Solution          | Privacy Level    | Regulatory        | Usability |
| ----------------- | ---------------- | ----------------- | --------- |
| **Veilfi**        | High (ZK proofs) | ✅ KYC-compatible | Easy      |
| **Tornado Cash**  | Very High        | ❌ Not compliant  | Complex   |
| **Standard DeFi** | None             | ✅ Transparent    | Easy      |
| **Aztec**         | Very High        | ⚠️ Partial        | Medium    |
| **Railgun**       | High             | ⚠️ Partial        | Medium    |

**Veilfi Advantage**: Balance privacy with compliance

## Limitations

### Current Limitations

- ⚠️ Wallet addresses still public (Ethereum limitation)
- ⚠️ Share balances visible (not amounts)
- ⚠️ Transaction timing visible
- ⚠️ Withdrawal privacy not yet implemented (v2)

### Future Improvements (Roadmap)

- 🔄 Private withdrawals (Q3 2024)
- 🔄 Stealth addresses (Q4 2024)
- 🔄 Cross-chain privacy bridges (2025)
- 🔄 Fully private balances (2025)

## Use Cases

### Individual Privacy

**Scenario**: High-net-worth individual wants yield without exposing wealth

```
Problem: Standard DeFi → "This wallet has $10M"
Solution: Veilfi → "This wallet has vault shares" (value hidden)
```

### Institutional Treasury

**Scenario**: DAO wants to earn yield without revealing strategy

```
Problem: Competitors see: "DAO X deployed $50M to Aave"
Solution: Veilfi hides allocation amounts
```

### Activist Protection

**Scenario**: Journalist in authoritarian country needs private savings

```
Problem: Government can track all DeFi activity
Solution: Veilfi provides financial privacy
```

---

**Next**: [Multi-Strategy Aggregation](./multi-strategy-aggregation) - Diversified yield sources.
