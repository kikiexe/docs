---
title: Modular Strategies
sidebar_position: 4
---

# Modular Strategies

Veilfi's architecture is **modular and extensible**, allowing new yield strategies to be added without disrupting existing users or requiring contract redeployment.

## Modular Design

### Strategy Interface

All strategies implement standardized interface:

```solidity
interface IStrategy {
    function deposit(uint256 amount) external;
    function withdraw(uint256 amount) external;
    function harvest() external returns (uint256 yield);
    function totalAssets() external view returns (uint256);
    function apy() external view returns (uint256);
}
```

### Adding New Strategies

Admin can integrate new protocols:

```solidity
contract StrategyVaultV2 {
    IStrategy[] public strategies;

    function addStrategy(address newStrategy) external onlyOwner {
        require(IStrategy(newStrategy).apy() > 0, "Invalid strategy");
        strategies.push(IStrategy(newStrategy));
    }
}
```

**Example**: Launch with Aave + Lido → Later add Compound, Curve, Convex.

## Benefits of Modularity

### 1. Upgradability

Add new yield sources without migrating user funds:

```
Week 1: Aave + Lido (5% blended APY)
Week 4: + Uniswap added (7% blended APY)
Week 8: +  Compound added (8% blended APY)

Users' funds  seamlessly earn more as strategies expand
```

### 2. Risk Isolation

If one strategy fails, others unaffected:

```
Aave gets exploited → Pause Aave strategy
                     Lido + Uniswap continue operating
                     Users can still withdraw
```

### 3. Strategy Competition

Vault can rotate to best performers:

```
If Strategy A APY drops below threshold:
  → Remove from active allocation
  → Redirect capital to Strategy B
```

## Current Strategies

### Aave Strategy

- **Type**: Lending
- **APY**: 3-8%
- **Risk**: 🟢 Low

### Lido Strategy

- **Type**: ETH Staking
- **APY**: 4-5%
- **Risk**: 🟢 Low

### Uniswap Strategy

- **Type**: Liquidity Provision
- **APY**: 10-30%
- **Risk**: 🟡 Medium (IL risk)

## Future Strategies (Roadmap)

- Compound V3
- Curve Finance
- Convex Finance
- Beefy Auto-Compounding
- GMX Perpetuals

---

**Next**: [Yield Model Overview](../yield-model-overview/how-aggregation-works)
