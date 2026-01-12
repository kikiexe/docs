---
title: How Yields are Distributed
sidebar_position: 2
---

# How Yields are Distributed

Veilfi distributes yields through **share price appreciation**, ensuring fair and proportional returns for all depositors regardless of deposit timing.

## Distribution Model: ERC-4626

### Share-Based System

```
User deposits X ETH → Receives Y shares
Share value = totalAssets / totalShares
```

**Example**:

```
Vault has 1000 ETH, 900 shares outstanding
Share price = 1000 / 900 = 1.111 ETH per share

Alice deposits 10 ETH:
Shares minted = 10 / 1.111 = 9 shares
```

### Yield Accrual

As yields compound, share price increases:

```
Week 0: Share price = 1.000 ETH
Week 1: +0.5% yield → Share price = 1.005 ETH
Week 4: +2% cumulative → Share price = 1.020 ETH
```

**User's Value**:

```
Alice has 9 shares
Week 0: 9 × 1.000 = 9 ETH
Week 4: 9 × 1.020 = 9.18 ETH (+0.18 ETH yield)
```

## Fee Structure

### Management Fee: 1% Annual

Deducted from yields before distribution:

```
Gross Yield: 7% APY
Management Fee: 1% APY
Net to Users: 6% APY
```

### Performance Fee: 10% of Profits

Only charged on gains:

```
User earns 1 ETH profit
Performance fee: 0.1 ETH (10%)
User keeps: 0.9 ETH (90%)
```

### No Deposit/Withdrawal Fees

```
Deposit: FREE
Management: 1% annual
Performance: 10% of profits
Withdrawal: FREE (except 0.1% anti-manipulation)
```

## Yield Distribution Examples

### Example 1: Early Depositor

```
Alice deposits 100 ETH on Day 1
Receives: 100 shares (1:1 ratio initially)

After 1 year:
Total vault yields: 7%
Share price: 1.00 → 1.07 ETH

Alice's value:
100 shares × 1.07 = 107 ETH
Gross profit: 7 ETH
After fees (1% mgmt + 10% perf): ~6.3 ETH net
```

### Example 2: Late Depositor

```
Bob deposits 100 ETH on Day 180 (mid-year)
Share price at deposit: 1.035 ETH
Receives: 100 / 1.035 = 96.6 shares

After 6 months:
Share price: 1.035 → 1.07 ETH

Bob's value:
96.6 shares × 1.07 = 103.4 ETH
Profit: 3.4 ETH (pro-rated for 6 months)
```

**Fairness**: Late depositors get fewer shares at higher price = proportional returns.

## Compounding

### Auto-Compounding

Yields automatically reinvested:

```
Month 1: 100 ETH earning 7% = 0.58 ETH
         → Reinvested → 100.58 ETH base
Month 2: 100.58 ETH earning 7% = 0.59 ETH
         → Reinvested → 101.17 ETH base
...
Month 12: ~107.23 ETH (compounded)

vs.

Simple interest: 107 ETH
Compound advantage: +0.23 ETH
```

### APY vs APR

- **APR (Annual Percentage Rate)**: 7% simple
- **APY (Annual Percentage Yield)**: 7.25% compounded

Veilfi displays **APY** (true returns including compounding).

## Withdrawal Mechanics

### Fair Value Calculation

```solidity
function withdraw(uint256 shares) external {
    // Current share price
    uint256 price = totalAssets() / totalShares();

    // ETH value of shares
    uint256 ethValue = shares * price / 1e18;

    // Burn shares, return ETH
    _burn(msg.sender, shares);
    payable(msg.sender).transfer(ethValue);
}
```

**Guarantee**: Users always get proportional vault value at withdrawal time.

---

**Next**: [Strategy Allocation](./strategy-allocation)
