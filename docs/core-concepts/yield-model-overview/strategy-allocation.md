---
title: Strategy Allocation
sidebar_position: 3
---

# Strategy Allocation

Veilfi allocates capital across multiple DeFi strategies using a **risk-adjusted, performance-optimized model** to maximize returns while controlling downside risk.

## Current Allocation Model

### Static 40/30/30 Split

| Strategy    | Allocation | Rationale                         |
| ----------- | ---------- | --------------------------------- |
| **Aave**    | 40%        | Highest safety, consistent 5% APY |
| **Lido**    | 30%        | ETH staking rewards, 4.5% APY     |
| **Uniswap** | 30%        | Higher yield (12%), but IL risk   |

**Total Weighted APY**: ~7%

### Why This Split?

**40% Aave** (Largest):

- Battle-tested protocol ($10B+ TVL)
- Lowest risk
- Consistent yields
- High liquidity for withdrawals

**30% Lido** (Medium):

- Ethereum staking (network-level security)
- Predictable 4-5% APY
- Low smart contract risk

**30% Uniswap** (Smallest):

- Highest APY potential (10-30%)
- Impermanent loss risk
- Volatile yields
- Limited to 30% for risk control

## Allocation Algorithm

### Current: Manual Rebalancing

Admin monitors and adjusts weekly:

```solidity
function rebalance() external onlyOwner {
    // Withdraw from all strategies
    for (uint i = 0; i < strategies.length; i++) {
        strategies[i].withdrawAll();
    }

    // Reallocate based on new percentages
    uint256 total = address(this).balance;
    aaveStrategy.deposit(total * newAllocation[0] / 100);
    lidoStrategy.deposit(total * newAllocation[1] / 100);
    uniswapStrategy.deposit(total * newAllocation[2] / 100);
}
```

**Decision Factors**:

1. Current APYs (shift to higher yields)
2. Risk events (reduce exposure if exploit detected)
3. Liquidity needs (maintain withdrawal capacity)
4. Gas costs (avoid frequent small rebalances)

### Future: Automated Dynamic Allocation

Algorithm-driven optimization:

```solidity
function dynamicAllocate() external {
    // Get current APYs
    uint256 aaveAPY = aaveStrategy.apy();
    uint256 lidoAPY = lidoStrategy.apy();
    uint256 uniAPY = uniswapStrategy.apy();

    // Risk-adjusted scores
    uint256 aaveScore = aaveAPY * 100 / riskScore[AAVE];
    uint256 lidoScore = lidoAPY * 100 / riskScore[LIDO];
    uint256 uniScore = uniAPY * 100 / riskScore[UNI];

    // Allocate proportionally to scores
    uint256 totalScore = aaveScore + lidoScore + uniScore;
    allocations[AAVE] = aaveScore * 100 / totalScore;
    allocations[LIDO] = lidoScore * 100 / totalScore;
    allocations[UNI] = uniScore * 100 / totalScore;
}
```

**Benefit**: Automatic optimization based on market conditions.

## Risk Management

### Diversification Limits

Never allocate >50% to single strategy:

```solidity
require(allocation <= MAX_ALLOCATION, "Too concentrated");
```

**Reason**: If protocol exploited, max 50% loss (not 100%).

### Strategy Health Monitoring

Pause allocations if risk detected:

```solidity
modifier strategyHealthy(uint idx) {
    require(!strategies[idx].isPaused(), "Strategy paused");
    require(strategies[idx].totalDebt() < limits[idx], "Debt too high");
    _;
}
```

## Rebalancing Triggers

### Time-Based

Rebalance every 7 days regardless of conditions:

```
Weekly schedule: Every Monday 00:00 UTC
Purpose: Maintain target allocations
```

### Event-Based

Immediate rebalancing if:

1. **APY Delta > 5%**:

   ```
   If Uniswap APY jumps from 12% → 20%:
   → Increase Uniswap allocation from 30% → 40%
   ```

2. **Risk Event**:

   ```
   If Aave has exploit rumor:
   → Reduce Aave allocation from 40% → 20%
   → Increase safer strategies
   ```

3. **Liquidity Needed**:
   ```
   If large withdrawal request:
   → Withdraw from most liquid strategy first
   ```

## Performance Tracking

### Strategy Rankings

Track historical performance:

| Strategy | 7-Day APY | 30-Day APY | Risk Score | Rank |
| -------- | --------- | ---------- | ---------- | ---- |
| Uniswap  | 15%       | 12%        | 7/10       | 1st  |
| Aave     | 5.2%      | 5.0%       | 2/10       | 2nd  |
| Lido     | 4.5%      | 4.5%       | 3/10       | 3rd  |

**Action**: Gradually shift allocation to top performers.

### Rebalancing History

Public transparency:

```solidity
struct RebalanceEvent {
    uint256 timestamp;
    uint256[3] oldAllocations;
    uint256[3] newAllocations;
    string reason;
}

RebalanceEvent[] public rebalanceHistory;
```

**Users can audit**: Why and when allocations changed.

## Gas Optimization

### Minimize Rebalancing Frequency

```
Cost of rebalancing: ~$50-100 in gas
Benefit threshold: Must gain >$100 in  extra yield

Only rebalance if: expectedGain > gasCost * 2
```

### Batch Operations

Combine multiple actions:

```solidity
function harvestAndRebalance() external onlyOwner {
    // 1. Harvest yields (one transaction)
    harvestYields();

    // 2. Reallocate (same transaction)
    rebalance();

    // Saves ~40% gas vs. separate calls
}
```

---

**Congratulations!** You've completed the **Core Concepts** section.

**Next Steps**:

- [Protocol Design](../../protocol-design/architecture-overview/core-vault-layer) - Deep dive into technical architecture
- [DeFi Strategies](../../defi-strategies/overview) - Learn about individual yield strategies
