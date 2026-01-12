---
title: MockUniswapStrategy
sidebar_position: 3
---

# MockUniswapStrategy

Uniswap V3 liquidity provision strategy.

## Contract

```solidity
contract MockUniswapStrategy is IStrategy {
    INonfungiblePositionManager public positionManager;
    uint256 public tokenId;

    function deposit() external payable override returns (uint256) {
        (tokenId, , , ) = positionManager.mint(
            INonfungiblePositionManager.MintParams({
                token0: WETH,
                token1: USDC,
                fee: 3000,  // 0.3%
                amount0Desired: msg.value,
                // ... other params
            })
        );
        return msg.value;
    }

    function harvest() external override returns (uint256) {
        (uint256 amount0, uint256 amount1) = positionManager.collect(...);
        return amount0 + _convertUSDCToETH(amount1);
    }
}
```

**APY**: 10-30%  
**Risk**: Medium (5/10)

---

**Next**: [Deployment](../deployment/mantle-sepolia)
