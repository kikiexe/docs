---
title: Yield Aggregation
sidebar_position: 1
---

# Yield Aggregation

Yield aggregation is the practice of **deploying capital across multiple DeFi protocols simultaneously** to maximize returns while diversifying risk. Veilfi automates this process with an added privacy layer.

## What is Yield Aggregation?

### Traditional Approach (Manual)

Without aggregation, users must:

1. **Research protocols** individually (Aave, Lido, Uniswap, etc.)
2. **Deposit separately** to each protocol (multiple transactions)
3. **Monitor yields** across multiple dashboards
4. **Rebalance manually** when APYs change
5. **Claim rewards** from each protocol (high gas costs)

**Result**: Time-consuming, expensive, and inefficient.

### Aggregated Approach (Veilfi)

With Veilfi's aggregation:

1. **Single deposit** to the vault
2. **Auto-allocation** to best-performing strategies
3. **Unified monitoring** via one dashboard
4. **Automatic rebalancing** by protocol admins
5. **Compounded yields** reinvested automatically

**Result**: Passive income with professional-grade optimization.

## How Veilfi Aggregates Yield

### Architecture Overview

```
User Deposit (10 ETH)
        ↓
┌───────────────────────┐
│   StrategyVaultV2     │ ← Central coordinator
└───────────────────────┘
        ↓
  Auto-Allocation:
  ├─ 40% → Aave Strategy (4 ETH)
  ├─ 30% → Lido Strategy (3 ETH)
  └─ 30% → Uniswap Strategy (3 ETH)
        ↓
  Each strategy earns yield
        ↓
  Yields flow back to vault
        ↓
  User shares appreciate in value
```

### Multi-Strategy Vault

Veilfi's vault implements **ERC-4626 standard** with extensions:

```solidity
contract StrategyVaultV2_Multi is ERC4626 {
    IStrategy[] public strategies;

    // Allocate user deposits to strategies
    function allocateToStrategies() external onlyOwner {
        uint256 totalAssets = totalAssets();

        // Example: 40/30/30 split
        strategies[0].deposit(totalAssets * 40 / 100); // Aave
        strategies[1].deposit(totalAssets * 30 / 100); // Lido
        strategies[2].deposit(totalAssets * 30 / 100); // Uniswap
    }

    // Harvest yields from all strategies
    function harvestYields() external onlyOwner {
        for (uint i = 0; i < strategies.length; i++) {
            strategies[i].harvest();
        }
    }
}
```

## Benefits of Aggregation

### 1. Higher Returns Through Diversification

Instead of choosing one protocol, earn from multiple:

| Single Protocol         | Aggregated (Veilfi) |
| ----------------------- | ------------------- |
| Aave only: 5% APY       | Blended: ~7% APY    |
| Lido only: 4.5% APY     | **+40% more yield** |
| Uniswap only: 12% APY\* | Lower risk exposure |

\*_Uniswap LP has impermanent loss risk; diversification mitigates this_

### 2. Risk Mitigation

**Single Protocol Risk**:

```
All 10 ETH in Aave
↓
Aave gets exploited
↓
Lose 100% of funds
```

**Diversified Risk** (Veilfi):

```
4 ETH in Aave, 3 ETH in Lido, 3 ETH in Uniswap
↓
Aave gets exploited
↓
Lose only 40% of funds (4 ETH)
Remaining 60% (6 ETH) safe
```

**Impact**: Risk is spread, not eliminated, but significantly reduced.

### 3. Gas Efficiency

**Manual Multi-Protocol Farming**:

```
Deposit to Aave:     ~$15 gas
Deposit to Lido:     ~$20 gas
Deposit to Uniswap:  ~$25 gas
Monthly rebalance:   ~$60 gas
─────────────────────────────
Total: ~$120/month
```

**Veilfi Aggregation**:

```
Single deposit:      ~$18 gas
Auto-allocation:     FREE (admin pays)
Auto-rebalance:      FREE (admin pays)
─────────────────────────────
Total: ~$18/month (85% savings)
```

### 4. Professional Strategy Management

**Amateur Approach**:

- Manual yield tracking
- Delayed rebalancing (miss opportunities)
- Emotional decisions (FOMO, panic)

**Veilfi Approach**:

- Real-time yield monitoring
- Algorithm-driven rebalancing
- Emotionless optimization

## Yield Aggregation + Privacy

### Traditional Aggregators (Yearn, Beefy)

**Problem**: Deposits are fully transparent.

```solidity
// Public vault - everyone can see balances
mapping(address => uint256) public balanceOf;

// When you deposit 10 ETH, it's PUBLIC
function deposit(uint256 amount) public {
    balanceOf[msg.sender] += amount; // ← EXPOSED!
}
```

