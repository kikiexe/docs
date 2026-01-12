---
title: Uniswap Strategy
sidebar_position: 3
---

# Uniswap Strategy

Uniswap V3 provides concentrated liquidity and trading fee earnings, offering Veilfi's highest APY potential with controlled impermanent loss risk.

## Protocol Overview

**Uniswap V3**: Leading decentralized exchange with concentrated liquidity.

- **TVL**: $5B+
- **Years Live**: 3+ (V3 launched May 2021)
- **Audits**: 8+ including ABDK, Trail of Bits, Consensys
- **Daily Volume**: $1-3B

## How It Works

### Concentrated Liquidity

Unlike Uniswap V2 (full range), V3 allows capital concentration:

```
V2 Approach:
Provide liquidity: $0 - $∞
Capital efficiency: Low

V3 Approach:
Provide liquidity: $1,800 - $2,200 (concentrated range)
Capital efficiency: 4x-10x higher
Trading fees: 3x-5x more per dollar
```

### Fee Tiers

| Fee Tier  | Best For                      | Volume    | APY Potential |
| --------- | ----------------------------- | --------- | ------------- |
| 0.01%     | Stablecoin pairs              | Very High | 5-15%         |
| 0.05%     | Correlated assets (ETH/stETH) | High      | 10-20%        |
| **0.30%** | **ETH/USDC (Veilfi uses)**    | **High**  | **15-30%**    |
| 1.00%     | Exotic pairs                  | Low       | 20-50%        |

## Smart Contract Integration

### Mock Uniswap Strategy

```solidity
contract MockUniswapStrategy is IStrategy {
    INonfungiblePositionManager public positionManager;
    IUniswapV3Pool public pool;

    uint256 public tokenId;  // LP position NFT ID
    uint256 public totalDeposited;

    // Price range for concentrated liquidity
    int24 public tickLower = -887220;  // ~$1,800 per ETH
    int24 public tickUpper = 887220;   // ~$2,200 per ETH

    function deposit() external payable override onlyVault returns (uint256) {
        require(msg.value > 0, "Zero deposit");

        // Mint new LP position
        INonfungiblePositionManager.MintParams memory params =
            INonfungiblePositionManager.MintParams({
                token0: address(WETH),
                token1: address(USDC),
                fee: 3000,  // 0.3% fee tier
                tickLower: tickLower,
                tickUpper: tickUpper,
                amount0Desired: msg.value,
                amount1Desired: 0,  // Single-sided liquidity
                amount0Min: 0,
                amount1Min: 0,
                recipient: address(this),
                deadline: block.timestamp
            });

        (tokenId, , , ) = positionManager.mint(params);

        totalDeposited += msg.value;

        emit Deposited(msg.value);
        return msg.value;
    }

    function withdraw(uint256 amount) external override onlyVault returns (uint256) {
        // Decrease liquidity
        uint128 liquidity = _calculateLiquidityToRemove(amount);

        positionManager.decreaseLiquidity(
            INonfungiblePositionManager.DecreaseLiquidityParams({
                tokenId: tokenId,
                liquidity: liquidity,
                amount0Min: 0,
                amount1Min: 0,
                deadline: block.timestamp
            })
        );

        // Collect tokens
        (uint256 amount0, uint256 amount1) = positionManager.collect(
            INonfungiblePositionManager.CollectParams({
                tokenId: tokenId,
                recipient: address(vault),
                amount0Max: type(uint128).max,
                amount1Max: type(uint128).max
            })
        );

        totalDeposited -= amount;
        return amount0 + _convertUSDCToETH(amount1);
    }

    function harvest() external override onlyVault returns (uint256) {
        // Collect accumulated trading fees
        (uint256 amount0, uint256 amount1) = positionManager.collect(
            INonfungiblePositionManager.CollectParams({
                tokenId: tokenId,
                recipient: address(this),
                amount0Max: type(uint128).max,
                amount1Max: type(uint128).max
            })
        );

        // Convert USDC fees to ETH
        uint256 totalETH = amount0 + _convertUSDCToETH(amount1);

        // Send to vault
        payable(vault).transfer(totalETH);

        return totalETH;
    }

    function totalAssets() external view override returns (uint256) {
        (uint256 amount0, uint256 amount1) = _getPositionAmounts();
        return amount0 + _convertUSDCToETH(amount1);
    }

    function apy() external view override returns (uint256) {
        // Calculate APY from 24h fee data
        uint256 dailyFees = _getDailyFees();
        uint256 currentValue = this.totalAssets();

        // Annualize: dailyFees * 365 / currentValue
        return (dailyFees * 365 * 10000) / currentValue;  // in basis points
    }
}
```

