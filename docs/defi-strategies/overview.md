---
title: DeFi Strategies Overview
sidebar_position: 1
---

# DeFi Strategies Overview

Veilfi deploys capital across multiple battle-tested DeFi protocols to generate diversified, risk-adjusted yields while maintaining user privacy.

## Strategy Philosophy

### Diversification Over Maximization

```
❌ Wrong Approach: Chase highest APY (e.g., 200% on new protocol)
✅ Veilfi Approach: Balanced portfolio across proven protocols (7-12% blended)

Why: Sustainable returns > risky high yields
```

### Three-Protocol Foundation

| Strategy             | Protocol     | Type                | Target APY | Allocation |
| -------------------- | ------------ | ------------------- | ---------- | ---------- |
| **Aave Strategy**    | Aave V3      | Lending             | 3-8%       | 40%        |
| **Lido Strategy**    | Lido Finance | ETH Staking         | 4-5%       | 30%        |
| **Uniswap Strategy** | Uniswap V3   | Liquidity Provision | 10-30%     | 30%        |

**Blended APY**: ~7-12% (depending on market conditions)

## Strategy Categories

### 1. Lending Protocols (Aave)

**Mechanism**: Supply assets, earn interest from borrowers.

```
User deposits → Aave lending pool → Borrowers pay interest
                                  → Lenders receive yield
```

**Characteristics**:

- 🟢 Low risk (battle-tested, $10B+ TVL)
- 🟢 Predictable yields (3-8% APY)
- 🟢 High liquidity (instant withdrawals)
- 🟡 Lower APY than other strategies

### 2. Staking (Lido)

**Mechanism**: Stake ETH, earn network validation rewards.

```
User deposits → Lido stakes on Ethereum → Receives stETH (rebasing token)
                                        → Earns 4-5% APY from validators
```

**Characteristics**:

- 🟢 Very low risk (Ethereum network security)
- 🟢 Stable yields (4-5% APY)
- 🟢 Liquid staking (stETH tradable)
- 🟡 Slightly lower returns

### 3. Liquidity Provision (Uniswap)

**Mechanism**: Provide liquidity to DEX, earn trading fees.

```
User deposits → Uniswap V3 pool → Traders pay 0.3% fees
                                → LPs receive fee share
```

**Characteristics**:

- 🟡 Medium risk (impermanent loss possible)
- 🟢 Higher yields (10-30% APY)
- 🟡 Variable returns (depends on volume)
- 🔴 Impermanent loss exposure

## Current Strategy Portfolio

### Allocation Breakdown

```
Total Vault: 1,000 ETH
│
├─ 400 ETH (40%) → Aave Strategy
│   └─ Earning: 5% APY = 20 ETH/year
│
├─ 300 ETH (30%) → Lido Strategy
│   └─ Earning: 4.5% APY = 13.5 ETH/year
│
└─ 300 ETH (30%) → Uniswap Strategy
    └─ Earning: 12% APY = 36 ETH/year

Total Annual Yield: 69.5 ETH (~6.95% blended APY)
```

### Risk-Adjusted Returns

| Metric         | Aave      | Lido  | Uniswap | **Blended** |
| -------------- | --------- | ----- | ------- | ----------- |
| **APY**        | 5%        | 4.5%  | 12%     | **6.95%**   |
| **Risk Score** | 2/10      | 2/10  | 5/10    | **3/10**    |
| **Liquidity**  | Very High | High  | Medium  | **High**    |
| **TVL**        | $10B+     | $30B+ | $5B+    | -           |

**Veilfi Advantage**: Lower risk than Uniswap alone, higher yield than Aave alone.

## Strategy Selection Criteria

### Must-Have Requirements

✅ **Battle-Tested**: Protocol operational for 2+ years  
✅ **High TVL**: $1B+ locked (liquidity assurance)  
✅ **Audited**: Multiple security audits from reputable firms  
✅ **Ethereum-Native**: Deployed on Ethereum or compatible L2s  
✅ **Open Source**: Verifiable smart contracts

### Evaluation Matrix

| Protocol       | Years Live | TVL   | Audits | Compatible | Score           |
| -------------- | ---------- | ----- | ------ | ---------- | --------------- |
| **Aave V3**    | 4+         | $10B+ | ✅ 10+ | ✅ Yes     | ⭐⭐⭐⭐⭐      |
| **Lido**       | 3+         | $30B+ | ✅ 15+ | ✅ Yes     | ⭐⭐⭐⭐⭐      |
| **Uniswap V3** | 3+         | $5B+  | ✅ 8+  | ✅ Yes     | ⭐⭐⭐⭐⭐      |
| New DeFi X     | 0.5        | $100M | ⚠️ 1   | ✅ Yes     | ⭐⭐ (rejected) |

**Rejection Criteria**: New DeFi X fails "Battle-Tested" and "High TVL" requirements.

## Yield Generation Mechanisms

### Aave: Interest Rate Model

