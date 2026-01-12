---
title: Strategies Overview
sidebar_position: 1
---

# DeFi Strategies Overview

ZK-Yield optimizes yields by automatically allocating funds across multiple **DeFi strategies**. This page explains how our multi-strategy approach works.

## Why Multi-Strategy?

### Single Protocol Limitations

| Issue                       | Impact                                     |
| --------------------------- | ------------------------------------------ |
| **Single Point of Failure** | If protocol gets hacked, all funds at risk |
| **Volatile APY**            | Yields fluctuate with market conditions    |
| **Limited Upside**          | Can't capitalize on better opportunities   |
| **Capital Inefficiency**    | Funds locked in suboptimal positions       |

### Multi-Strategy Benefits

✅ **Risk Diversification** - Spread across protocols  
✅ **Yield Optimization** - Always capturing best rates  
✅ **Dynamic Rebalancing** - Shift to better performers  
✅ **Protocol Resilience** - Survive individual protocol issues

---

## Supported Strategies

ZK-Yield currently supports **three core strategies**:

### 1. 🏦 Aave Strategy (Lending)

**Protocol**: Aave V3  
**Type**: Lending & Borrowing  
**Risk**: Low  
**APY**: 3-8%

**How it works**:

- Deposit assets into Aave lending pools
- Earn interest from borrowers
- Receive aToken rewards
- Low-risk, stable yields

**Parameters**:

