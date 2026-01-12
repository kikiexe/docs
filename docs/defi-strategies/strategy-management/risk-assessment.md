---
title: Risk Assessment
sidebar_position: 3
---

# Risk Assessment

Continuous risk monitoring and management across all strategies to protect user capital and maintain optimal risk-return balance.

## Risk Framework

### Multi-Dimensional Risk Model

```javascript
const RiskFactors = {
  smartContract: 0.3, // 30% weight
  liquidity: 0.2, // 20% weight
  economic: 0.25, // 25% weight
  operational: 0.15, // 15% weight
  systemic: 0.1, // 10% weight
};

function calculateStrategyRisk(strategy) {
  const scores = {
    smartContract: assessSmartContractRisk(strategy),
    liquidity: assessLiquidityRisk(strategy),
    economic: assessEconomicRisk(strategy),
    operational: assessOperationalRisk(strategy),
    systemic: assessSystemicRisk(strategy),
  };

  let totalRisk = 0;

  for (const [factor, weight] of Object.entries(RiskFactors)) {
    totalRisk += scores[factor] * weight;
  }

  return totalRisk; // 0-10 scale
}
```

## Per-Strategy Risk Scoring

### Aave Risk Assessment

```javascript
const AaveRisk = {
  smartContract: 2, // 10+ audits, 4+ years
  liquidity: 1, // $10B+ TVL, instant withdrawals
  economic: 2, // Interest rate volatility
  operational: 1, // Automated, battle-tested
  systemic: 3, // DeFi-wide contagion possible

  overall: 1.85, // Very Low Risk
};
```

**Risk Score**: 1.85/10 (Very Low)

### Lido Risk Assessment

```javascript
const LidoRisk = {
  smartContract: 2, // 15+ audits, 3+ years
  liquidity: 2, // DEX swaps, 1-7 day queue
  economic: 3, // stETH depeg risk
  operational: 2, // Validator management
  systemic: 2, // Ethereum network dependency

  overall: 2.25, // Very Low Risk
};
```

**Risk Score**: 2.25/10 (Very Low)

### Uniswap Risk Assessment

```javascript
const UniswapRisk = {
  smartContract: 2, // 8+ audits, 3+ years
  liquidity: 2, // Deep pools, instant swaps
  economic: 7, // Impermanent loss significant
  operational: 3, // Position management required
  systemic: 4, // MEV, front-running

  overall: 4.15, // Medium Risk
};
```

**Risk Score**: 4.15/10 (Medium)

## Portfolio Risk Calculation

### Weighted Risk Score

```javascript
function calculatePortfolioRisk() {
  const strategies = [
    { name: "Aave", allocation: 0.4, risk: 1.85 },
    { name: "Lido", allocation: 0.3, risk: 2.25 },
    { name: "Uniswap", allocation: 0.3, risk: 4.15 },
  ];

  let portfolioRisk = 0;

  for (const strategy of strategies) {
    portfolioRisk += strategy.allocation * strategy.risk;
  }

  return portfolioRisk;
}

// Result: 0.40×1.85 + 0.30×2.25 + 0.30×4.15 = 2.66
```

**Portfolio Risk**: 2.66/10 (Low)

**Diversification Benefit**: Individual high-risk (Uniswap: 4.15) reduced through allocation.

## Real-Time Risk Monitoring

### On-Chain Risk Indicators

```solidity
contract RiskMonitor {
    struct RiskMetrics {
        uint256 tvlRatio;           // Strategy TVL / Protocol TVL
        uint256 utilizationRate;     // For lending protocols
        uint256 volatility;          // Price volatility
        uint256 liquidityDepth;      // Available liquidity
        bool healthStatus;           // Overall health
    }

    mapping(address => RiskMetrics) public strategyRisks;

    function updateRiskMetrics(uint256 strategyIndex) external {
        IStrategy strategy = strategies[strategyIndex];

        strategyRisks[address(strategy)] = RiskMetrics({
            tvlRatio: calculateTVLRatio(strategy),
            utilizationRate: strategy.getUtilization(),
            volatility: calculateVolatility(strategy),
            liquidityDepth: strategy.availableLiquidity(),
            healthStatus: assessHealth(strategy)
        });
    }

    function isStrategyHealthy(uint256 strategyIndex) external view returns (bool) {
        RiskMetrics memory metrics = strategyRisks[address(strategies[strategyIndex])];

        // Check all risk factors
        if (metrics.utilizationRate > 90) return false;  // Over-utilized
        if (metrics.volatility > 50) return false;       // Too volatile
        if (!metrics.healthStatus) return false;         // General health issue

        return true;
    }
}
```

