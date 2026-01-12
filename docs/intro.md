# ZK-Yield Protocol

Welcome to **ZK-Yield** - a privacy-preserving yield aggregator built on zero-knowledge proofs.

## 30-Second Overview

**Problem**: DeFi users can't earn optimized yields while maintaining financial privacy. Traditional yield aggregators expose all transaction details on-chain.

**Solution**: ZK-Yield's privacy-first architecture enables users to deposit, earn yields across multiple DeFi strategies, and withdraw - all while keeping their financial data private through ZK-SNARK proofs.

**Innovation**:

- 🔐 **Private Transactions** → Zero-knowledge proofs hide transaction details
- 🎯 **Multi-Strategy** → Auto-allocate to Aave, Lido, Uniswap for optimal yields
- ✅ **Compliant KYC** → Prove KYC status without revealing identity
- 💎 **Transparent Verification** → All proofs verifiable on-chain

**Status**: ✅ MVP deployed on Mantle Sepolia | 🚀 Multi-strategy vault active

**Why Mantle**: Optimized for Mantle's low-fee architecture with native integration to leading DeFi protocols.

---

## What is ZK-Yield?

**ZK-Yield** is a decentralized yield aggregation protocol that maximizes returns across multiple DeFi strategies while preserving complete user privacy through zero-knowledge proofs.

Built on the Mantle blockchain, ZK-Yield implements a novel privacy-preserving architecture that ensures both capital efficiency and regulatory compliance.

### Core Value Propositions

1. **Privacy First** - Your deposits, yields, and withdrawals remain private
2. **Yield Optimization** - Automated allocation across Aave, Lido, and Uniswap
3. **Compliance Ready** - KYC verification without identity exposure
4. **Fully Decentralized** - No central authority controls your funds

---

## Quick Start

### For Users (Yield Seekers)

1. **Connect Wallet** → Connect your Web3 wallet (MetaMask, RainbowKit)
2. **Complete KYC** → Verify identity once, generate zero-knowledge proof
3. **Deposit Funds** → Deposit ETH or tokens with private ZK proof
4. **Earn Yields** → Automatically allocated to best-performing strategies
5. **Withdraw Anytime** → Withdraw with full privacy maintained

[Go to User Guide →](./core-flow/user-flow/wallet-connection)

### For Admins

1. **Manage Strategies** → Add/remove DeFi protocols
2. **Allocate Funds** → Distribute vault assets across strategies
3. **Harvest Yields** → Collect yields from all protocols
4. **Monitor KYC** → Manage compliance without seeing user data

[Go to Admin Guide →](./core-flow/admin-flow/manage-strategies)

---

## Key Features

:::tip Privacy-Preserving
All transactions use **ZK-SNARK proofs** to hide amounts, addresses, and transaction details while remaining verifiable on-chain.
:::

### 🔐 Zero-Knowledge Architecture

- **KYC Verification Circuit** - Prove compliance without revealing identity
- **Balance Proof Circuit** - Prove sufficient funds without showing amounts
- **Circom Implementation** - Industry-standard ZK proof system

### 💰 Multi-Strategy Yield Optimization

- **Aave Strategy** - Lending protocol for stable yields
- **Lido Strategy** - Liquid staking for ETH staking rewards
- **Uniswap Strategy** - Liquidity provision for trading fees

### 🎯 Smart Allocation

- **Automated Rebalancing** - Dynamically shift funds to best yields
- **Risk Assessment** - Evaluate protocol safety before allocation
- **Gas Optimization** - Batch operations to minimize fees

---

## Current MVP Status

### ✅ Implemented Features

- ✅ Multi-strategy vault architecture (`StrategyVaultV2_Multi`)
- ✅ KYC compliance system (`ComplianceManagerV2`)
- ✅ ZK circuit design (KYC + Balance proofs)
- ✅ Mock strategy implementations (Aave, Lido, Uniswap)
- ✅ Frontend with RainbowKit wallet integration
- ✅ Admin dashboard for strategy management
- ✅ Deployed on Mantle Sepolia testnet

### 🔄 Upcoming Features (Post-MVP)

- 🔄 Additional DeFi protocols (Compound, Curve, Balancer)
- 🔄 Advanced ZK circuits (shielded transactions)
- 🔄 Governance token and DAO
- 🔄 Mainnet deployment with audit
- 🔄 Mobile application
- 🔄 Cross-chain support

---

## Architecture at a Glance

```
┌─────────────────────────────────────────────┐
│         ZK-Yield Protocol                   │
├─────────────────────────────────────────────┤
│                                             │
│  Frontend (Next.js)                         │
│       ↓                                     │
│  StrategyVaultV2 ──→ DeFi Strategies        │
│       ↓                 • Aave (lending)    │
│  ZK Verifier            • Lido (staking)    │
│       ↓                 • Uniswap (LP)      │
│  ComplianceV2 (KYC)                         │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Learn More

Dive deeper into ZK-Yield:

- [**Overview**](./introduction/overview) - Understand the protocol architecture
- [**Core Concepts**](./core-concepts/key-concepts-definitions/yield-aggregation) - Learn fundamental concepts
- [**ZK Circuits**](./zk-circuits/introduction) - Explore zero-knowledge implementation
- [**Smart Contracts**](./smart-contracts/overview) - Review contract architecture
- [**Developer Guide**](./developer-guide/quick-start) - Start building

---

## Why ZK-Yield Matters

Traditional DeFi exposes all your financial activities on-chain:

- 👁️ Everyone can see your balance
- 👁️ All transactions are public
- 👁️ Your investment strategy is visible
- 👁️ Privacy = Zero

**ZK-Yield changes this**:

- 🔐 Balance hidden with zero-knowledge proofs
- 🔐 Transaction amounts private
- 🔐 Strategy allocation confidential
- 🔐 Only you see your data

**Plus, you still get**:

- ✅ Optimized yields across protocols
- ✅ Automated strategy allocation
- ✅ Full on-chain verification
- ✅ Regulatory compliance

---

## Technology Stack

- **Smart Contracts**: Solidity, Foundry, OpenZeppelin
- **ZK Proofs**: Circom, SnarkJS
- **Frontend**: Next.js 16, React, TypeScript
- **Web3**: Wagmi, Viem, RainbowKit
- **Blockchain**: Mantle Sepolia Testnet

---

## Get Started Now

Ready to experience privacy-preserving DeFi yields?

👉 [**Try the Demo**](https://zk-yield.vercel.app)  
👉 [**Read the Docs**](./introduction/overview)  
👉 [**Join Community**](./support/community)

---

_Built with ❤️ for the future of private DeFi_