```solidity
// Simplified Aave yield calculation
utilizationRate = totalBorrows / totalLiquidity
baseRate = 0.03 (3%)
slope1 = 0.04 (4%)

if (utilizationRate < 0.8) {
    supplyAPY = baseRate + (utilizationRate * slope1)
} else {
    supplyAPY = baseRate + slope1 + (utilizationRate - 0.8) * slope2
}

// Example: 50% utilization
supplyAPY = 3% + (0.5 * 4%) = 5% APY
```

### Lido: Staking Rewards

```
Ethereum Network Staking:
├─ Base Reward: ~4% annual
├─ MEV Rewards: ~0.5% annual
└─ Priority Fees: ~0.2% annual
────────────────────────────
Total stETH APY: ~4.7%

Lido takes 10% fee:
User receives: ~4.2% net APY
```

### Uniswap: Trading Fees

```
Pool: ETH/USDC (0.3% fee tier)
Daily Volume: $10M
LP Position: $100k (1% of pool)

Daily fees = $10M * 0.003 = $30,000
LP share = $30,000 * 0.01 = $300/day

Annual return = $300 * 365 = $109,500
APY = $109,500 / $100,000 = 109.5%

Note: High APY comes with impermanent loss risk!
```

## Strategy Lifecycle

### 1. Initial Deployment

```
Week 0: Launch with 2 strategies (Aave + Lido)
Week 4: Add Uniswap strategy (after testing)
Week 8: Optimize allocations based on performance
```

### 2. Active Management

**Weekly Tasks**:

- Monitor APYs across all strategies
- Check for security incidents
- Harvest yields
- Rebalance if APY delta &gt; 5%

**Monthly Tasks**:

- Review allocation percentages
- Evaluate new strategy candidates
- Performance reporting

### 3. Emergency Procedures

```
If strategy exploit detected:
1. Pause deposits to affected strategy
2. Withdraw all assets immediately
3. Reallocate to safe strategies
4. Notify users via Discord/Twitter
5. Post-mortem analysis
```

## Performance Metrics

### Historical Performance (Simulated)

| Month   | Aave APY | Lido APY  | Uniswap APY | Blended APY |
| ------- | -------- | --------- | ----------- | ----------- |
| Jan     | 4.5%     | 4.3%      | 15%         | 7.2%        |
| Feb     | 5.2%     | 4.5%      | 12%         | 6.8%        |
| Mar     | 5.8%     | 4.4%      | 10%         | 6.5%        |
| Apr     | 6.1%     | 4.6%      | 8%          | 6.1%        |
| **Avg** | **5.4%** | **4.45%** | **11.25%**  | **6.65%**   |

### Comparison with Alternatives

| Vault          | APY | Risk      | Privacy     | Management |
| -------------- | --- | --------- | ----------- | ---------- |
| **Veilfi**     | 7%  | 🟢 Low    | ✅ ZK-based | Auto       |
| Yearn Finance  | 8%  | 🟡 Medium | ❌ Public   | Auto       |
| Beefy Finance  | 9%  | 🟡 Medium | ❌ Public   | Auto       |
| Manual Farming | 12% | 🔴 High   | ❌ Public   | Manual     |

**Veilfi Trade-off**: Slightly lower APY for significantly better risk profile + privacy.

## Future Strategy Roadmap

### Phase 1 (Current)

- ✅ Aave V3 integration
- ✅ Lido integration
- ✅ Uniswap V3 integration

### Phase 2 (Q2 2024)

- 🔄 Compound V3 integration
- 🔄 Curve Finance integration
- 🔄 Dynamic rebalancing algorithm

### Phase 3 (Q3 2024)

- ⏳ Convex Finance integration
- ⏳ GMX perpetuals strategy
- ⏳ Cross-chain strategies (Arbitrum, Optimism)

### Phase 4 (Q4 2024)

- ⏳ AI-driven allocation optimization
- ⏳ Custom strategy creation (governance)
- ⏳ Strategy marketplace

## Strategy Constraints

### Protocol Limits

- **Maximum Strategies**: 10 simultaneous
- **Max Allocation per Strategy**: 50%
- **Minimum Strategy TVL**: $1B
- **Minimum Audit Count**: 3 independent audits

### Gas Optimization

```
Single strategy interaction: ~150k gas
Multi-strategy batch: ~350k gas (not 450k)

Savings: ~150k gas = ~30% efficiency gain
```

## Key Takeaways

1. **Diversification is key** - No single protocol gets &gt;50% allocation
2. **Safety over yield** - Only battle-tested protocols (2+ years, $1B+ TVL)
3. **Active management** - Weekly monitoring, monthly rebalancing
4. **Privacy maintained** - All strategies integrated with ZK proof layer
5. **User-friendly** - Automated yield collection and compounding

---

**Next Steps**:

- [Supported Protocols](./supported-protocols/aave-strategy) - Detailed protocol integrations
- [Yield Optimization](./yield-optimization/auto-rebalancing) - How yields are maximized