### Risk Alerts

```javascript
async function monitorRisks() {
  const strategies = await getAllStrategies();

  for (const strategy of strategies) {
    // Check 1: TVL concentration
    if (strategy.vaultTVL / strategy.protocolTVL > 0.1) {
      sendAlert({
        level: "WARNING",
        strategy: strategy.name,
        issue: "High TVL concentration (>10% of protocol)",
        action: "Consider reducing allocation",
      });
    }

    // Check 2: Utilization (for lending)
    if (strategy.type === "lending" && strategy.utilization > 85) {
      sendAlert({
        level: "WARNING",
        strategy: strategy.name,
        issue: `High utilization: ${strategy.utilization}%`,
        action: "Liquidity may be constrained",
      });
    }

    // Check 3: APY anomaly
    if (strategy.currentAPY < strategy.historicalAvgAPY * 0.5) {
      sendAlert({
        level: "INFO",
        strategy: strategy.name,
        issue: "APY dropped 50% below historical average",
        action: "Investigate cause",
      });
    }
  }
}
```

## Risk Limits & Circuit Breakers

### Allocation Limits

```solidity
uint256 public constant MAX_HIGH_RISK_ALLOCATION = 30;  // 30% max for risk > 4

function validateAllocation(uint256 strategyIndex, uint256 allocation)
    internal view returns (bool)
{
    uint256 riskScore = strategies[strategyIndex].getRiskScore();

    if (riskScore > 4 && allocation > MAX_HIGH_RISK_ALLOCATION) {
        return false;  // High-risk strategy exceeds limit
    }

    return true;
}
```

### Emergency Pause

```solidity
bool public emergencyPaused;

function emergencyPause(uint256 strategyIndex, string memory reason)
    external onlyOwner
{
    // Withdraw all assets from risky strategy
    strategies[strategyIndex].emergencyWithdraw();

    // Mark as paused
    strategyActive[strategyIndex] = false;
    emergencyPaused = true;

    emit EmergencyPause(strategyIndex, reason, block.timestamp);
}
```

### Gradual Withdrawal

```solidity
// For large withdrawals, spread over time to minimize impact
function gradualWithdrawal(
    uint256 strategyIndex,
    uint256 totalAmount,
    uint256 steps
) external onlyOwner {
    uint256 amountPerStep = totalAmount / steps;

    for (uint i = 0; i < steps; i++) {
        strategies[strategyIndex].withdraw(amountPerStep);

        // Wait for next block to avoid MEV
        if (i < steps - 1) {
            require(block.number > lastWithdrawalBlock, "Wait for next block");
            lastWithdrawalBlock = block.number;
        }
    }
}
```

## Stress Testing

### Scenario Analysis

```javascript
function stressTest() {
  const scenarios = [
    {
      name: "Market Crash (-50%)",
      aaveAPY: 2,
      lidoAPY: 3,
      uniswapAPY: -20, // Negative due to IL
      outcome: calculateReturn([2, 3, -20]),
    },
    {
      name: "DeFi Exploit (Aave compromised)",
      aaveImpact: -100, // Total loss
      outcome: 0.4 * -100 + 0.3 * 4.5 + 0.3 * 18,
    },
    {
      name: "stETH Depeg (-10%)",
      lidoImpact: -10,
      outcome: 0.4 * 5 + 0.3 * -10 + 0.3 * 18,
    },
  ];

  return scenarios;
}

// Results:
// Market Crash: -3.5% return (still bearable)
// Aave Exploit: -40% loss (limited by 40% allocation)
// stETH Depeg: +4.4% return (still positive)
```

