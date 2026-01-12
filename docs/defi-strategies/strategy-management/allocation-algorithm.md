---
title: Allocation Algorithm
sidebar_position: 1
---

# Allocation Algorithm

The allocation algorithm determines how capital is distributed across Veilfi's yield strategies to maximize risk-adjusted returns.

## Current Model: Static Allocation

### Fixed Percentages

```javascript
const ALLOCATIONS = {
  aave: 40, // 40% - Lowest risk, stable yields
  lido: 30, // 30% - Low risk, ETH staking
  uniswap: 30, // 30% - Medium risk, higher yields
};

function allocateCapital(totalAssets) {
  const allocations = {
    aave: totalAssets * 0.4,
    lido: totalAssets * 0.3,
    uniswap: totalAssets * 0.3,
  };

  return allocations;
}
```

### Rationale

**40% Aave** (Largest):

- Lowest risk profile (2/10)
- Most reliable liquidity
- Battle-tested protocol ($10B+ TVL)
- Base layer of safety

**30% Lido** (Medium):

- Very low risk (2/10)
- ETH staking rewards
- Liquid through stETH
- Network-level security

**30% Uniswap** (Smallest high-risk):

- Higher yields (15-30% APY)
- Impermanent loss risk
- Limited to 30% for risk control

### Smart Contract Implementation

```solidity
contract StrategyVaultV2_Multi {
    uint256[] public allocations = [40, 30, 30];  // Percentages
    IStrategy[] public strategies;

    function allocateToStrategies() external onlyOwner {
        uint256 totalAssets = address(this).balance;
        require(totalAssets > 0, "Nothing to allocate");

        // Keep 10% reserve for withdrawals
        uint256 reserveAmount = totalAssets * 10 / 100;
        uint256 allocatableAmount = totalAssets - reserveAmount;

        for (uint i = 0; i < strategies.length; i++) {
            uint256 amount = allocatableAmount * allocations[i] / 100;

            if (amount > 0) {
                strategies[i].deposit{value: amount}();
                emit FundsAllocated(i, amount);
            }
        }
    }
}
```

## Future Model: Dynamic Allocation

### Risk-Adjusted Returns

```javascript
function calculateOptimalAllocation(strategies) {
  const weights = strategies.map((s) => {
    // Calculate risk-adjusted score
    const riskAdjustedAPY = s.apy / (1 + s.riskScore);

    return {
      strategy: s.name,
      score: riskAdjustedAPY,
      maxAllocation: 50, // Max 50% per strategy
    };
  });

  // Normalize weights to sum to 100%
  const totalScore = weights.reduce((sum, w) => sum + w.score, 0);

  const allocations = weights.map((w) => ({
    strategy: w.strategy,
    allocation: Math.min((w.score / totalScore) * 100, w.maxAllocation),
  }));

  return allocations;
}
```

### Example Calculation

```
Current Market State:
├─ Aave:    APY 5%, Risk 2/10 → Score: 5/(1+0.2) = 4.17
├─ Lido:    APY 4.5%, Risk 2/10 → Score: 4.5/(1+0.2) = 3.75
└─ Uniswap: APY 18%, Risk 5/10 → Score: 18/(1+0.5) = 12.0

Total Score: 4.17 + 3.75 + 12.0 = 19.92

Dynamic Allocations:
├─ Aave:    (4.17/19.92) × 100 = 20.9%
├─ Lido:    (3.75/19.92) × 100 = 18.8%
└─ Uniswap: (12.0/19.92) × 100 = 60.2% → Capped at 50%

Final Allocations (after cap):
├─ Aave:    25%
├─ Lido:    25%
└─ Uniswap: 50%
```

## Allocation Constraints

### Hard Limits

```solidity
// Prevent over-concentration
uint256 public constant MAX_SINGLE_ALLOCATION = 50;  // 50%
uint256 public constant MIN_SINGLE_ALLOCATION = 10;   // 10%
uint256 public constant RESERVE_RATIO = 10;           // 10%

modifier validAllocation(uint256[] memory newAllocations) {
    uint256 sum = 0;

    for (uint i = 0; i < newAllocations.length; i++) {
        require(
            newAllocations[i] >= MIN_SINGLE_ALLOCATION,
            "Below minimum"
        );
        require(
            newAllocations[i] <= MAX_SINGLE_ALLOCATION,
            "Above maximum"
        );
        sum += newAllocations[i];
    }

    require(sum == 100, "Must sum to 100%");
    _;
}

function updateAllocations(uint256[] memory newAllocations)
    external
    onlyOwner
    validAllocation(newAllocations)
{
    allocations = newAllocations;
    emit AllocationsUpdated(newAllocations);
}
```

### Rationale for Limits

**Max 50%**: Limit blast radius if strategy fails  
**Min 10%**: Ensure meaningful diversification  
**10% Reserve**: Maintain liquidity for withdrawals

## Allocation Triggers

### Initial Allocation

```javascript
// When vault receives first deposits
if (totalAssets >= MINIMUM_THRESHOLD) {
  allocateToStrategies();
}

// Example threshold: 1 ETH minimum
const MINIMUM_THRESHOLD = ethers.utils.parseEther("1");
```

### Periodic Reallocation

```javascript
// Weekly reallocation check
const REALLOCATION_INTERVAL = 7 * 24 * 60 * 60; // 7 days

if (block.timestamp >= lastAllocation + REALLOCATION_INTERVAL) {
  // Check if reallocation needed
  if (shouldReallocate()) {
    reallocateCapital();
  }
}
```

### Threshold-Based Reallocation

