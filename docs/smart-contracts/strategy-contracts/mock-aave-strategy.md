---
title: MockAaveStrategy
sidebar_position: 1
---

# MockAaveStrategy

Aave V3 lending strategy implementation.

## Contract

```solidity
contract MockAaveStrategy is IStrategy {
    IAavePool public aavePool;
    IERC20 public aToken;

    function deposit() external payable override returns (uint256) {
        aavePool.supply(WETH, msg.value, address(this), 0);
        return msg.value;
    }

    function withdraw(uint256 amount) external override returns (uint256) {
        return aavePool.withdraw(WETH, amount, msg.sender);
    }

    function harvest() external override returns (uint256) {
        uint256 yield = aToken.balanceOf(address(this)) - totalDeposited;
        aavePool.withdraw(WETH, yield, msg.sender);
        return yield;
    }
}
```

**APY**: 3-8%  
**Risk**: Low (2/10)

---

**Next**: [MockLidoStrategy](./mock-lido-strategy)