### Value at Risk (VaR)

```javascript
function calculateVaR(confidence = 0.95, timeframe = 1) {
  // Historical volatility
  const dailyVolatility = 0.025; // 2.5% daily std dev

  // Z-score for 95% confidence: 1.65
  const zScore = 1.65;

  // VaR = z-score × volatility × sqrt(timeframe)
  const var95 = zScore * dailyVolatility * Math.sqrt(timeframe);

  return var95; // 0.04125 = 4.125%
}

// Interpretation: 95% confidence that daily loss won't exceed 4.125%
```

## Risk-Adjusted Performance

### Sharpe Ratio

```javascript
function calculateSharpeRatio(returns, riskFreeRate = 0) {
  const avgReturn = mean(returns);
  const stdDev = standardDeviation(returns);

  const sharpe = (avgReturn - riskFreeRate) / stdDev;

  return sharpe;
}

// Example:
// Avg Return: 7% APY
// Std Dev: 8%
// Risk-free Rate: 0% (crypto has no truly risk-free rate)
// Sharpe: 7 / 8 = 0.875

// Interpretation:
// > 1.0 = Excellent
// 0.5-1.0 = Good
// < 0.5 = Poor
```

### Sortino Ratio

```javascript
// Like Sharpe, but only penalizes downside volatility
function calculateSortinoRatio(returns, targetReturn = 0) {
  const avgReturn = mean(returns);

  // Only consider negative returns
  const downsideReturns = returns.filter((r) => r < targetReturn);
  const downsideDeviation = standardDeviation(downsideReturns);

  const sortino = (avgReturn - targetReturn) / downsideDeviation;

  return sortino;
}

// Better for asymmetric return distributions (crypto)
```

## Risk Reporting

### User-Facing Dashboard

```typescript
interface RiskDashboard {
  portfolioRisk: number; // 0-10 scale
  strategyRisks: {
    name: string;
    risk: number;
    status: "healthy" | "warning" | "critical";
  }[];
  riskFactors: {
    smartContract: number;
    liquidity: number;
    economic: number;
    operational: number;
    systemic: number;
  };
  riskMetrics: {
    var95: number;
    maxDrawdown: number;
    sharpeRatio: number;
  };
}

function RiskDashboard({ data }: { data: RiskDashboard }) {
  return (
    <div>
      <h2>Portfolio Risk</h2>

      <RiskGauge
        value={data.portfolioRisk}
        max={10}
        thresholds={[3, 6, 10]}
        colors={["green", "yellow", "red"]}
      />

      <h3>Strategy Risk Breakdown</h3>
      {data.strategyRisks.map((strategy) => (
        <StrategyRiskCard key={strategy.name} strategy={strategy} />
      ))}

      <h3>Risk Metrics</h3>
      <MetricGrid>
        <Metric label="95% VaR (1-day)" value={`${data.riskMetrics.var95}%`} />
        <Metric
          label="Max Drawdown"
          value={`${data.riskMetrics.maxDrawdown}%`}
        />
        <Metric
          label="Sharpe Ratio"
          value={data.riskMetrics.sharpeRatio.toFixed(2)}
        />
      </MetricGrid>
    </div>
  );
}
```

### Risk Transparency

```markdown
## Risk Disclosure

Veilfi's current portfolio risk profile:

**Overall Risk**: 2.66/10 (Low)

**Risk Breakdown**:

- Aave: 1.85/10 (40% allocation)
- Lido: 2.25/10 (30% allocation)
- Uniswap: 4.15/10 (30% allocation)

**Key Risks**:

1. Smart Contract Risk: Low (all strategies audited 8+ times)
2. Impermanent Loss: Medium (Uniswap LP positions)
3. stETH Depeg: Low (historically temporary)

**Worst-Case Scenario**: -40% loss if single strategy fully compromised
**Mitigations**: 40% max allocation, continuous monitoring, emergency pause
```

---

**Congratulations!** You've completed all **Strategy Management** files.

**Next**: Explore other sections like [Core Flow](../../core-flow/user-flow/wallet-connection) for user interaction flows.