## Yield Characteristics

### APY Breakdown

```
Example Position: $100k in ETH/USDC (0.3% fee)

Daily Trading Volume: $10M
Daily Fees Generated: $10M × 0.003 = $30,000

LP Pool Share: 1% ($100k / $10M TVL)
LP Daily Fees: $30,000 × 0.01 = $300

Annual Fees: $300 × 365 = $109,500
APY: $109,500 / $100,000 = 109.5%

Minus Impermanent Loss: ~10-15%
Net APY: ~90-100%

Realistic APY (lower volume): 15-30%
```

### Variable Returns

| Market Condition  | Volume    | Fee APY | IL Impact  | Net APY    |
| ----------------- | --------- | ------- | ---------- | ---------- |
| **Bull Market**   | Very High | 40-50%  | -5 to -10% | **30-40%** |
| **Normal Market** | Medium    | 20-30%  | -3 to -5%  | **15-25%** |
| **Bear Market**   | Low       | 10-15%  | -2 to -3%  | **8-12%**  |

**Veilfi Average**: ~12-18% APY (conservative estimate)

## Risk Profile

### Impermanent Loss

**What is IL?**
When asset prices diverge, LPs lose value vs. holding assets:

```
Scenario:
Initial: 1 ETH ($2,000) + 2,000 USDC
Total Value: $4,000

ETH doubles to $4,000:
--- Holding: 1 ETH ($4,000) + 2,000 USDC = $6,000
--- LP Position: 0.707 ETH ($2,828) + 2,828 USDC = $5,656
--- IL: $6,000 - $5,656 = $344 loss (5.7%)

But earned fees: $500
Net Gain: $500 - $344 = $156 profit ✅
```

### IL Mitigation Strategies

1. **Concentrated Ranges**: Narrower range = more fees, but more IL risk
2. **Fee Compensation**: High fees offset IL
3. **Correlated Pairs**: ETH/stETH has minimal IL
4. **Active Management**: Rebalance when price exits range

### Overall Risk

| Risk Type            | Level     | Mitigation             |
| -------------------- | --------- | ---------------------- |
| **Impermanent Loss** | 🟡 Medium | Fee earnings offset    |
| **Smart Contract**   | 🟢 Low    | Audited, battle-tested |
| **Liquidity**        | 🟢 Low    | $5B+ TVL               |
| **Price Range**      | 🟡 Medium | Monitor & rebalance    |

**Overall**: 🟡 Medium Risk (5/10)

## Position Management

### Range Selection

```solidity
// Current ETH price: $2,000
// Target range: ±20%

tickLower = priceToTick($1,600);  // Lower bound
tickUpper = priceToTick($2,400);  // Upper bound

// If ETH &lt; $1,600 or &gt; $2,400:
// → Position goes "out of range"
// → Stop earning fees until price returns
```

### Rebalancing Trigger

```
IF price exits range (±20%):
  1. Withdraw liquidity
  2. Recalculate optimal range
  3. Redeposit to new range

Gas cost: ~$50-100
Frequency: Once per month (typical)
```

## Performance Metrics

### Veilfi Allocation

- **Current Allocation**: 30% of total vault
- **Rationale**: Highest APY, but controlled exposure due to IL risk
- **Target Range**: 20-40%

### Historical Performance

```
Month 1: 18% APY (bull market, high volume)
Month 2: 12% APY (normal market)
Month 3: 25% APY (volatility spike)
Month 4: 10% APY (bear market)

Average: 16.25% APY
```

## Liquidity

### Withdrawal Process

```
1. Decrease liquidity (remove from pool)
2. Collect tokens (ETH + USDC)
3. Swap USDC → ETH if needed
4. Transfer to vault

Timeline: Instant (on-chain)
Slippage: 0.1-0.5% (during swap)
```

---

**Next**: [Performance Tracking](../performance-tracking/apy-monitoring) - How yields are measured.
