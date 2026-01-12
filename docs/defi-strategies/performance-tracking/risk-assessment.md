---
title: Risk Assessment
sidebar_position: 2
---

# Risk Assessment

Comprehensive risk analysis across all Veilfi strategies to ensure informed decision-making and transparent risk disclosure.

## Risk Framework

### Risk Categories

| Category           | Definition              | Impact             |
| ------------------ | ----------------------- | ------------------ |
| **Smart Contract** | Code vulnerability      | Total loss         |
| **Oracle**         | Price feed manipulation | Partial loss       |
| **Liquidity**      | Cannot exit position    | Delayed withdrawal |
| **Economic**       | Impermanent loss, depeg | Value erosion      |
| **Systemic**       | Market-wide crash       | Temporary drawdown |

## Strategy Risk Profiles

### Aave Strategy

**Risk Score**: 2/10 (Very Low)

| Risk Type      | Level       | Mitigation                                |
| -------------- | ----------- | ----------------------------------------- |
| Smart Contract | 🟢 Very Low | 10+ audits, 4+ years live, $10B TVL       |
| Oracle         | 🟢 Low      | Chainlink oracles (battle-tested)         |
| Liquidity      | 🟢 Very Low | Instant withdrawals (10-20% reserve)      |
| Economic       | 🟢 Very Low | Lenders don't face liquidation            |
| Systemic       | 🟡 Medium   | Bank run possible (mitigated by reserves) |

**Historical Incidents**: None (no major exploits since 2020)

**Insurance**: $50M+ Aave Safety Module

### Lido Strategy

**Risk Score**: 2/10 (Very Low)

| Risk Type      | Level     | Mitigation                             |
| -------------- | --------- | -------------------------------------- |
| Smart Contract | 🟢 Low    | 15+ audits, 3+ years live, $30B TVL    |
| Oracle         | N/A       | No oracle dependency                   |
| Liquidity      | 🟢 Low    | DEX pools (0.1-0.5% slippage)          |
| Economic       | 🟡 Medium | stETH depeg risk (temporary)           |
| Systemic       | 🟡 Medium | Ethereum network risk (extremely rare) |

**Historical Incidents**:

- May 2022: stETH depeg to 0.93 (recovered)
- Jun 2023: stETH depeg to 0.95 (recovered)

**Insurance**: $100M+ self-insurance

### Uniswap Strategy

**Risk Score**: 5/10 (Medium)

| Risk Type      | Level     | Mitigation                         |
| -------------- | --------- | ---------------------------------- |
| Smart Contract | 🟢 Low    | 8+ audits, 3+ years live, $5B TVL  |
| Oracle         | 🟢 Low    | TWAP (time-weighted average)       |
| Liquidity      | 🟢 Low    | Instant withdrawals                |
| Economic       | 🔴 High   | Impermanent loss (10-20% possible) |
| Systemic       | 🟡 Medium | Low liquidity during crashes       |

**Historical Incidents**: None (V3 secure since 2021)

**IL Mitigation**: High trading fees (~15-30% APY) offset IL

## Portfolio-Level Risk

### Diversification Benefit

```
Single Strategy Risk: 5/10 (if 100% Uniswap)
Diversified Risk: 3/10 (40% Aave, 30% Lido, 30% Uniswap)

Risk Reduction: 40% through diversification
```

### Correlation Analysis

| Strategy Pair  | Correlation  | Benefit                     |
| -------------- | ------------ | --------------------------- |
| Aave ↔ Lido    | Low (0.2)    | ✅ Good diversification     |
| Aave ↔ Uniswap | Medium (0.4) | ✅ Moderate diversification |
| Lido ↔ Uniswap | Low (0.3)    | ✅ Good diversification     |

**Low correlation** = When one underperforms, others may still perform well.

## Risk Metrics

### Value at Risk (VaR)

```
95% Confidence VaR (1-day): -2.5%

Interpretation:
95% of days, vault won't lose more than 2.5%
In 1 out of 20 days, losses may exceed 2.5%
```

### Maximum Drawdown

```
Historical Maximum Drawdown: -8%
Expected Annual Drawdown: -5 to -10%

Example:
$100k investment → Worst case: $92k temporarily
Expected recovery: 1-3 months
```

### Sharpe Ratio