```javascript
function shouldReallocate() {
  // Get current actual allocations
  const currentAllocations = getCurrentAllocations();
  const targetAllocations = [40, 30, 30];

  // Check if any strategy drifted > 5%
  for (let i = 0; i < strategies.length; i++) {
    const drift = Math.abs(currentAllocations[i] - targetAllocations[i]);

    if (drift > 5) {
      return true; // Reallocate needed
    }
  }

  return false;
}
```

## Gas Optimization

### Batch Allocation

```solidity
// Allocate to all strategies in single transaction
function allocateToStrategies() external onlyOwner {
    uint256 totalAssets = address(this).balance;

    for (uint i = 0; i < strategies.length; i++) {
        uint256 amount = totalAssets * allocations[i] / 100;
        strategies[i].deposit{value: amount}();
    }

    // Single transaction: ~350k gas
    // vs. 3 separate: 3 × 150k = 450k gas
    // Savings: 22%
}
```

### Conditional Allocation

```solidity
// Skip strategies that don't need reallocation
function smartReallocate() external onlyOwner {
    uint256 totalAssets = getTotalAssets();

    for (uint i = 0; i < strategies.length; i++) {
        uint256 currentAmount = strategies[i].totalAssets();
        uint256 targetAmount = totalAssets * allocations[i] / 100;

        // Only reallocate if difference > 1%
        if (abs(currentAmount - targetAmount) > totalAssets / 100) {
            if (currentAmount < targetAmount) {
                // Deposit more
                strategies[i].deposit{value: targetAmount - currentAmount}();
            } else {
                // Withdraw excess
                strategies[i].withdraw(currentAmount - targetAmount);
            }
        }
    }
}
```

## Performance Monitoring

### Allocation Efficiency

```javascript
function calculateAllocationEfficiency() {
  let weightedAPY = 0;

  for (const strategy of strategies) {
    const allocation = strategy.allocation / 100;
    const contribution = allocation * strategy.apy;
    weightedAPY += contribution;
  }

  // Compare to best single strategy
  const bestAPY = Math.max(...strategies.map((s) => s.apy));
  const efficiency = weightedAPY / bestAPY;

  return {
    blendedAPY: weightedAPY,
    bestSingleAPY: bestAPY,
    efficiency: efficiency, // e.g., 0.85 = 85% of best
  };
}

// Example:
// Blended: 7% APY
// Best (Uniswap): 18% APY
// Efficiency: 7/18 = 38.9%
//
// But with risk consideration:
// Blended risk: 3/10
// Uniswap risk: 5/10
// Risk-adjusted efficiency: Much better!
```

### Allocation Drift Tracking

```solidity
event AllocationDrift(
    uint256 indexed strategyIndex,
    uint256 targetAllocation,
    uint256 actualAllocation,
    uint256 driftPercentage
);

function trackAllocationDrift() external view returns (uint256[] memory) {
    uint256[] memory drifts = new uint256[](strategies.length);
    uint256 totalAssets = getTotalAssets();

    for (uint i = 0; i < strategies.length; i++) {
        uint256 actualAmount = strategies[i].totalAssets();
        uint256 actualPercentage = (actualAmount * 100) / totalAssets;

        drifts[i] = actualPercentage > allocations[i]
            ? actualPercentage - allocations[i]
            : allocations[i] - actualPercentage;
    }

    return drifts;
}
```

## Advanced Allocation Strategies

### Kelly Criterion (Future)

```javascript
// Optimal allocation based on expected returns and variance
function kellyAllocation(strategy) {
  const expectedReturn = strategy.apy / 100;
  const variance = strategy.volatility ** 2;

  // Kelly formula: f* = μ / σ²
  const optimalFraction = expectedReturn / variance;

  // Apply safety factor (half-Kelly)
  const safeFraction = optimalFraction * 0.5;

  return Math.min(safeFraction, 0.5); // Cap at 50%
}
```

### Mean-Variance Optimization (Future)

```javascript
function meanVarianceOptimization(strategies, targetReturn) {
  // Minimize portfolio variance for given target return
  // Using quadratic programming

  const weights = optimizeWeights({
    expectedReturns: strategies.map((s) => s.apy),
    covariances: calculateCovariances(strategies),
    targetReturn: targetReturn,
    constraints: {
      minWeight: 0.1,
      maxWeight: 0.5,
      sumToOne: true,
    },
  });

  return weights;
}
```

## Allocation History

### Tracking Changes

```solidity
struct AllocationSnapshot {
    uint256 timestamp;
    uint256[] allocations;
    uint256 totalAssets;
    string reason;
}

AllocationSnapshot[] public allocationHistory;

function recordAllocation(string memory reason) internal {
    allocationHistory.push(AllocationSnapshot({
        timestamp: block.timestamp,
        allocations: allocations,
        totalAssets: getTotalAssets(),
        reason: reason
    }));
}
```

### Historical Analysis

```javascript
// Fetch allocation history
const history = await contract.getAllocationHistory();

const chartData = history.map((snapshot) => ({
  date: new Date(snapshot.timestamp * 1000),
  aave: snapshot.allocations[0],
  lido: snapshot.allocations[1],
  uniswap: snapshot.allocations[2],
  totalTVL: ethers.utils.formatEther(snapshot.totalAssets),
}));

// Visualize allocation changes over time
<AreaChart data={chartData}>
  <Area dataKey="aave" stackId="1" fill="#82ca9d" />
  <Area dataKey="lido" stackId="1" fill="#8884d8" />
  <Area dataKey="uniswap" stackId="1" fill="#ffc658" />
</AreaChart>;
```

---

**Next**: [Rebalancing](./rebalancing) - How and when to adjust allocations.
