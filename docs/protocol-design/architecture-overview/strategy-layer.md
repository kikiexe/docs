---
title: Strategy Layer
sidebar_position: 2
---

# Strategy Layer

The **Strategy Layer** consists of modular smart contracts that integrate with external DeFi protocols to generate yield. Each strategy implements a standard interface, making them plug-and-play with the core vault.

## Strategy Architecture

```
┌────────────────────────────────────────┐
│      IStrategy Interface               │
│  (Standardized contract interface)     │
└────────────────────────────────────────┘
            ↓ Implemented by
┌─────────────┬──────────────┬───────────────┐
│ AaveStrategy│ LidoStrategy │ UniswapStrategy│
└─────────────┴──────────────┴───────────────┘
      ↓              ↓               ↓
┌─────────────┬──────────────┬───────────────┐
│  Aave V3    │ Lido Finance │  Uniswap V3   │
│  Protocol   │   Protocol   │    Protocol   │
└─────────────┴──────────────┴───────────────┘
```

## Standard Interface

All strategies implement `IStrategy`:

```solidity
interface IStrategy {
    // Deploy assets to protocol
    function deposit() external payable returns (uint256 shares);

    // Withdraw assets from protocol
    function withdraw(uint256 amount) external returns (uint256);

    // Claim yields/rewards
    function harvest() external returns (uint256 yield);

    // Check total assets in strategy
    function totalAssets() external view returns (uint256);

    // Get current APY
    function apy() external view returns (uint256);

    // Emergency withdrawal
    function emergencyWithdraw() external returns (uint256);
}
```

## Strategy Implementations

### Aave Strategy

Deposits to Aave lending pool:

```solidity
contract MockAaveStrategy is IStrategy {
    IAavePool public aavePool;
    IERC20 public aToken;  // Interest-bearing token

    function deposit() external payable override returns (uint256) {
        // Deposit ETH to Aave
        aavePool.supply(WETH, msg.value, address(this), 0);

        // Receive aTokens (accrue interest)
        return msg.value;
    }

    function harvest() external override returns (uint256) {
        // Claim accrued interest
        uint256 currentBalance = aToken.balanceOf(address(this));
        uint256 yield = currentBalance - totalDeposited;

        // Withdraw yield only
        aavePool.withdraw(WETH, yield, address(vault));
        return yield;
    }
}
```

**APY**: 3-8% (lending interest)  
**Risk**: 🟢 Low (battle-tested, $10B+ TVL)

### Lido Strategy

Stakes ETH with Lido:

```solidity
contract MockLidoStrategy is IStrategy {
    ILido public lido;
    IERC20 public stETH;  // Liquid staking token

    function deposit() external payable override returns (uint256) {
        // Stake ETH, receive stETH
        uint256 stETHAmount = lido.submit{value: msg.value}(address(0));
        return stETHAmount;
    }

    function harvest() external override returns (uint256) {
        // stETH appreciates in value (rebasing)
        // Yield = stETH balance growth
        uint256 yield = stETH.balanceOf(address(this)) - totalDeposited;

        // Swap stETH → ETH and return to vault
        return _swapToETH(yield);
    }
}
```

**APY**: 4-5% (ETH staking rewards)  
**Risk**: 🟢 Low (Ethereum network security)

### Uniswap Strategy

Provides liquidity to Uniswap V3:

```solidity
contract MockUniswapStrategy is IStrategy {
    INonfungiblePositionManager public positionManager;
    uint256 public tokenId;  // LP position NFT

    function deposit() external payable override returns (uint256) {
        // Provide liquidity to ETH/USDC pool
        (tokenId, , , ) = positionManager.mint(
            INonfungiblePositionManager.MintParams({
                token0: WETH,
                token1: USDC,
                fee: 3000,  // 0.3% fee tier
                tickLower: -887220,
                tickUpper: 887220,
                amount0Desired: msg.value,
                amount1Desired: 0,
                amount0Min: 0,
                amount1Min: 0,
                recipient: address(this),
                deadline: block.timestamp
            })
        );

        return msg.value;
    }

    function harvest() external override returns (uint256) {
        // Collect trading fees
        (uint256 amount0, uint256 amount1) = positionManager.collect(
            INonfungiblePositionManager.CollectParams({
                tokenId: tokenId,
                recipient: address(vault),
                amount0Max: type(uint128).max,
                amount1Max: type(uint128).max
            })
        );

        return amount0 + _convertUSDCToETH(amount1);
    }
}
```

