---
title: Lido Strategy
sidebar_position: 2
---

# Lido Strategy

Lido Finance enables liquid ETH staking, allowing Veilfi to earn Ethereum network validation rewards while maintaining liquidity through stETH tokens.

## Protocol Overview

**Lido**: Liquid staking protocol for Ethereum 2.0.

- **TVL**: $30B+ (largest DeFi protocol)
- **Years Live**: 3+ (launched 2020)
- **Audits**: 15+ including Sigma Prime, Quantstamp, MixBytes
- **Validators**: 30+ node operators

## How It Works

### Liquid Staking Mechanism

```
1. Veilfi deposits ETH to Lido
   ↓
2. Lido stakes ETH with validators
   ↓
3. Veilfi receives stETH (1:1 initially)
   ↓
4. stETH balance increases daily (rebasing)
   ↓
5. Veilfi swaps stETH → ETH when harvesting
```

### Rebasing Model

```solidity
// stETH is a rebasing token
Day 0:  Deposit 100 ETH → Receive 100 stETH
Day 1:  Balance: 100.0123 stETH (+0.0123 ETH rewards)
Day 30: Balance: 100.37 stETH (+0.37 ETH rewards)
Day 365: Balance: 104.5 stETH (+4.5 ETH rewards = 4.5% APR)
```

## Smart Contract Integration

### Mock Lido Strategy

```solidity
contract MockLidoStrategy is IStrategy {
    ILido public lido;
    IERC20 public stETH;
    IUniswapRouter public router;

    uint256 public totalDeposited;

    function deposit() external payable override onlyVault returns (uint256) {
        require(msg.value > 0, "Zero deposit");

        // Submit to Lido, receive stETH
        uint256 stETHReceived = lido.submit{value: msg.value}(address(0));

        totalDeposited += msg.value;

        emit Deposited(msg.value);
        return stETHReceived;
    }

    function withdraw(uint256 amount) external override onlyVault returns (uint256) {
        // Swap stETH → ETH via DEX (Lido withdrawal queue takes 1-7 days)
        uint256 stETHToSwap = (amount * 1e18) / _getStETHPrice();

        address[] memory path = new address[](2);
        path[0] = address(stETH);
        path[1] = address(WETH);

        uint256[] memory amounts = router.swapExactTokensForTokens(
            stETHToSwap,
            amount * 99 / 100,  // 1% slippage tolerance
            path,
            address(vault),
            block.timestamp
        );

        totalDeposited -= amount;
        return amounts[1];
    }

    function harvest() external override onlyVault returns (uint256) {
        // Calculate stETH growth (rebasing)
        uint256 currentStETH = stETH.balanceOf(address(this));
        uint256 expectedStETH = totalDeposited;  // 1:1 initial

        uint256 yieldInStETH = currentStETH - expectedStETH;

        if (yieldInStETH > 0) {
            // Swap stETH yield → ETH
            uint256 ethReceived = _swapStETHToETH(yieldInStETH);
            return ethReceived;
        }

        return 0;
    }

    function totalAssets() external view override returns (uint256) {
        uint256 stETHBalance = stETH.balanceOf(address(this));
        return stETHBalance * _getStETHPrice() / 1e18;
    }

    function apy() external view override returns (uint256) {
        // stETH APR typically 4-5%
        return 450;  // 4.5% in basis points
    }

    function _getStETHPrice() internal view returns (uint256) {
        // stETH usually trades 0.98-1.0 ETH
        // For simplicity, assume 1:1
        return 1e18;
    }
}
```

## Yield Characteristics

### APY Composition

| Source                      | APY Contribution |
| --------------------------- | ---------------- |
| **Consensus Layer Rewards** | ~4.0%            |
| **MEV Rewards**             | ~0.3-0.5%        |
| **Priority Fees**           | ~0.1-0.2%        |
| **Total Gross**             | ~4.5%            |
| **Lido Fee** (10%)          | -0.45%           |
| **Net to Users**            | **~4.05%**       |

### Historical APY

```
2023 Average: 4.2%
2024 Q1: 4.5%
2024 Q2: 4.3%

Post-Shanghai Upgrade: More stable around 4-4.5%
```

## Risk Profile

### Security

✅ **Audited**: 15+ audits  
✅ **Distributed Validators**: 30+ operators (no single point of failure)  
✅ **Insurance**: $100M+ self-insurance fund  
✅ **Slashing Protection**: Distributed validator set minimizes risk

### Risks

⚠️ **Validator Slashing**: Validators penalized for misbehavior (rare)  
⚠️ **stETH Depeg Risk**: stETH may trade &lt;1 ETH during stress (temporary)  
⚠️ **Smart Contract Risk**: Bug in Lido contracts (low probability)  
⚠️ **Ethereum Risk**: Network-level issues (extremely low)

**Overall Risk**: 🟢 Very Low (2/10)

### stETH Depeg History

| Event                             | stETH/ETH Ratio | Duration | Recovery |
| --------------------------------- | --------------- | -------- | -------- |
| **Normal**                        | 0.998-1.0       | Ongoing  | N/A      |
| **May 2022 (UST crash)**          | 0.93            | 2 weeks  | Full     |
| **Jun 2023 (withdrawal enabled)** | 0.95            | 1 week   | Full     |

**Veilfi Mitigation**: Can swap stETH → ETH via DEX for instant liquidity.

## Liquidity Options

### Option 1: Lido Withdrawal Queue

```
Timeline: 1-7 days
Fee: None
Slippage: None
Best for: Patient withdrawals
```

### Option 2: DEX Swap (Curve, Uniswap)

```
Timeline: Instant
Fee: ~0.3% swap fee
Slippage: 0.1-0.5%
Best for: Urgent withdrawals (Veilfi uses this)
```

## Performance Metrics

### Veilfi Allocation

- **Current Allocation**: 30% of total vault
- **Rationale**: Balance of yield and safety
- **Target Range**: 20-40%

### Compounding Effect

```
Month 0:  100 ETH staked
Month 1:  100.37 ETH (+0.37%)
Month 6:  102.25 ETH (+2.25%)
Month 12: 104.50 ETH (+4.50%)
```

**Auto-compounding**: Staking rewards automatically compound (rebasing).

---

**Next**: [Uniswap Strategy](./uniswap-strategy) - Liquidity provision.
