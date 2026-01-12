---
title: APY Monitoring
sidebar_position: 1
---

# APY Monitoring

Real-time tracking and historical analysis of yields across all Veilfi strategies to ensure optimal performance and transparent reporting.

## APY Calculation

### Formula

```javascript
// Annualized Percentage Yield
APY = ((1 + periodicRate) ^ periods) - 1

// Example: Daily rate of 0.019%
dailyRate = 0.00019
APY = (1.00019)^365 - 1 = 0.0725 = 7.25%
```

### Strategy-Specific Calculations

**Aave**:

```javascript
// Get current supply rate from Aave
const reserveData = await aavePool.getReserveData(WETH);
const supplyRate = reserveData.currentLiquidityRate;

// Convert RAY (10^27) to percentage
const aaveAPY = supplyRate / 1e25; // e.g., 5.2%
```

**Lido**:

```javascript
// stETH rebases daily
const day0Balance = stETH.balanceOf(user);
const day1Balance = stETH.balanceOf(user); // 24h later

const dailyYield = (day1Balance - day0Balance) / day0Balance;
const lidoAPY = dailyYield * 365; // e.g., 4.5%
```

**Uniswap**:

```javascript
// Calculate from 24h fee earnings
const position = await positionManager.positions(tokenId);
const fees24h = await calculateFees24h(position);
const positionValue = await getPositionValue(tokenId);

const dailyAPY = fees24h / positionValue;
const uniswapAPY = dailyAPY * 365; // e.g., 18%
```

## Blended APY

### Vault-Level Calculation

```javascript
function calculateBlendedAPY() {
  const strategies = [
    { name: "Aave", allocation: 0.4, apy: 0.05 },
    { name: "Lido", allocation: 0.3, apy: 0.045 },
    { name: "Uniswap", allocation: 0.3, apy: 0.18 },
  ];

  let blendedAPY = 0;

  for (const strategy of strategies) {
    blendedAPY += strategy.allocation * strategy.apy;
  }

  return blendedAPY; // 0.0685 = 6.85%
}
```

### Example Calculation

```
Strategy Yields:
├─ Aave:    40% × 5.0%  = 2.00%
├─ Lido:    30% × 4.5%  = 1.35%
└─ Uniswap: 30% × 18.0% = 5.40%
────────────────────────────────
Blended APY: 8.75%
```

## Real-Time Monitoring

### On-Chain Data Sources

```solidity
contract APYMonitor {
    function getStrategyAPYs() external view returns (
        uint256 aaveAPY,
        uint256 lidoAPY,
        uint256 uniswapAPY
    ) {
        aaveAPY = aaveStrategy.apy();
        lidoAPY = lidoStrategy.apy();
        uniswapAPY = uniswapStrategy.apy();
    }

    function getBlendedAPY() external view returns (uint256) {
        (uint256 a, uint256 l, uint256 u) = getStrategyAPYs();

        uint256 blended = (
            (a * allocations[0]) +
            (l * allocations[1]) +
            (u * allocations[2])
        ) / 100;

        return blended;
    }
}
```

### Frontend Display

```tsx
function APYDashboard() {
  const { aaveAPY, lidoAPY, uniswapAPY, blendedAPY } = useVaultAPYs();

  return (
    <div>
      <h2>Current APYs</h2>

      <MetricCard title="Blended APY" value={`${blendedAPY}%`} />

      <h3>Strategy Breakdown</h3>
      <APYRow strategy="Aave" apy={aaveAPY} allocation="40%" />
      <APYRow strategy="Lido" apy={lidoAPY} allocation="30%" />
      <APYRow strategy="Uniswap" apy={uniswapAPY} allocation="30%" />
    </div>
  );
}
```

## Historical Tracking

### Data Storage

```solidity
struct APYSnapshot {
    uint256 timestamp;
    uint256 aaveAPY;
    uint256 lidoAPY;
    uint256 uniswapAPY;
    uint256 blendedAPY;
}

APYSnapshot[] public apyHistory;

function recordAPYSnapshot() external {
    apyHistory.push(APYSnapshot({
        timestamp: block.timestamp,
        aaveAPY: aaveStrategy.apy(),
        lidoAPY: lidoStrategy.apy(),
        uniswapAPY: uniswapStrategy.apy(),
        blendedAPY: _calculateBlendedAPY()
    }));
}
```

### Historical Charts

```javascript
// Fetch 30-day APY history
const history = await contract.getAPYHistory(30);

const chartData = history.map((snapshot) => ({
  date: new Date(snapshot.timestamp * 1000),
  blendedAPY: snapshot.blendedAPY / 100,
  aaveAPY: snapshot.aaveAPY / 100,
  lidoAPY: snapshot.lidoAPY / 100,
  uniswapAPY: snapshot.uniswapAPY / 100,
}));

// Render chart
<LineChart data={chartData}>
  <Line dataKey="blendedAPY" stroke="#8884d8" />
  <Line dataKey="aaveAPY" stroke="#82ca9d" />
  <Line dataKey="lidoAPY" stroke="#ffc658" />
  <Line dataKey="uniswapAPY" stroke="#ff7c7c" />
</LineChart>;
```

## Performance Alerts

### Trigger Conditions

```javascript
// Alert if APY drops below threshold
if (blendedAPY < TARGET_APY * 0.8) {
  sendAlert("APY dropped 20% below target");
}

// Alert if strategy underperforming
if (uniswapAPY < aaveAPY) {
  sendAlert("Uniswap APY below Aave (unusual)");
}

// Alert if rebalancing needed
const apyDelta = Math.abs(uniswapAPY - aaveAPY);
if (apyDelta > 5) {
  sendAlert("Consider rebalancing (APY delta > 5%)");
}
```

## User-Facing Metrics

### Share Price Growth

```javascript
// More intuitive than APY for users
const initialSharePrice = 1.0;
const currentSharePrice = await vault.pricePerShare();

const growthPercentage =
  ((currentSharePrice - initialSharePrice) / initialSharePrice) * 100;

// Example: Share price went from 1.0 to 1.07
// Growth: 7% over the period
```

### Projected Earnings

```javascript
function calculateProjectedEarnings(depositAmount, days) {
  const dailyRate = blendedAPY / 365;
  const projectedValue = depositAmount * Math.pow(1 + dailyRate, days);
  const earnings = projectedValue - depositAmount;

  return {
    total: projectedValue,
    earnings: earnings,
    apy: blendedAPY,
  };
}

// Example: $10,000 deposit for 30 days at 7% APY
// Earnings: ~$57.53
```

---

**Next**: [Risk Assessment](./risk-assessment) - Strategy risk analysis.