```
Sharpe Ratio = (Return - Risk-Free Rate) / Volatility

Veilfi: (7% - 0%) / 8% = 0.875

Interpretation:
> 1.0 = Excellent risk-adjusted returns
0.5-1.0 = Good risk-adjusted returns
< 0.5 = Poor risk-adjusted returns

Veilfi: Good but can improve
```

## Scenario Analysis

### Best Case (Bull Market)

```
Aave APY: 8% × 40% = 3.2%
Lido APY: 5% × 30% = 1.5%
Uniswap APY: 40% × 30% = 12%
──────────────────────────
Blended APY: 16.7%

User $10k → $11,670 in 1 year ✅
```

### Base Case (Normal Market)

```
Aave APY: 5% × 40% = 2.0%
Lido APY: 4.5% × 30% = 1.35%
Uniswap APY: 15% × 30% = 4.5%
──────────────────────────
Blended APY: 7.85%

User $10k → $10,785 in 1 year ✅
```

### Worst Case (Bear Market)

```
Aave APY: 3% × 40% = 1.2%
Lido APY: 4% × 30% = 1.2%
Uniswap APY: 5% × 30% = 1.5%
Uniswap IL: -10% × 30% = -3%
──────────────────────────
Blended Return: 0.9%

User $10k → $10,090 in 1 year (still positive) ✅
```

## Risk Mitigation Strategies

### 1. Allocation Limits

```solidity
uint256 public constant MAX_SINGLE_ALLOCATION = 50;  // 50%

// Prevent over-concentration
require(newAllocation <= MAX_SINGLE_ALLOCATION, "Exceeds limit");
```

**Why**: Limits blast radius if one strategy fails.

### 2. Emergency Pause

```solidity
function emergencyPause() external onlyOwner {
    paused = true;

    // Withdraw from all strategies
    for (uint i = 0; i < strategies.length; i++) {
        strategies[i].emergencyWithdraw();
    }
}
```

**When**: Exploit detected or market anomaly.

### 3. Gradual Rollout

```
Week 1: $100k TVL cap
Week 4: $1M TVL cap
Week 8: $10M TVL cap
Week 12: Remove cap if no issues
```

**Why**: Test strategies with limited capital first.

### 4. Circuit Breakers

```javascript
// Halt deposits if APY drops too much
if (currentAPY < lastAPY * 0.5) {
  pauseDeposits();
  alertAdmin("APY dropped 50% - investigate");
}

// Halt withdrawals if too rapid
if (withdrawals24h > TVL * 0.3) {
  pauseWithdrawals();
  alertAdmin("Bank run detected - 30% TVL withdrawn");
}
```

## User Risk Disclosure

### Risk Warnings

```
⚠️ WARNING: Yield farming carries risks:

1. Smart Contract Risk: Bugs could lead to loss of funds
2. Impermanent Loss: Uniswap positions may lose value vs. holding
3. stETH Depeg: Lido's stETH may trade below 1 ETH
4. APY Volatility: Returns are not guaranteed
5. Market Risk: Crypto market downturns affect all strategies

Do not invest more than you can afford to lose.
```

### Risk Acceptance

```typescript
// Before first deposit
function acknowledgeRisks() {
  const [acknowledged, setAcknowledged] = useState(false);

  return (
    <div>
      <h2>Risk Acknowledgment</h2>
      <ul>
        <li>I understand smart contract risks</li>
        <li>I understand impermanent loss</li>
        <li>I understand yields are not guaranteed</li>
      </ul>

      <Checkbox
        checked={acknowledged}
        onChange={() => setAcknowledged(!acknowledged)}
      >
        I acknowledge all risks
      </Checkbox>

      <Button disabled={!acknowledged}>Proceed to Deposit</Button>
    </div>
  );
}
```

## Ongoing Monitoring

### Daily Checks

- ✅ APY monitoring (alert if &lt;80% of target)
- ✅ TVL changes (alert if &gt;20% daily swing)
- ✅ Strategy health checks
- ✅ Gas price monitoring

### Weekly Reviews

- ✅ Protocol news monitoring (Twitter, Discord)
- ✅ Security incident scanning (Rekt News, PeckShield)
- ✅ Allocation rebalancing decisions
- ✅ User feedback review

### Monthly Audits

- ✅ Performance vs. expectations
- ✅ Risk metric recalculation
- ✅ Strategy addition/removal evaluation
- ✅ Insurance coverage review

---

**Congratulations!** You've completed the **DeFi Strategies** section.

**Next**: [Core Flow](../../core-flow/user-flow/wallet-connection) - Learn user interaction flows.
