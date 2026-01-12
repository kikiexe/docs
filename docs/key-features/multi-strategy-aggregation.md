---
title: Multi-Strategy Aggregation
sidebar_position: 2
---

# Multi-Strategy Aggregation

Veilfi automatically diversifies capital across multiple battle-tested DeFi protocols to maximize risk-adjusted returns.

## The Aggregation Advantage

### Single Strategy (Risky)

```
100% in Uniswap V3
├─ APY: 25%
├─ Risk: 5/10 (High - impermanent loss)
└─ If exploited: 100% loss
```

### Multi-Strategy (Safer)

```
Veilfi Diversification:
├─ 40% Aave (5% APY, 2/10 risk)
├─ 30% Lido (4.5% APY, 2/10 risk)
└─ 30% Uniswap (18% APY, 5/10 risk)

Blended:
├─ APY: 8.25%
├─ Risk: 2.95/10 (Low - diversified)
└─ If one exploited: 30-40% max loss
```

**Result**: Better risk/reward ratio

## Supported Strategies

### 1. Aave V3 (Lending)

```
Protocol: Aave
Type: Supply-side lending
TVL: $10B+
APY: 3-8%
Risk: Very Low (2/10)

How it works:
User deposits → Aave lending pool → Earn interest from borrowers
```

### 2. Lido (ETH Staking)

```
Protocol: Lido Finance
Type: Liquid staking
TVL: $30B+
APY: 4-5%
Risk: Very Low (2/10)

How it works:
User deposits → Staked on Ethereum → Earn validator rewards
```

### 3. Uniswap V3 (LP)

```
Protocol: Uniswap V3
Type: Liquidity provision
TVL: $5B+
APY: 10-30%
Risk: Medium (5/10)

How it works:
User deposits → ETH/USDC pool → Earn trading fees
```

## Allocation Strategy

### Current Allocation

```javascript
const allocations = {
  aave: 40, // Largest - lowest risk
  lido: 30, // Medium - stable yield
  uniswap: 30, // Limited - controls IL risk
};

// Max 50% per strategy (risk limit)
// Min 10% per strategy (true diversification)
```

### Why 40/30/30?

**40% Aave** (Safety-first):

- Most established ($10B+ TVL, 4+ years)
- Instant liquidity
- Predictable yields
- Lowest risk profile

**30% Lido** (Stable returns):

- Ethereum network security
- Liquid staking (stETH)
- Consistent 4-5% APY
- Low correlation with lending

**30% Uniswap** (Yield boost):

- Higher APY potential
- Acceptable risk (5/10)
- Limited to 30% to control impermanent loss
- Balances safety vs returns

## Automatic Rebalancing

### When Rebalancing Occurs

```solidity
// Trigger 1: Weekly schedule
if (block.timestamp > lastRebalance + 7 days) {
    rebalance();
}

// Trigger 2: Drift > 5%
if (actualAllocation - targetAllocation > 5%) {
    rebalance();
}

// Trigger 3: APY opportunity
if (strategyAPYDelta > 10%) {
    considerRebalancing();
}
```

### Rebalancing Process

```
1. Check current allocations
   Aave: 38%, Lido: 29%, Uniswap: 33%

2. Compare to targets
   Targets: 40%, 30%, 30%
   Drifts: -2%, -1%, +3%

3. Rebalance if needed
   Uniswap drifted 3% → Rebalance ✅

4. Execute trades
   Withdraw 3% from Uniswap
   → Deposit 2% to Aave, 1% to Lido
```

## Performance Optimization

### Dynamic APY Adjustment (Future)

```javascript
// Adjust allocations based on current APYs
function optimizeAllocations(strategies) {
  return strategies.map((s) => {
    // Higher allocation to better risk-adjusted APY
    const riskAdjustedAPY = s.apy / (1 + s.riskScore);
    return {
      allocation: calculateOptimal(riskAdjustedAPY),
      maxAllocation: 50, // Safety cap
    };
  });
}
```

## Risk Mitigation

### Diversification Benefits

```
If Uniswap exploited:
├─ Single strategy: 100% loss
└─ Veilfi (30% allocation): 30% loss

Recovery:
├─ Redirect future deposits to safe strategies
├─ Remaining 70% continues earning
└─ Rebalance to 50/50 Aave/Lido
```

### Protocol Selection Criteria

✅ **2+ years operational**  
✅ **$1B+ TVL**  
✅ **3+ independent audits**  
✅ **Open source**  
✅ **Active development**

## Yield Calculation

### Blended APY

```javascript
const blendedAPY =
  (0.40 × 5.0) +   // Aave: 2.0%
  (0.30 × 4.5) +   // Lido: 1.35%
  (0.30 × 18.0);   // Uniswap: 5.4%

= 8.75% total APY
```

### Real-World Example

```
User deposits: 100 ETH
After 1 year:

Aave earnings:   40 ETH × 5%  = 2.0 ETH
Lido earnings:   30 ETH × 4.5% = 1.35 ETH
Uniswap earnings: 30 ETH × 18% = 5.4 ETH
─────────────────────────────────────────
Total earnings: 8.75 ETH

Final balance: 108.75 ETH (8.75% return)
```

## Comparison with Alternatives

| Approach           | APY   | Risk    | Diversification |
| ------------------ | ----- | ------- | --------------- |
| **Veilfi**         | 8.75% | 2.95/10 | ✅ 3 protocols  |
| **Single Aave**    | 5%    | 2/10    | ❌ None         |
| **Single Uniswap** | 18%   | 5/10    | ❌ None         |
| **Yearn**          | 9%    | 4/10    | ✅ Multiple     |
| **Manual**         | 12%   | 7/10    | ⚠️ User managed |

---

**Next**: [Compliant KYC System](./compliant-kyc-system) - Privacy-preserving compliance.
