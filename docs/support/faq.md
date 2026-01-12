---
title: FAQ
sidebar_position: 1
---

# Frequently Asked Questions

Common questions about Veilfi and privacy-preserving yield aggregation.

## General

### What is Veilfi?

Veilfi is a privacy-preserving yield aggregator that lets you earn ~7% APY on ETH while keeping your deposit amounts and balances private through Zero-Knowledge proofs.

### How does Veilfi generate yield?

We diversify your capital across three battle-tested DeFi protocols:

- 40% Aave (lending)
- 30% Lido (ETH staking)
- 30% Uniswap (liquidity provision)

Combined blended APY: ~7-8%

### Is Veilfi safe?

**Security measures**:

- ✅ Non-custodial (you control your funds)
- ✅ Only battle-tested protocols (2+ years, $1B+ TVL)
- ✅ Open source & verified contracts
- ✅ Planned professional audit

**Risks**:

- Smart contract bugs (like all DeFi)
- Underlying protocol exploits (mitigated by diversification)
- See [Known Risks](/docs/security/known-risks) for full disclosure

### What's the minimum deposit?

**Minimum**: 0.01 ETH  
**Maximum**: 1000 ETH per transaction (gradually increasing)

## Privacy

### How private is it really?

**What's private**:

- ❌ Deposit amounts (with ZK proofs)
- ❌ Exact balances (only share count visible)
- ❌ KYC identity details

**What's public**:

- ✅ Wallet address (Ethereum limitation)
- ✅ Number of vault shares
- ✅ Transaction timing

**Privacy level**: High for amounts, medium for wallet addresses

### Do I need KYC?

**Tiered system**:

- < 10 ETH: No KYC required
- 10-100 ETH: KYC recommended
- \> 100 ETH: ZK-KYC required

KYC uses Zero-Knowledge proofs - only verification status is stored on-chain, not your identity.

### Can the government see my deposits?

**Short answer**: Wallet addresses are public, but amounts can be private (with ZK proofs).

**Details**:

- Standard deposit: Amount visible on-chain
- Private deposit (ZK): Amount hidden
- Blockchain is public, but ZK proofs hide specific values
- With court order: KYC provider can reveal identity (not Veilfi)

## Technical

### What's a Zero-Knowledge proof?

A cryptographic method to prove something is true without revealing the underlying data.

**Example**:

- Traditional: "I deposited 100 ETH" (amount exposed)
- ZK Proof: "I made a valid deposit" (amount hidden)

The blockchain verifies the proof is valid without seeing your actual deposit amount.

### Why does proof generation take 10 seconds?

ZK proof generation is computationally intensive - your browser needs to:

1. Load circuit files (~5MB)
2. Perform cryptographic calculations
3. Generate the proof

We're working on optimizations (Web Workers, smaller circuits).

### What chains does Veilfi support?

**Current**: Mantle Sepolia Testnet (for hackathon)

**Planned**:

- Mantle Mainnet (Q2 2024)
- Arbitrum (Q3 2024)
- Optimism (Q4 2024)
- Base, Polygon zkEVM (2025)

## Yields & Fees

### Is 7% APY guaranteed?

**No**. APY fluctuates based on:

- Underlying protocol rates
- Market conditions
- Utilization rates

**Historical range**: 5-10% APY  
**Current**: ~7% APY

### What are the fees?

- **Deposit fee**: 0% (FREE)
- **Withdrawal fee**: 0.1%
- **Management fee**: 1% annual (from yields)
- **Performance fee**: 10% of profits

**Example**:

- Deposit: 100 ETH
- Earn: 7 ETH in 1 year
- Fees: 0.1 ETH (management) + 0.7 ETH (performance) = 0.8 ETH
- Net profit: 6.2 ETH

### Can I withdraw anytime?

**Yes**, withdrawals are processed immediately if vault has liquidity.

**Typical withdrawal**:

- Small (&lt;5% of vault): Instant
- Large (&gt;10% of vault): May take 1-2 hours (strategy liquidation)

### What if I lose my wallet?

**You lose access to your funds**. Veilfi cannot recover your funds - we don't have your private keys.

**Prevention**:

- Backup seed phrase securely
- Use hardware wallet for large amounts
- Never share private keys

## Comparison

### Veilfi vs Tornado Cash?

| Aspect         | Veilfi                | Tornado Cash               |
| -------------- | --------------------- | -------------------------- |
| **Privacy**    | High (amounts hidden) | Very High (full anonymity) |
| **Yields**     | ✅ 7% APY             | ❌ None                    |
| **Compliance** | ✅ KYC-compatible     | ❌ Sanctioned              |
| **Regulation** | ✅ Compliant          | ❌ Banned                  |

Veilfi is for **yield + privacy**, Tornado was for **full anonymity**.

### Veilfi vs Yearn Finance?

| Aspect         | Veilfi       | Yearn          |
| -------------- | ------------ | -------------- |
| **Privacy**    | ✅ ZK proofs | ❌ Public      |
| **APY**        | ~7%          | ~8%            |
| **Strategies** | 3 (curated)  | 100+ (complex) |
| **UX**         | Simple       | Advanced       |

Veilfi trades slightly lower APY for privacy + simplicity.

## Troubleshooting

### Transaction failed?

**Common issues**:

1. Insufficient gas (add more MNT)
2. Wrong network (switch to Mantle Sepolia)
3. Amount too small (&lt;0.01 ETH minimum)
4. Slippage too high (try smaller amount)

See [Troubleshooting](/docs/support/troubleshooting) for detailed fixes.

### Proof generation stuck?

1. Refresh page
2. Use desktop browser (mobile may run out of memory)
3. Close other tabs
4. Try standard deposit (non-private)

### Wrong network?

Click network selector in wallet → Switch to "Mantle Sepolia Testnet"

**Network details**:

- Chain ID: 5003
- RPC: https://rpc.sepolia.mantle.xyz

---

**Still have questions?** Join our [Community](/docs/support/community)
