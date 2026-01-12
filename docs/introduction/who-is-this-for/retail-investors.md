---
title: Retail Investors
sidebar_position: 1
---

# Retail Investors

Veilfi empowers individual DeFi users to earn competitive yields while protecting their financial privacy from surveillance, competitors, and bad actors.

## Key Benefits

### 1. Financial Privacy Protection

**Problem**: Every DeFi interaction permanently doxxes your wealth.

**Veilfi Solution**:

- Deposit amounts remain private (hidden via ZK proofs)
- Vault balances invisible to outsiders
- Withdrawal sizes protected cryptographically
- No on-chain link between deposits and your identity

**Real Impact**: Your crypto friend can't see you have more money than them. Your employer can't track your side income. Scammers can't target high-value wallets.

### 2. Simplified Yield Farming

**Problem**: Managing multiple DeFi protocols is time-consuming and expensive.

**Before Veilfi**:

```
Step 1: Deposit 10 ETH to Aave      → Gas: $15
Step 2: Deposit 10 ETH to Lido      → Gas: $20
Step 3: Provide 10 ETH to Uniswap   → Gas: $25
Step 4: Monitor 3 dashboards daily
Step 5: Manually rebalance monthly  → Gas: $60+
Total Gas: ~$120+ per month
```

**With Veilfi**:

```
Step 1: Deposit 30 ETH to Veilfi    → Gas: $18
Step 2: Vault auto-allocates to 3 protocols (free)
Step 3: Earn blended 7% APY automatically
Step 4: Admin rebalances (you pay nothing)
Total Gas: ~$18 per month (85% savings!)
```

### 3. MEV & Front-Running Protection

**Problem**: Large transparent transactions get front-run by MEV bots.

**Example Attack**:

> _You swap 50 ETH for USDC on Uniswap. A bot sees your transaction in the mempool, front-runs you, and extracts $500 in value from your trade._

**Veilfi Protection**:

- Deposit amounts are hidden → Bots can't size your transaction
- Vault handles all DeFi interactions → Your wallet not directly exposed
- Batched operations → Harder to target individual users

**Result**: Your privacy reduces MEV attack surface.

### 4. Portfolio Diversification (Auto-Managed)

Instead of picking one protocol, earn from multiple simultaneously:

| Strategy          | Your Allocation | Expected Yield |
| ----------------- | --------------- | -------------- |
| Aave Lending      | 40%             | 5% APY         |
| Lido Staking      | 30%             | 4.5% APY       |
| Uniswap LP        | 30%             | 12% APY        |
| **Blended Total** | **100%**        | **~7% APY**    |

**Benefit**: Higher returns with lower risk (don't put all eggs in one basket).

## Use Cases

### Use Case 1: Privacy-Conscious DeFi Farmer

**Profile**: Sarah has $50k in crypto and actively farms yields.

**Problem**:

- Shared her ENS on Twitter → Now everyone can see her $50k net worth
- Gets 10+ scam DMs per week targeting her wallet
- Worried about $5 wrench attacks (physical security risk)

**How Veilfi Helps**:

1. Deposits $50k to Veilfi privately
2. Amount hidden from public view
3. Earns 7% APY across Aave + Lido + Uniswap automatically
4. Scammers see "a deposit occurred" but not the $50k value

**Result**: Privacy restored, yield maximized, stress reduced.

### Use Case 2: Small Holder Seeking Efficiency

**Profile**: Mike has 5 ETH and wants passive income.

**Problem**:

- Too expensive to deposit to multiple protocols (gas fees eat profits)
- Doesn't have time to monitor yields daily
- Scared of missing rebalancing opportunities

**How Veilfi Helps**:

1. Single deposit of 5 ETH
2. Vault automatically spreads across 3 protocols
3. Admin rebalances when APYs shift (Mike pays nothing extra)
4. Just check balance monthly

**Result**: 85% gas savings, professional-grade strategy, zero effort.

### Use Case 3: Competitor Privacy

**Profile**: Alex is a DeFi degen who found a profitable strategy.

**Problem**:

- Every transaction is public → Competitors copy winning strategies
- On-chain analysis firms track his moves
- His edge disappears as copycats flood in

**How Veilfi Helps**:

1. Deposits privately to Veilfi
2. Vault allocations are aggregated (competitors can't see Alex's specific moves)
3. Withdrawals are anonymous
4. Strategy remains private

**Result**: Maintains alpha while earning yield.

## How It Works (Step-by-Step)

### Step 1: Connect Wallet

```
Open app.veilfi.xyz
↓
Click "Connect Wallet"
↓
Select MetaMask/WalletConnect
↓
Approve connection
```

### Step 2: Optional KYC (For Compliance)

```
If institutional or regulatory requirement:
↓
Generate ZK-KYC proof (off-chain)
↓
Submit proof hash (no PII stored on-chain)
↓
Receive "verified" status
```

### Step 3: Deposit with Privacy

```
Enter deposit amount (e.g., 10 ETH)
↓
Choose: "Private Deposit" (with ZK proof)
    OR: "Standard Deposit" (public)
↓
Sign transaction
↓
Receive vault shares (proportional to deposit)
```

### Step 4: Earn Yield Automatically

```
Vault auto-allocates to strategies:
├─ 4 ETH to Aave (5% APY)
├─ 3 ETH to Lido (4.5% APY)
└─ 3 ETH to Uniswap (12% APY)
↓
Yields compound automatically
↓
Your shares increase in value
```

### Step 5: Withdraw Anytime

```
Enter withdrawal amount (e.g., 5 ETH)
↓
Generate ZK proof of ownership
↓
Vault liquidates from strategies
↓
Receive ETH/USDC to your wallet
↓
Amount remains private to outsiders
```

## Requirements

### What You Need

✅ **Web3 Wallet**: MetaMask, Rainbow, or WalletConnect-compatible  
✅ **Network**: Mantle Sepolia (testnet) or Mantle (mainnet)  
✅ **Gas Token**: ETH for transaction fees  
✅ **Minimum Deposit**: 0.1 ETH (lower in future versions)

### Optional (For Enhanced Privacy)

⚙️ **VPN**: Hide IP address from RPC providers  
⚙️ **Fresh Wallet**: Use a new address unlinked to your identity  
⚙️ **Tor Browser**: Maximum network-level privacy

## Frequently Asked Questions

**Q: Is my deposit amount completely hidden?**  
A: Yes, if you use "Private Deposit" mode with ZK proof. Standard deposits are public like normal DeFi.

**Q: Can the Veilfi team see my balance?**  
A: No. Even we can't see individual balances—only cryptographic proof hashes and total vault TVL.

**Q: What if I lose my ZK proof?**  
A: You can regenerate it using your wallet (same private key = same proof). No risk of fund loss.

**Q: How do I know my funds are safe?**  
A: Veilfi is non-custodial—you retain full control. Smart contracts are open source and auditable.

**Q: What's the fee structure?**  
A: 0% deposit fee, 1% annual management fee, 10% performance fee on profits, 0.1% withdrawal fee.

---

**Ready to get started?** Visit the [User Flow Guide](../../core-flow/user-flow/wallet-connection) for a detailed walkthrough.

**Want more privacy details?** Check out [ZK Circuits](../../zk-circuits/introduction) to understand the cryptography.