**Result**: High yield, zero privacy.

### Veilfi's Privacy-First Aggregation

**Solution**: ZK proofs hide deposit amounts.

```solidity
// Private vault - balances cryptographically hidden
mapping(address => bool) private isDepositor;

// When you deposit 10 ETH, amount is HIDDEN
function depositWithProof(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[3] memory publicSignals
) external payable {
    // Verify proof WITHOUT seeing deposit amount
    require(zkVerifier.verifyProof(a, b, c, publicSignals));

    // Process deposit privately
    _mint(msg.sender, shares); // Shares minted, amount unknown to public
}
```

**Result**: High yield + privacy = Veilfi's innovation.

## Key Terminology

### Total Value Locked (TVL)

The total amount of capital deposited in the vault.

```javascript
TVL = sum of all user deposits - total withdrawals
```

**Example**: If 100 users deposit 10 ETH each = 1,000 ETH TVL.

### Share Price

The value of one vault share in underlying assets.

```javascript
sharePrice = totalAssets() / totalSupply();
```

**Example**:

- Vault has 1,000 ETH assets
- Vault has 900 shares outstanding
- Share price = 1,000 / 900 = 1.111 ETH per share

As yields accumulate, share price increases.

### Annual Percentage Yield (APY)

The annualized rate of return including compounding.

```javascript
APY = (1 + periodicRate) ^ (periods - 1);
```

**Example**:

- Daily rate: 0.019% (7% annually)
- APY = (1.00019)^365 - 1 = 7.25% (compounding effect)

### Blended APY

The weighted average yield across all strategies.

```javascript
Blended APY = (Aave_APY × 40%) + (Lido_APY × 30%) + (Uniswap_APY × 30%)
```

**Example**:

```
= (5% × 0.40) + (4.5% × 0.30) + (12% × 0.30)
= 2.0% + 1.35% + 3.6%
= 6.95% blended APY
```

## Comparison with Alternatives

| Approach                        | Yield | Risk      | Effort  | Privacy         |
| ------------------------------- | ----- | --------- | ------- | --------------- |
| **Single Protocol** (Aave only) | 5%    | 🔴 High   | 🟢 Low  | ❌ None         |
| **Manual Multi-Protocol**       | 7%+   | 🟡 Medium | 🔴 High | ❌ None         |
| **Yearn/Beefy Aggregator**      | 8%+   | 🟡 Medium | 🟢 Low  | ❌ None         |
| **🎯 Veilfi Aggregator**        | 7-8%  | 🟡 Medium | 🟢 Low  | ✅ **ZK-based** |

**Veilfi's Edge**: Only aggregator with built-in privacy.

## Real-World Example

**Alice's Journey**:

**Month 0** (Initial Deposit):

```
Alice deposits: 100 ETH
Vault allocates:
├─ 40 ETH → Aave (5% APY)
├─ 30 ETH → Lido (4.5% APY)
└─ 30 ETH → Uniswap (12% APY)

Alice receives: 100 vault shares
Share price: 1.0 ETH per share
```

**Month 1** (Yields Earned):

```
Yields generated:
├─ Aave:    40 ETH × 5% / 12 = 0.167 ETH
├─ Lido:    30 ETH × 4.5% / 12 = 0.113 ETH
└─ Uniswap: 30 ETH × 12% / 12 = 0.300 ETH
Total yield: 0.580 ETH

New vault total: 100.580 ETH
Alice's shares: still 100
New share price: 100.580 / 100 = 1.0058 ETH

Alice's value: 100 shares × 1.0058 = 100.58 ETH (+0.58%)
```

**Month 12** (After compounding):

```
Compounded blended APY: ~7%
Alice's final value: 100 × 1.07 = 107 ETH
Profit: 7 ETH (~$14,000 at $2k/ETH)

Privacy maintained: Outsiders never saw her 100 ETH deposit
```

## Limitations of Yield Aggregation

### What Aggregation Doesn't Solve

❌ **Smart contract risk**: All strategies carry code risk  
❌ **Market risk**: DeFi yields fluctuate with market conditions  
❌ **Impermanent loss**: Uniswap LP positions can lose value  
❌ **Regulatory risk**: DeFi regulations may change

### Veilfi-Specific Considerations

⚠️ **Admin trust**: Allocation decisions made by protocol owners (future: DAO)  
⚠️ **Rebalancing delay**: Not instant (admin must execute)  
⚠️ **Gas overhead**: ZK proofs cost ~2x more gas than standard deposits  
⚠️ **Withdrawal timing**: May require strategy liquidation (not instant)

---

**Next**: Learn about [Zero-Knowledge Proofs](./zero-knowledge-proofs) that power Veilfi's privacy layer.
