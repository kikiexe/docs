---
title: Aave Strategy
sidebar_position: 1
---

# Aave Strategy

Aave V3 is Veilfi's primary lending strategy, providing stable, low-risk yields through supplying assets to the world's leading DeFi lending protocol.

## Protocol Overview

**Aave**: Decentralized lending and borrowing protocol.

- **TVL**: $10B+
- **Years Live**: 4+ (launched 2020)
- **Audits**: 10+ from Trail of Bits, OpenZeppelin, ABDK, Consensys
- **Chain**: Ethereum, Polygon, Arbitrum, Optimism

## How It Works

### Lending Mechanism

```
1. Veilfi deposits ETH to Aave
   ↓
2. Aave mints aETH (interest-bearing token)
   ↓
3. aETH balance increases over time (rebasing)
   ↓
4. Veilfi harvests yield by withdrawing excess aETH
   ↓
5. Yield returned to vault, distributed to users
```

### Interest Rate Model

Aave uses algorithmic interest rates:

```
Utilization Rate = Total Borrows / Total Liquidity

Supply APY = Base Rate + (Utilization × Variable Rate)

Example:
- Base Rate: 2%
- Utilization: 60%
- Variable Rate: 5%
- Supply APY: 2% + (0.6 × 5%) = 5%
```

## Smart Contract Integration

### Mock Aave Strategy

```solidity
contract MockAaveStrategy is IStrategy {
    IAavePool public aavePool;
    IERC20 public aToken;
    address public vault;

    uint256 public totalDeposited;

    function deposit() external payable override onlyVault returns (uint256) {
        require(msg.value > 0, "Zero deposit");

        // Supply ETH to Aave
        aavePool.supply{value: msg.value}(
            address(WETH),
            msg.value,
            address(this),
            0  // referral code
        );

        totalDeposited += msg.value;

        emit Deposited(msg.value);
        return msg.value;
    }

    function withdraw(uint256 amount) external override onlyVault returns (uint256) {
        // Withdraw from Aave
        uint256 withdrawn = aavePool.withdraw(
            address(WETH),
            amount,
            address(vault)
        );

        totalDeposited -= amount;

        return withdrawn;
    }

    function harvest() external override onlyVault returns (uint256) {
        // Calculate yield
        uint256 currentBalance = aToken.balanceOf(address(this));
        uint256 yield = currentBalance - totalDeposited;

        if (yield > 0) {
            // Withdraw only the yield
            aavePool.withdraw(address(WETH), yield, address(vault));
        }

        return yield;
    }

    function totalAssets() external view override returns (uint256) {
        return aToken.balanceOf(address(this));
    }

    function apy() external view override returns (uint256) {
        // Get current supply APY from Aave
        return aavePool.getReserveData(address(WETH)).currentLiquidityRate / 1e25;
    }
}
```

## Yield Characteristics

### APY Range

| Market Condition | Utilization | Supply APY |
| ---------------- | ----------- | ---------- |
| Bear Market      | 30-40%      | 2-3%       |
| Normal Market    | 50-60%      | 4-6%       |
| Bull Market      | 70-80%      | 6-8%       |

**Average**: 4-5% APY

### Yield Sources

1. **Borrower Interest**: Main yield source
2. **Flash Loan Fees**: 0.09% of flash loan volume
3. **Liquidation Bonuses**: Small percentage

## Risk Profile

### Security

✅ **Audited**: 10+ independent audits  
✅ **Battle-Tested**: 4+ years, no major exploits  
✅ **Insurance**: $50M+ in Aave Safety Module  
✅ **Bug Bounty**: Up to $1M for critical bugs

### Risks

⚠️ **Smart Contract Risk**: Code vulnerability (low probability)  
⚠️ **Oracle Risk**: Price feed manipulation (mitigated by Chainlink)  
⚠️ **Liquidation Risk**: Systemic market crash (low for lenders)

**Overall Risk**: 🟢 Very Low (2/10)

## Performance Metrics

### Historical APY (2023)

```
Jan: 4.2%  │██████████████
Feb: 4.8%  │████████████████
Mar: 5.1%  │█████████████████
Apr: 5.5%  │██████████████████
May: 4.9%  │████████████████
Jun: 4.3%  │██████████████
```

**Average**: 4.8% APY

### Veilfi Allocation

- **Current Allocation**: 40% of total vault
- **Rationale**: Largest allocation due to lowest risk
- **Target Range**: 30-50%

## Liquidity

### Withdrawal Speed

- **Small Withdrawals** (&lt;1% of pool): Instant
- **Large Withdrawals** (&gt;5% of pool): May need to wait for repayments
- **Aave Reserve**: Typically 10-20% idle for instant liquidity

**Veilfi Impact**: With 40% allocation, withdrawals are almost always instant.

---

**Next**: [Lido Strategy](./lido-strategy) - ETH staking integration.