- **Max Allocation**: 40% of vault
- **Assets**: ETH, USDC, USDT
- **Liquidation Risk**: None (we're lenders)

### 2. 🌊 Lido Strategy (Liquid Staking)

**Protocol**: Lido Finance  
**Type**: ETH Staking  
**Risk**: Low-Medium  
**APY**: 4-5%

**How it works**:

- Stake ETH through Lido
- Receive stETH (liquid staking token)
- Earn staking rewards
- Maintain liquidity with stETH

**Parameters**:

- **Max Allocation**: 50% of vault
- **Assets**: ETH only
- **Lock Period**: None (liquid)

### 3. 🦄 Uniswap Strategy (Liquidity Provision)

**Protocol**: Uniswap V3  
**Type**: AMM Liquidity  
**Risk**: Medium-High  
**APY**: 10-30%

**How it works**:

- Provide liquidity to trading pairs
- Earn trading fees (0.3%)
- Concentrated liquidity for efficiency
- Higher yields, higher risk (impermanent loss)

**Parameters**:

- **Max Allocation**: 30% of vault
- **Pairs**: ETH/USDC, ETH/USDT
- **Range**: ±10% from current price

---

## Allocation Algorithm

### Dynamic Allocation

Our algorithm considers multiple factors:

```javascript
function calculateAllocation() {
  factors = {
    currentAPY: 40%,      // Weight on current yield
    historicalAPY: 20%,   // Weight on past performance
    risk: 25%,            // Weight on risk score
    liquidity: 15%        // Weight on protocol liquidity
  }

  // Calculate weighted score for each strategy
  score = Σ (factor × weight)

  // Allocate proportionally
  allocation = score / totalScore
}
```

### Example Allocation

Current market conditions:

- **Aave**: 5% APY, Low risk → 40% allocation
- **Lido**: 4.5% APY, Low risk → 35% allocation
- **Uniswap**: 15% APY, Medium risk → 25% allocation

Total expected yield: **~7.5% APY**

---

## Strategy Lifecycle

### 1. Deposit Phase

```solidity
// User deposits to vault
vault.deposit{value: 1 ether}();

// Funds sit in vault until admin allocates
```

### 2. Allocation Phase

```solidity
// Admin allocates to strategies
vault.allocateToStrategies();

// Vault distributes funds:
// 40% → Aave
// 35% → Lido
// 25% → Uniswap
```

### 3. Earning Phase

Each strategy earns yield:

- **Aave**: Accrues aToken balance
- **Lido**: Receives staking rewards
- **Uniswap**: Collects trading fees

### 4. Harvest Phase

```solidity
// Admin harvests yields
vault.harvestYields();

// Collected from all strategies
// Compounded back into vault
```

### 5. Rebalance Phase

```solidity
// If allocation drifts from target
vault.rebalanceStrategies();

// Moves funds to maintain optimal allocation
```

### 6. Withdrawal Phase

```solidity
// User withdraws shares
vault.withdraw(shares);

// Vault liquidates from strategies if needed
// Prioritizes: Aave → Lido → Uniswap
```

---

## Risk Management

### Position Limits

| Strategy          | Max %   | Safety Reserve            |
| ----------------- | ------- | ------------------------- |
| Aave              | 40%     | Very safe                 |
| Lido              | 50%     | Safe                      |
| Uniswap           | 30%     | Higher risk               |
| **Vault Reserve** | **10%** | **Emergency withdrawals** |

### Risk Metrics

We monitor:

- **TVL** - Total Value Locked in each protocol
- **APY Volatility** - Stability of returns
- **Smart Contract Risk** - Audit status
- **Liquidity Depth** - Ability to exit positions

### Emergency Procedures

In case of protocol issues:

1. **Pause deposits** to affected strategy
2. **Withdraw all funds** from risky protocol
3. **Redistribute** to safer strategies
4. **Notify users** via dashboard alerts

---

## Yield Calculations

### Individual Strategy Yields

```solidity
// Aave yield
aaveYield = (aTokenBalance - initialDeposit) / initialDeposit

// Lido yield
lidoYield = (stETHBalance - initialETH) / initialETH

// Uniswap yield
uniswapYield = feesCollected / liquidityProvided
```

### Total Vault Yield

```solidity
totalYield = Σ(strategyYield × allocationPercent)

// Example:
// Aave: 5% × 40% = 2%
// Lido: 4.5% × 35% = 1.575%
// Uniswap: 15% × 25% = 3.75%
// Total: 7.325% APY
```

### User Share Value

```solidity
sharePrice = totalVaultValue / totalShares

userValue = userShares × sharePrice
```

---

## Strategy Implementation

### Interface

All strategies implement:

```solidity
interface IStrategy {
    function deposit(uint256 amount) external;
    function withdraw(uint256 amount) external returns (uint256);
    function harvest() external returns (uint256);
    function balanceOf() external view returns (uint256);
    function estimatedAPY() external view returns (uint256);
}
```

### Aave Strategy Example

```solidity
contract AaveStrategy is IStrategy {
    ILendingPool public aavePool;
    IERC20 public aToken;

    function deposit(uint256 amount) external {
        // Deposit to Aave
        aavePool.deposit(asset, amount, address(this), 0);
    }

    function withdraw(uint256 amount) external returns (uint256) {
        // Withdraw from Aave
        return aavePool.withdraw(asset, amount, msg.sender);
    }

    function harvest() external returns (uint256) {
        // Claim rewards if any
        uint256 rewards = aaveIncentives.claimRewards();
        return rewards;
    }
}
```

---

## Performance Tracking

### Real-Time Metrics

Dashboard displays:

- **Current APY** per strategy
- **TVL** in each protocol
- **Yield generated** (24h, 7d, 30d)
- **Allocation percentages**
- **Risk scores**

### Historical Data

Track over time:

- APY trends
- Allocation changes
- Rebalancing events
- Harvest profits

---

## Future Strategies

### Planned Additions

1. **Compound Finance** - Alternative lending
2. **Curve Finance** - Stablecoin yields
3. **Balancer** - Weighted pool LPing
4. **GMX** - Perpetual trading fees
5. **Yearn Finance** - Strategy aggregation

### Selection Criteria

New strategies must have:

- ✅ **Audited contracts** (by reputable firms)
- ✅ **TVL > $100M** (proven product-market fit)
- ✅ **6+ months history** (battle-tested)
- ✅ **Active development** (not abandoned)
- ✅ **Clear documentation** (for integration)

---

## Strategy Management

### Admin Functions

```solidity
// Add new strategy
vault.addStrategy(strategyAddress, maxAllocation);

// Remove strategy
vault.removeStrategy(strategyAddress);

// Update allocation
vault.updateAllocation(strategyAddress, newPercentage);

// Emergency withdraw
vault.emergencyWithdraw(strategyAddress);
```

### Governance (Future)

Eventually, strategy management will be:

- 🗳️ **DAO-governed** (token holder votes)
- 📊 **Data-driven** (performance metrics)
- 🤖 **Automated** (rebalancing algorithms)

---

## Best Practices

### For Admins

1. **Monitor regularly** - Check APYs daily
2. **Rebalance quarterly** - Or when drift > 5%
3. **Harvest weekly** - Compound yields
4. **Review risks monthly** - Update risk scores
5. **Test withdrawals** - Ensure liquidity

### For Developers

1. **Test thoroughly** - Simulate edge cases
2. **Handle failures** - Graceful degradation
3. **Log everything** - Track all operations
4. **Optimize gas** - Batch transactions
5. **Monitor events** - Real-time alerts

---

## Next Steps

Explore individual strategies:

- [Aave Strategy](./supported-protocols/aave-strategy) - Lending implementation
- [Lido Strategy](./supported-protocols/lido-strategy) - Staking details
- [Uniswap Strategy](./supported-protocols/uniswap-strategy) - LP mechanics
- [Allocation Algorithm](./strategy-management/allocation-algorithm) - How we optimize
- [Rebalancing](./strategy-management/rebalancing) - When and how we rebalance

---

**Ready to dive deeper?** Pick a strategy to learn more!
