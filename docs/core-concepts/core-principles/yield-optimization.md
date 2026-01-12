---
title: Yield Optimization
sidebar_position: 2
---

# Yield Optimization

Veilfi maximizes returns through **intelligent capital allocation**, **automated rebalancing**, and **multi-strategy diversification** while maintaining complete privacy.

## Core Strategy

### Multi-Protocol Aggregation

Deploy capital across protocols simultaneously:

| Strategy       | Target APY | Risk Level | Allocation |
| -------------- | ---------- | ---------- | ---------- |
| **Aave**       | 3-8%       | 🟢 Low     | 40%        |
| **Lido**       | 4-5%       | 🟢 Low     | 30%        |
| **Uniswap LP** | 10-30%     | 🟡 Medium  | 30%        |

**Blended APY**: ~7-12% (vs. 5% single-protocol)

### Automated Rebalancing

Admin monitors yields and reallocates:

```
Weekly Check:
If Aave APY > Uniswap APY + 2%:
  → Shift 10% from Uniswap to Aave

If Lido APY < 3%:
  → Reduce Lido allocation, increase others
```

**User Benefit**: Professional management, zero effort, no additional gas fees.

### Compounding

Yields automatically reinvested:

```
Month 1: 100 ETH earning 7% = 0.58 ETH yield
Month 2: 100.58 ETH earning 7% = 0.59 ETH yield
Month 12: ~107 ETH (compounded)

vs.

Simple interest: 100 ETH + (7% * 1 year) = 107 ETH
No compounding advantage for short periods, significant over years
```

## Optimization Techniques

### 1. Dynamic Allocation

Responds to market conditions:

```solidity
function rebalance() external onlyOwner {
    uint256[] memory apys = getStrategyAPYs();

    // Find best performing strategy
    uint256 bestIdx = findMax(apys);

    // Increase allocation to best performer
    allocations[bestIdx] += 5%;
    // Decrease worst performer
    allocations[worstIdx] -= 5%;
}
```

### 2. Gas Optimization

Batch operations to save user fees:

- Single deposit → auto-allocated to 3 protocols (1 tx instead of 3)
- Harvesting done by protocol (users pay nothing)
- Withdrawals optimized (pull from best liquidity source)

### 3. Risk-Adjusted Returns

Not just highest APY, but best risk/reward:

```
Strategy A: 15% APY, 🔴 High risk (new protocol)
Strategy B: 7% APY, 🟢 Low risk (Aave, battle-tested)

Veilfi chooses: Strategy B (safer 7% > riskier 15%)
```

---

**Next**: [Compliance Friendly](./compliance-friendly)