**APY**: 10-30% (trading fees, variable)  
**Risk**: 🟡 Medium (impermanent loss, volatile APY)

## Strategy Lifecycle

### 1. Addition

Owner adds new strategy to vault:

```solidity
// In StrategyVaultV2_Multi
function addStrategy(
    address strategyAddress,
    uint256 allocationPercentage
) external onlyOwner {
    require(strategies.length < MAX_STRATEGIES, "Max strategies reached");
    require(allocationPercentage <= 50, "Allocation too high");

    IStrategy newStrategy = IStrategy(strategyAddress);

    // Verify strategy implements interface
    require(newStrategy.totalAssets() >= 0, "Invalid strategy");

    strategies.push(newStrategy);
    allocations.push(allocationPercentage);

   emit StrategyAdded(strategyAddress, allocationPercentage);
}
```

### 2. Activation

Admin allocates capital to strategy:

```solidity
function allocateToStrategy(uint256 strategyIndex) internal {
    IStrategy strategy = strategies[strategyIndex];
    uint256 allocation = allocations[strategyIndex];

    uint256 amountToDeposit = totalAssets() * allocation / 100;

    // Deposit to strategy
    strategy.deposit{value: amountToDeposit}();
}
```

### 3. Monitoring

Track strategy performance:

```solidity
struct StrategyInfo {
    address strategyAddress;
    uint256 totalDeposited;
    uint256 currentValue;
    uint256 yieldEarned;
    uint256 apy;
    bool isActive;
}

function getStrategyInfo(uint256 index)
    external view returns (StrategyInfo memory)
{
    IStrategy strategy = strategies[index];

    return StrategyInfo({
        strategyAddress: address(strategy),
        totalDeposited: strategyDeposits[index],
        currentValue: strategy.totalAssets(),
        yieldEarned: strategyYields[index],
        apy: strategy.apy(),
        isActive: strategyActive[index]
    });
}
```

### 4. Rebalancing

Adjust allocations based on performance:

```solidity
function rebalanceStrategies(uint256[] memory newAllocations)
    external onlyOwner
{
    require(newAllocations.length == strategies.length, "Length mismatch");
    require(_sumAllocations(newAllocations) == 100, "Must total 100%");

    // Withdraw from all strategies
    for (uint i = 0; i < strategies.length; i++) {
        strategies[i].withdraw(strategies[i].totalAssets());
    }

    // Update allocations
    allocations = newAllocations;

    // Reallocate with new percentages
    allocateToStrategies();
}
```

### 5. Removal

Deactivate underperforming strategies:

```solidity
function removeStrategy(uint256 index) external onlyOwner {
    // Withdraw all assets from strategy
    strategies[index].emergencyWithdraw();

    // Remove from array (swap with last element)
    strategies[index] = strategies[strategies.length - 1];
    strategies.pop();

    allocations[index] = allocations[allocations.length - 1];
    allocations.pop();

    emit StrategyRemoved(index);
}
```

## Risk Management

### Allocation Limits

```solidity
uint256 public constant MAX_ALLOCATION = 50; // 50% max per strategy

function setAllocation(uint256 index, uint256 newAllocation)
    external onlyOwner
{
    require(newAllocation <= MAX_ALLOCATION, "Exceeds max allocation");
    allocations[index] = newAllocation;
}
```

**Rationale**: Limit blast radius if strategy exploited.

### Health Checks

```solidity
function isStrategyHealthy(uint256 index) public view returns (bool) {
    IStrategy strategy = strategies[index];

    // Check 1: Not paused
    if (strategy.isPaused()) return false;

    // Check 2: Assets > 95% of deposits (max 5% loss acceptable)
    uint256 currentAssets = strategy.totalAssets();
    uint256 deposited = strategyDeposits[index];
    if (currentAssets < deposited * 95 / 100) return false;

    // Check 3: APY > 0
    if (strategy.apy() == 0) return false;

    return true;
}
```

### Emergency Procedures

```solidity
function emergencyWithdrawStrategy(uint256 index) external onlyOwner {
    IStrategy strategy = strategies[index];

    // Pull all assets immediately
    uint256 withdrawn = strategy.emergencyWithdraw();

    // Mark strategy as inactive
    strategyActive[index] = false;

    emit EmergencyWithdrawal(index, withdrawn);
}
```

---

**Next**: [ZK Proof Layer](./zk-proof-layer) - Privacy infrastructure.

**Related**: [Supported Protocols](../../defi-strategies/supported-protocols/aave-strategy) for strategy details.
