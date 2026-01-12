---
title: Automated Yield Optimization
sidebar_position: 4
---

# Automated Yield Optimization

Veilfi automatically manages capital allocation, harvesting, and compounding to maximize returns without user intervention.

## Set and Forget

```
You deposit → Veilfi handles everything → You earn

No manual:
❌ APY monitoring
❌ Rebalancing
❌ Yield harvesting
❌ Compounding
```

## Automation Features

### Auto-Allocation (Instant)

```solidity
function deposit() external payable {
    _mint(msg.sender, shares);

    // Automatically allocate
    aaveStrategy.deposit{value: msg.value * 40 / 100}();
    lidoStrategy.deposit{value: msg.value * 30 / 100}();
    uniswapStrategy.deposit{value: msg.value * 30 / 100}();
}
```

### Auto-Harvesting (Weekly)

```solidity
function autoHarvest() external {
    for (uint i = 0; i < strategies.length; i++) {
        totalYield += strategies[i].harvest();
    }
}
```

### Auto-Compounding

Yields reinvested automatically - share price increases.

### Auto-Rebalancing

When allocations drift, automatically rebalanced to 40/30/30.

---

**Next**: [Transparent On-Chain Verification](./transparent-on-chain-verification)
