---
title: Rebalancing
sidebar_position: 2
---

# Rebalancing

Rebalancing restores target allocations when strategies drift due to performance differences, ensuring optimal risk-return balance.

## Why Rebalancing Matters

### Allocation Drift Problem

```
Initial State (Week 0):
├─ Aave:    40% (400 ETH) @ 5% APY
├─ Lido:    30% (300 ETH) @ 4.5% APY
└─ Uniswap: 30% (300 ETH) @ 18% APY

After 1 Month (Uniswap outperforms):
├─ Aave:    38.5% (401.67 ETH) - underweight
├─ Lido:    29.2% (301.13 ETH) - underweight
└─ Uniswap: 32.3% (304.50 ETH) - overweight

Drift: Uniswap now 32.3% instead of target 30%
```

**Impact**: Higher risk than intended (Uniswap has 5/10 risk score).

## Rebalancing Triggers

### 1. Time-Based Rebalancing

```solidity
uint256 public constant REBALANCE_INTERVAL = 7 days;
uint256 public lastRebalanceTime;

modifier canRebalance() {
    require(
        block.timestamp >= lastRebalanceTime + REBALANCE_INTERVAL,
        "Too soon to rebalance"
    );
    _;
}

function rebalance() external onlyOwner canRebalance {
    _executeRebalance();
    lastRebalanceTime = block.timestamp;
}
```

**Schedule**: Every 7 days (weekly)

### 2. Threshold-Based Rebalancing

```javascript
function needsRebalancing() {
    const drifts = calculateAllocationDrifts();

    // Rebalance if any strategy drifted > 5%
    for (const drift of drifts) {
        if (Math.abs(drift) > 5) {
            return true;
        }
    }

    return false;
}

function calculateAllocationDrifts() {
    const totalAssets = await vault.getTotalAssets();
    const targets = [40, 30, 30];  // Target allocations

    const drifts = [];

    for (let i = 0; i < strategies.length; i++) {
        const actualAmount = await strategies[i].totalAssets();
        const actualPercent = (actualAmount / totalAssets) * 100;
        const drift = actualPercent - targets[i];

        drifts.push(drift);
    }

    return drifts;
}
```

**Threshold**: ±5% drift triggers rebalancing

### 3. APY-Based Rebalancing

```javascript
function apy BasedRebalance() {
    const apys = await getAllStrategyAPYs();

    // If APY spread > 10%, consider rebalancing
    const maxAPY = Math.max(...apys);
    const minAPY = Math.min(...apys);

    if (maxAPY - minAPY > 10) {
        // Shift more to high-APY strategy
        return true;
    }

    return false;
}
```

**Example**: Uniswap jumps to 30% APY → Increase allocation

## Rebalancing Process

### Step-by-Step Flow

```
1. Calculate current allocations
   ↓
2. Determine target allocations
   ↓
3. Calculate differences
   ↓
4. Withdraw from overweight strategies
   ↓
5. Deposit to underweight strategies
   ↓
6. Verify final allocations
```

### Smart Contract Implementation

```solidity
function executeRebalance() external onlyOwner {
    uint256 totalAssets = getTotalAssets();

    // Step 1: Calculate target amounts
    uint256[] memory targetAmounts = new uint256[](strategies.length);
    for (uint i = 0; i < strategies.length; i++) {
        targetAmounts[i] = totalAssets * allocations[i] / 100;
    }

    // Step 2: Withdraw excess from overweight strategies
    for (uint i = 0; i < strategies.length; i++) {
        uint256 currentAmount = strategies[i].totalAssets();

        if (currentAmount > targetAmounts[i]) {
            uint256 excess = currentAmount - targetAmounts[i];
            strategies[i].withdraw(excess);
        }
    }

    // Step 3: Deposit to underweight strategies
    for (uint i = 0; i < strategies.length; i++) {
        uint256 currentAmount = strategies[i].totalAssets();

        if (currentAmount < targetAmounts[i]) {
            uint256 deficit = targetAmounts[i] - currentAmount;
            strategies[i].deposit{value: deficit}();
        }
    }

    emit Rebalanced(targetAmounts, block.timestamp);
}
```

