---
title: StrategyVaultV2
sidebar_position: 1
---

# StrategyVaultV2_Multi

Main vault contract managing user deposits, shares, and strategy allocation.

## Contract Overview

```solidity
contract StrategyVaultV2_Multi is ERC4626, ReentrancyGuard, Ownable {
    IStrategy[] public strategies;
    uint256[] public allocations;  // [40, 30, 30]

    IGroth16Verifier public zkVerifier;
    IComplianceManager public compliance;
}
```

## Key Functions

### deposit()

```solidity
function deposit() external payable returns (uint256 shares) {
    shares = _convertToShares(msg.value);
    _mint(msg.sender, shares);

    emit Deposit(msg.sender, msg.value, shares);
}
```

### withdraw()

```solidity
function withdraw(uint256 shares) external returns (uint256 assets) {
    assets = _convertToAssets(shares);
    _burn(msg.sender, shares);

    payable(msg.sender).transfer(assets);
    emit Withdraw(msg.sender, assets, shares);
}
```

### allocateToStrategies()

```solidity
function allocateToStrategies() external onlyOwner {
    uint256 available = address(this).balance;

    for (uint i = 0; i < strategies.length; i++) {
        uint256 amount = available * allocations[i] / 100;
        strategies[i].deposit{value: amount}();
    }
}
```

---

**Next**: [ComplianceManagerV2](./compliance-manager-v2)
