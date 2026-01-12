---
title: MockLidoStrategy
sidebar_position: 2
---

# MockLidoStrategy

Lido liquid staking strategy.

## Contract

```solidity
contract MockLidoStrategy is IStrategy {
    ILido public lido;
    IERC20 public stETH;

    function deposit() external payable override returns (uint256) {
        return lido.submit{value: msg.value}(address(0));
    }

    function withdraw(uint256 amount) external override returns (uint256) {
        // Swap stETH → ETH via DEX
        return _swapStETHToETH(amount);
    }

    function harvest() external override returns (uint256) {
        uint256 yield = stETH.balanceOf(address(this)) - totalDeposited;
        return _swapStETHToETH(yield);
    }
}
```

**APY**: 4-5%  
**Risk**: Low (2/10)

---

**Next**: [MockUniswapStrategy](./mock-uniswap-strategy)
