---
title: Overview
sidebar_position: 2
---

# Overview

## What is Veilfi?

**Veilfi** is a privacy-preserving yield aggregator that enables users to earn yield across multiple DeFi strategies while maintaining complete financial privacy through Zero-Knowledge proofs. The protocol operates on Mantle blockchain and aggregates yield from battle-tested protocols like Aave, Lido, and Uniswap.

## 1-Minute Protocol Flow

### Problem → Solution → Flow

**Problem**: DeFi protocols offer attractive yields but force radical transparency → Every transaction is public

**Veilfi's Solution**: Privacy layer + Multi-strategy aggregation = Private yield earning

**How It Works**:

1. **User deposits funds** ($1,000) → Enters shared anonymity pool
2. **Optional KYC via ZK proof** → Compliance without identity exposure
3. **Vault allocates to strategies** → 40% Aave, 30% Lido, 30% Uniswap
4. **Strategies earn yield** → From multiple DeFi protocols simultaneously
5. **Privacy preserved** → ZK proofs verify ownership without revealing amounts
6. **User withdraws** → Anonymously with cryptographic proof of shares

**Privacy Guarantee**: Deposit amounts, balances, and withdrawal values remain private to outsiders.

## Core Mechanism

The protocol implements a **privacy-first vault model** where:

- Users deposit into a shared vault creating an anonymity set
- Funds are strategically allocated across multiple yield sources
- Zero-Knowledge circuits verify user actions without revealing sensitive data
- KYC compliance is achieved through cryptographic proofs, not data storage

## Key Components

### Privacy Layer (ZK Circuits)

The privacy foundation using Circom-based ZK-SNARKs:

- **KYC Verification Circuit**: Proves compliance status without revealing identity
- **Balance Proof Circuit**: Demonstrates sufficient balance without exposing amounts
- **Ownership Proof**: Verifies vault share ownership anonymously

### Strategy Vault (StrategyVaultV2)

The core contract managing all deposits and allocations:

- Accepts deposits with optional ZK proofs for enhanced privacy
- Issues proportional shares to depositors
- Allocates capital across multiple DeFi strategies
- Processes withdrawals with privacy protection
- Verifies all ZK proofs on-chain

### Compliance Manager (ComplianceManagerV2)

Privacy-preserving KYC system:

- Stores only cryptographic proof hashes (not personal data)
- Enables regulatory compliance without sacrificing privacy
- Allows users to prove KYC status anonymously
- Supports institutional adoption with compliant privacy

### Multi-Strategy Engine

Diversified yield generation across protocols:

| Strategy    | Protocol     | Type                | Target APY |
| ----------- | ------------ | ------------------- | ---------- |
| **Aave**    | Aave V3      | Lending             | 3-8%       |
| **Lido**    | Lido Finance | ETH Staking         | 4-5%       |
| **Uniswap** | Uniswap V3   | Liquidity Provision | 10-30%\*   |

\*_Variable based on pool fees and volume_

## Technical Implementation

### Smart Contract Architecture

```solidity
StrategyVaultV2_Multi (Core Vault)
├── deposit() / depositWithProof()
├── withdraw(shares)
├── allocateToStrategies() [Admin]
└── harvestYields() [Admin]

ComplianceManagerV2 (KYC Manager)
├── verifyKYC(proof)
└── isCompliant(user)

Strategies (Yield Generators)
├── MockAaveStrategy
├── MockLidoStrategy
└── MockUniswapStrategy
```

### Network Deployment

- **Blockchain**: Mantle Sepolia Testnet
- **Chain ID**: 5003
- **Explorer**: https://explorer.sepolia.mantle.xyz

### ZK Circuit Stack

- **Framework**: Circom + SnarkJS
- **Proof System**: Groth16
- **Trusted Setup**: Powers of Tau ceremony
- **Verification**: On-chain Solidity verifiers

## MVP Status (Hackathon Version)

### ✅ What's Live Now

- Multi-strategy vault with 3 protocols (Aave, Lido, Uniswap)
- ZK-SNARK circuits for KYC and balance verification
- Privacy-preserving deposit/withdrawal flows
- Admin dashboard for strategy management
- Smart contract deployment on Mantle Sepolia

### 🔄 Planned Enhancements

- Dynamic rebalancing algorithm
- More DeFi strategy integrations
- Advanced privacy features (stealth addresses)
- Gas optimization for proof verification
- Mainnet deployment with audit

## Key Features

### Capital Efficiency

- **Single deposit, multiple yields**: One transaction earns from 3+ protocols
- **Gas savings**: Batch allocations instead of individual strategy deposits
- **Optimized capital**: Smart rebalancing maximizes returns

### Security Model

- **Privacy by Design**: ZK proofs instead of trusted intermediaries
- **Non-custodial**: Users maintain control of funds
- **Strategy diversification**: Risk spread across protocols
- **Transparent verification**: Anyone can verify proofs without seeing amounts

### Transparency

- **Open source**: All contracts and circuits are public
- **Verifiable yields**: On-chain proof of returns
- **Auditable privacy**: ZK proofs can be verified by anyone
- **Real-time monitoring**: Total TVL and allocations are visible

## Technology Stack

### Smart Contracts

- **Language**: Solidity 0.8.20
- **Framework**: Foundry
- **Standards**: ERC-4626 (Vault), ERC-20 (Shares)
- **Testing**: Comprehensive Foundry test suite

### Frontend

- **Framework**: Next.js 14
- **Wallet**: RainbowKit + Wagmi
- **Styling**: TailwindCSS
- **Charts**: Recharts for yield visualization

### Network Infrastructure

- **Deployment**: Mantle Sepolia (Testnet)
- **RPC**: Mantle RPC endpoints
- **Fallback**: Ankr/Infura for reliability

## Project Goals

### Primary Objectives

1. **Prove privacy + yield are compatible**: DeFi doesn't require full transparency
2. **Showcase ZK-SNARKs in production**: Practical privacy implementation
3. **Enable compliant privacy**: KYC without data exposure
4. **Optimize yield aggregation**: Multi-strategy beats single protocol

### Success Criteria

**For Users**:

- Earn competitive yields (5-15% APY)
- Maintain complete financial privacy
- Simple UX (wallet connect → deposit → earn)

**For Institutions**:

- Regulatory compliance via ZK-KYC
- Privacy for treasury operations
- Professional-grade security

**For Developers**:

- Open-source reference implementation
- Reusable ZK circuits
- Integration-friendly APIs

---

**Next Steps**: Learn about [why Veilfi exists](./why-zk-yield-exists/problem-space) or jump to [who should use it](./who-is-this-for/privacy-conscious-users).
