---
title: How Aggregation Works
sidebar_position: 1
---

# How Aggregation Works

Veilfi's yield aggregation automatically distributes user deposits across multiple DeFi protocols to maximize returns and minimize risk.

## The Aggregation Flow

### Step 1: User Deposits

```
User deposits 10 ETH to Veilfi vault
          ↓
Vault mints shares proportional to deposit
          ↓
Share price: totalAssets / totalShares
```

### Step 2: Capital Allocation

Admin allocates pooled capital to strategies:

```solidity
function allocateToStrategies() external onlyOwner {
    uint256 total = totalAssets();

    // 40/30/30 split
    aaveStrategy.deposit(total * 40 / 100);    // 4 ETH
    lidoStrategy.deposit(total * 30 / 100);    // 3 ETH
    uniswapStrategy.deposit(total * 30 / 100); // 3 ETH
}
```

**Result**: Single user deposit → diversified across 3 protocols.

### Step 3: Yield Generation

Each strategy earns independently:

| Strategy  | Allocated  | APY     | Monthly Yield |
| --------- | ---------- | ------- | ------------- |
| Aave      | 4 ETH      | 5%      | 0.0167 ETH    |
| Lido      | 3 ETH      | 4.5%    | 0.0113 ETH    |
| Uniswap   | 3 ETH      | 12%     | 0.0300 ETH    |
| **Total** | **10 ETH** | **~7%** | **0.058 ETH** |

### Step 4: Yield Harvesting

Admin collects yields periodically:

```solidity
function harvestYields() external onlyOwner {
    for (uint i = 0; i < strategies.length; i++) {
        uint256 yield = strategies[i].harvest();
        totalYieldEarned += yield;
    }
    // Yields reinvested or distributed
}
```

### Step 5: Share Price Appreciation

As yields accumulate, share value increases:

```
Initial: 100 shares = 100 ETH → 1 share = 1  ETH
Month 1: 100 shares = 100.58 ETH → 1 share = 1.0058 ETH
Month 12: 100 shares = 107 ETH → 1 share = 1.07 ETH

User's 100 shares now worth 107 ETH (+7%)
```

## Why Aggregation > Single Protocol

### Comparison

**Single Protocol** (Aave only):

```
10 ETH → Aave (5% APY)
Annual Return: 0.5 ETH
```

**Aggregated** (Veilfi):

```
4 ETH → Aave (5% APY) = 0.2 ETH
3 ETH → Lido (4.5% APY) = 0.135 ETH
3 ETH → Uniswap (12% APY) = 0.36 ETH
────────────────────────────────────
Annual Return: 0.695 ETH (+39% more!)
```

### Risk Diversification

**Single Point of Failure**:

```
10 ETH in Aave → Aave exploit → Lose 100%
```

**Diversified Risk**:

```
4 ETH in Aave, 3 ETH in Lido, 3 ETH in Uniswap
→ Aave exploit → Lose only 40%
→ Remaining 60% safe in other protocols
```

## Allocation Strategies

### Current: Static Allocation

Fixed percentages (40/30/30):

**Pros**: Simple, predictable  
**Cons**: Doesn't adapt to market

### Future: Dynamic Allocation

Algorithm-driven rebalancing:

```solidity
function dynamicRebalance() external {
    uint256[] memory apys = getStrategyAPYs();

    // Allocate more to higher APY
    for (uint i = 0; i < strategies.length; i++) {
        allocations[i] = apys[i] / sum(apys) * 100;
    }
}
```

**Benefit**: Auto-optimize for maximum yield.

---

**Next**: [How Yields are Distributed](./how-yields-are-distributed)
