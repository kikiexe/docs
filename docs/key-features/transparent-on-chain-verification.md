---
title: Transparent On-Chain Verification
sidebar_position: 5
---

# Transparent On-Chain Verification

All Veilfi operations are verifiable on-chain while preserving user privacy.

## What's Verifiable

### ✅ Vault State

```javascript
// Anyone can query:
totalAssets(); // Total TVL
totalSupply(); // Total shares
pricePerShare(); // Current share value
getStrategyAllocs(); // Where funds deployed
```

### ✅ Transaction History

All deposits, withdrawals, harvests visible on Mantle Sepolia Explorer.

### ✅ Smart Contract Code

All contracts verified and open source:

```
StrategyVaultV2_Multi.sol    ✅ Verified
ComplianceManagerV2.sol      ✅ Verified
Aave/Lido/Uniswap Strategies ✅ Verified
```

## Privacy Balance

**Public**: Vault-level metrics (TVL, APY, allocations)  
**Private**: Individual amounts (with ZK proofs)

## Trust Minimization

- No admin keys for user funds
- Immutable core logic
- Time-locked configuration changes

---

**Congratulations!** Key Features section complete.

**Next**: [Technical Details](../smart-contracts/overview)
