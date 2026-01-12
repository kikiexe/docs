---
title: Yield Harvest Cycle
sidebar_position: 2
---

# Yield Harvest Cycle

The yield harvest cycle collects earnings from all strategies and compounds them back into the vault, increasing share value for all users.

## Harvest Flow

### Step 1: Admin Triggers Harvest

```solidity
function harvestYields() external onlyOwner {
    uint256 totalYield = _harvestFromAllStrategies();

    // Deduct protocol fees
    uint256 netYield = _deductFees(totalYield);

    // Yields remain in vault, increasing totalAssets()
    emit YieldHarvested(totalYield, netYield);
}
```

### Step 2: Collect from Each Strategy

```solidity
function _harvestFromAllStrategies() internal returns (uint256) {
    uint256 totalYield = 0;

    for (uint i = 0; i < strategies.length; i++) {
        try strategies[i].harvest() returns (uint256 strategyYield) {
            totalYield += strategyYield;
            emit StrategyHarvested(i, strategyYield);
        } catch {
            emit StrategyHarvestFailed(i);
        }
    }

    return totalYield;
}
```

### Step 3: Strategy-Specific Harvesting

**Aave Strategy**:

```solidity
function harvest() external override returns (uint256) {
    // Aave accrues interest in aTokens
    uint256 currentBalance = aToken.balanceOf(address(this));
    uint256 yield = currentBalance - totalDeposited;

    // Withdraw yield only
    aavePool.withdraw(WETH, yield, msg.sender);

    return yield;
}
```

**Lido Strategy**:

```solidity
function harvest() external override returns (uint256) {
    // stETH rebases daily (balance increases)
    uint256 currentStETH = stETH.balanceOf(address(this));
    uint256 yield = currentStETH - totalDeposited;

    // Swap stETH → ETH
    uint256 ethReceived = _swapStETHToETH(yield);
    payable(msg.sender).transfer(ethReceived);

    return ethReceived;
}
```

**Uniswap Strategy**:

```solidity
function harvest() external override returns (uint256) {
    // Collect trading fees from LP position
    (uint256 amount0, uint256 amount1) = positionManager.collect(
        INonfungiblePositionManager.CollectParams({
            tokenId: tokenId,
            recipient: msg.sender,
            amount0Max: type(uint128).max,
            amount1Max: type(uint128).max
        })
    );

    return amount0 + _convertUSDCToETH(amount1);
}
```

## Fee Deduction

### Management Fee (1% Annual)

Calculated pro-rata for harvest period:

```solidity
function _deductManagementFee(uint256 yield, uint256 daysSinceLastHarvest)
    internal returns (uint256)
{
    // 1% annual = 0.0027% daily
    uint256 dailyRate = 27; // basis points per day
    uint256 feeRate = dailyRate * daysSinceLastHarvest;

    uint256 fee = yield * feeRate / 1000000;
    protocolFees += fee;

    return yield - fee;
}
```

### Performance Fee (10% of Profits)

```solidity
function _deductPerformanceFee(uint256 profit) internal returns (uint256) {
    uint256 fee = profit * 1000 / 10000; // 10%
    protocolFees += fee;
    return profit - fee;
}
```

## Compounding Effect

### Auto-Reinvestment

Harvested yields stay in vault:

```
Week 0: Vault has 1000 ETH
Week 1: Harvest 5 ETH → totalAssets = 1005 ETH
Week 2: Harvest on 1005 ETH → 5.025 ETH
Week 3: Harvest on 1010.025 ETH → 5.05 ETH
...
Week 52: Vault has ~1072 ETH (7.2% APY with compounding)
```

### Share Price Appreciation

Users benefit through share value increase:

```solidity
// Before harvest
totalAssets: 1000 ETH
totalShares: 900
sharePrice: 1000/900 = 1.111 ETH

// After harvesting 5 ETH
totalAssets: 1005 ETH
totalShares: 900 (unchanged)
sharePrice: 1005/900 = 1.117 ETH (+0.54%)
```

## Harvest Frequency

### Time-Based Schedule

Weekly harvests optimize gas vs rewards:

```solidity
uint256 public lastHarvestTime;
uint256 public constant MIN_HARVEST_INTERVAL = 7 days;

modifier canHarvest() {
    require(
        block.timestamp >= lastHarvestTime + MIN_HARVEST_INTERVAL,
        "Too soon to harvest"
    );
    _;
}

function harvestYields() external onlyOwner canHarvest {
    lastHarvestTime = block.timestamp;
    _harvestFromAllStrategies();
}
```

### Event-Based Triggers

Harvest when yields exceed threshold:

```solidity
function shouldHarvest() public view returns (bool) {
    uint256 pendingYields = _calculatePendingYields();
    uint256 harvestCost = 500000 * tx.gasprice; // ~500k gas

    // Only harvest if yield > 2x gas cost
    return pendingYields > harvestCost * 2;
}
```

## Gas Optimization

### Batch Harvesting

Single transaction for all strategies:

```
❌ Bad: 3 separate harvest transactions
Gas cost: 3 × 150k = 450k gas

✅ Good: 1 batch harvest transaction
Gas cost: ~350k gas (22% savings)
```

### Skip Failed Harvests

```solidity
for (uint i = 0; i < strategies.length; i++) {
    try strategies[i].harvest() returns (uint256 yield) {
        totalYield += yield;
    } catch {
        // Skip failed strategy, continue with others
        continue;
    }
}
```

---

**Next**: [Withdrawal Process](./withdrawal-process)