### Optimized Rebalancing

```solidity
// Only rebalance strategies that drifted significantly
function smartRebalance() external onlyOwner {
    uint256 totalAssets = getTotalAssets();
    uint256 threshold = totalAssets / 100;  // 1% threshold

    for (uint i = 0; i < strategies.length; i++) {
        uint256 currentAmount = strategies[i].totalAssets();
        uint256 targetAmount = totalAssets * allocations[i] / 100;

        uint256 difference = currentAmount > targetAmount
            ? currentAmount - targetAmount
            : targetAmount - currentAmount;

        // Only rebalance if difference > 1%
        if (difference > threshold) {
            if (currentAmount > targetAmount) {
                strategies[i].withdraw(currentAmount - targetAmount);
            } else {
                strategies[i].deposit{value: targetAmount - currentAmount}();
            }
        }
    }
}
```

**Gas Savings**: Skip strategies that don't need adjustment.

## Rebalancing Strategies

### 1. Proportional Rebalancing

Maintain exact target ratios:

```
Target: 40/30/30
Current: 38.5/29.2/32.3

Action:
├─ Withdraw 2.3% from Uniswap (32.3% → 30%)
├─ Deposit 1.5% to Aave (38.5% → 40%)
└─ Deposit 0.8% to Lido (29.2% → 30%)

Result: Exact 40/30/30 restored
```

### 2. Band Rebalancing

Only rebalance when outside acceptable band:

```javascript
const REBALANCE_BANDS = {
  aave: { min: 35, max: 45 }, // ±5% band
  lido: { min: 25, max: 35 },
  uniswap: { min: 25, max: 35 },
};

function needsBandRebalancing(strategyIndex, actualPercent) {
  const band = REBALANCE_BANDS[strategyIndex];
  return actualPercent < band.min || actualPercent > band.max;
}

// Example:
// Aave at 38.5% → Within 35-45% band → No rebalancing
// Uniswap at 36% → Outside 25-35% band → Rebalance!
```

**Benefit**: Reduce unnecessary rebalancing (save gas).

### 3. Opportunistic Rebalancing

Combine with other operations:

```solidity
function harvestAndRebalance() external onlyOwner {
    // 1. Harvest yields from all strategies
    for (uint i = 0; i < strategies.length; i++) {
        strategies[i].harvest();
    }

    // 2. Rebalance using harvested yields
    if (needsRebalancing()) {
        executeRebalance();
    }

    // Single transaction: Save gas!
}
```

**Benefit**: Amortize gas costs across operations.

## Cost Considerations

### Gas Costs

```
Rebalancing Breakdown:
├─ Withdraw from 1 strategy:  ~150k gas (~$10 @ 100 gwei)
├─ Deposit to 2 strategies:   ~300k gas (~$20)
├─ Smart contract logic:       ~50k gas (~$3)
────────────────────────────────────────────
Total: ~500k gas (~$33 per rebalance)

Monthly cost (4 rebalances): ~$132
```

### Cost-Benefit Analysis

```javascript
function shouldRebalanceCostBenefit() {
  const rebalanceCost = 500000 * gasPrice; // Gas cost in ETH
  const tvl = totalAssets;

  // Only rebalance if cost < 0.1% of TVL
  const costRatio = rebalanceCost / tvl;

  if (costRatio > 0.001) {
    // 0.1%
    return false; // Too expensive
  }

  // Estimate benefit from improved allocation
  const currentAPY = calculateCurrentAPY();
  const targetAPY = calculateTargetAPY();
  const apyGain = targetAPY - currentAPY;

  // Annualized benefit
  const annualBenefit = tvl * apyGain;

  // ROI = annual benefit / rebalance cost
  return annualBenefit > rebalanceCost * 10; // 10x ROI minimum
}
```

## Slippage & Execution

### Slippage Management

