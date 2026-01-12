---
title: Smart Contracts Overview
sidebar_position: 1
---

# Smart Contracts Overview

Veilfi's smart contract architecture consists of modular, auditable contracts deployed on Mantle Sepolia Testnet.

## Contract Architecture

```
┌──────────────────────────────────────┐
│      StrategyVaultV2_Multi           │
│   (Main vault - ERC-4626)            │
└──────────────┬───────────────────────┘
               ↓
    ┌──────────┴──────────┐
    ↓                     ↓
┌─────────────────┐  ┌─────────────────┐
│ ComplianceV2    │  │  ZK Verifier    │
│ (KYC Manager)   │  │  (Groth16)      │
└─────────────────┘  └─────────────────┘
               ↓
    ┌──────────┼──────────┐
    ↓          ↓          ↓
┌─────────┬─────────┬─────────┐
│  Aave   │  Lido   │Uniswap  │
│Strategy │Strategy │Strategy │
└─────────┴─────────┴─────────┘
```

## Core Contracts

### StrategyVaultV2_Multi

**Purpose**: Main vault managing user deposits and strategy allocation

**Key Functions**:

- `deposit()` - Accept ETH deposits
- `withdraw()` - Redeem shares for ETH
- `allocateToStrategies()` - Distribute capital
- `harvestYields()` - Collect earnings

**Standard**: ERC-4626 tokenized vault

### ComplianceManagerV2

**Purpose**: ZK-KYC verification management

**Key Functions**:

- `submitKYCProof()` - Submit ZK proof of KYC
- `isKYCVerified()` - Check verification status

### Strategy Contracts

Each strategy implements `IStrategy` interface:

```solidity
interface IStrategy {
    function deposit() external payable returns (uint256);
    function withdraw(uint256 amount) external returns (uint256);
    function harvest() external returns (uint256);
    function totalAssets() external view returns (uint256);
    function apy() external view returns (uint256);
}
```

## Deployment Details

**Network**: Mantle Sepolia Testnet  
**Chain ID**: 5003  
**Explorer**: https://explorer.sepolia.mantle.xyz

**Contracts** (example addresses):

```
StrategyVaultV2_Multi: 0x...
ComplianceManagerV2:   0x...
MockAaveStrategy:      0x...
MockLidoStrategy:      0x...
MockUniswapStrategy:   0x...
```

## Security Features

✅ **ReentrancyGuard** - All external functions protected  
✅ **Ownable** - Admin functions restricted  
✅ **Pausable** - Emergency stop mechanism  
✅ **Access Control** - Role-based permissions

---

**Next**: [StrategyVaultV2](./core-contracts/strategy-vault-v2) - Core vault implementation
