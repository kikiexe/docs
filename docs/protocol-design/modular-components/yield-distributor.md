---
title: Yield Distributor
sidebar_position: 4
---

# Yield Distributor

The **Yield Distributor** manages yield collection from strategies and distribution to vault shareholders through share price appreciation.

## Distribution Model

### Share-Based System

```solidity
// Yields increase share price
sharePrice = totalAssets() / totalShares()

// User value = shares × sharePrice
userValue = balanceOf(user) * sharePrice
```

### Harvest Function

```solidity
function harvestYields() external onlyOwner {
    uint256 totalYield = 0;

    // Collect from all strategies
    for (uint i = 0; i < strategies.length; i++) {
        uint256 strategyYield = strategies[i].harvest();
        totalYield += strategyYield;
     }

    // Yields automatically increase totalAssets()
    // Share price appreciates proportionally
    emit YieldHarvested(totalYield);
}
```

## Fee Structure

### Management Fee (1% Annual)

```solidity
uint256 public constant MANAGEMENT_FEE = 100; // 1% in basis points

function _deductManagementFee(uint256 yield) internal returns (uint256) {
    uint256 fee = yield * MANAGEMENT_FEE / 10000;
    protocolFees += fee;
    return yield - fee;
}
```

### Performance Fee (10% of Profits)

```solidity
uint256 public constant PERFORMANCE_FEE = 1000; // 10% in basis points

function _deductPerformanceFee(uint256 profit) internal returns (uint256) {
    uint256 fee = profit * PERFORMANCE_FEE / 10000;
    protocolFees += fee;
    return profit - fee;
}
```

## Auto-Compounding

Yields reinvested automatically:

```solidity
function harvestYields() external onlyOwner {
    uint256 grossYield = _collectFromStrategies();

    // Deduct fees
    uint256 netYield = _deductFees(grossYield);

    // Reinvest (increases totalAssets, share price rises)
    allocateToStrategies();
}
```

**Benefit**: Users earn compound interest without manual action.

---

**Next**: [Capital Flow Model](../capital-flow-model/deposit-allocation)