```solidity
function rebalanceWithSlippage(uint256 maxSlippage) external onlyOwner {
    require(maxSlippage <= 500, "Max 5% slippage");  // 500 basis points

    for (uint i = 0; i < strategies.length; i++) {
        uint256 currentAmount = strategies[i].totalAssets();
        uint256 targetAmount = getTotalAssets() * allocations[i] / 100;

        if (currentAmount > targetAmount) {
            uint256 amountToWithdraw = currentAmount - targetAmount;
            uint256 minReceived = amountToWithdraw * (10000 - maxSlippage) / 10000;

            // Withdraw with slippage protection
            uint256 received = strategies[i].withdrawWithMinimum(
                amountToWithdraw,
                minReceived
            );

            require(received >= minReceived, "Slippage too high");
        }
    }
}
```

### Multi-Step Rebalancing

For large rebalances, split into smaller transactions:

```javascript
async function gradualRebalance(steps = 4) {
  const totalRebalance = calculateRebalanceAmount();
  const amountPerStep = totalRebalance / steps;

  for (let i = 0; i < steps; i++) {
    // Execute partial rebalance
    await executePartialRebalance(amountPerStep);

    // Wait for confirmation
    await sleep(60000); // 1 minute between steps
  }
}
```

**Benefit**: Reduce market impact, better pricing.

## Monitoring & Alerts

### Rebalancing Dashboard

```typescript
interface RebalancingMetrics {
  lastRebalance: Date;
  daysSinceRebalance: number;
  currentDrifts: number[];
  needsRebalancing: boolean;
  estimatedCost: string;
  estimatedAPYGain: string;
}

function RebalancingDashboard() {
  const metrics = useRebalancingMetrics();

  return (
    <div>
      <h2>Rebalancing Status</h2>

      <MetricCard
        title="Last Rebalance"
        value={metrics.lastRebalance.toLocaleDateString()}
      />

      <MetricCard
        title="Days Since"
        value={metrics.daysSinceRebalance}
        alert={metrics.daysSinceRebalance > 7}
      />

      <h3>Current Drifts</h3>
      {metrics.currentDrifts.map((drift, i) => (
        <DriftIndicator strategy={strategies[i]} drift={drift} threshold={5} />
      ))}

      {metrics.needsRebalancing && (
        <Alert severity="warning">
          Rebalancing recommended
          <br />
          Est. Cost: {metrics.estimatedCost}
          <br />
          Est. APY Gain: {metrics.estimatedAPYGain}
        </Alert>
      )}
    </div>
  );
}
```

### Automated Alerts

```javascript
// Monitor and alert
async function monitorRebalancing() {
  const drifts = await calculateDrifts();

  for (let i = 0; i < drifts.length; i++) {
    if (Math.abs(drifts[i]) > 5) {
      sendAlert({
        type: "REBALANCING_NEEDED",
        strategy: strategies[i].name,
        drift: drifts[i],
        urgency: Math.abs(drifts[i]) > 10 ? "HIGH" : "MEDIUM",
      });
    }
  }
}

// Run every hour
setInterval(monitorRebalancing, 3600000);
```

## Rebalancing History

### Event Logging

```solidity
event Rebalanced(
    uint256 timestamp,
    uint256[] oldAllocations,
    uint256[] newAllocations,
    uint256 gasCost,
    string reason
);

function rebalance(string memory reason) external onlyOwner {
    uint256[] memory oldAllocations = getCurrentAllocations();

    _executeRebalance();

    uint256[] memory newAllocations = getCurrentAllocations();

    emit Rebalanced(
        block.timestamp,
        oldAllocations,
        newAllocations,
        gasleft(),
        reason
    );
}
```

### Historical Analysis

```javascript
// Fetch rebalancing history
const events = await contract.queryFilter(contract.filters.Rebalanced());

const rebalanceData = events.map((event) => ({
  date: new Date(event.args.timestamp * 1000),
  reason: event.args.reason,
  gasCost: ethers.utils.formatEther(event.args.gasCost),
  changes: calculateAllocationChanges(
    event.args.oldAllocations,
    event.args.newAllocations
  ),
}));

// Analyze frequency
const avgInterval = calculateAverageInterval(rebalanceData);
console.log(`Average rebalancing interval: ${avgInterval} days`);
```

---

**Next**: [Risk Assessment](./risk-assessment) - Managing portfolio risk.
