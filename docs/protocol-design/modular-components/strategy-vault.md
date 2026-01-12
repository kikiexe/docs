---
title: Strategy Vault
sidebar_position: 1
---

# Strategy Vault

The **StrategyVaultV2_Multi** contract is the central coordinator managing deposits, shares, allocations, and user interactions.

## Contract Overview

```solidity
contract StrategyVaultV2_Multi is ERC4626, ReentrancyGuard,Ownable {
    // State
    IStrategy[] public strategies;
    uint256[] public allocations;
    IGroth16Verifier public zkVerifier;
    IComplianceManager public compliance;

    // Core functions
    function deposit() external payable returns (uint256 shares);
    function depositWithProof(...) external payable returns (uint256 shares);
    function withdraw(uint256 shares) external returns (uint256 assets);
    function allocateToStrategies() external onlyOwner;
    function harvestYields() external onlyOwner;
}
```

## Key Features

### ERC-4626 Compliance

Standard tokenized vault interface:

- `deposit()` / `withdraw()` - Standard deposit/withdrawal
- `totalAssets()` - Total vault TVL
- `convertToShares()` / `convertToAssets()` - Price calculations

### Multi-Strategy Support

Manages multiple yield sources:

```solidity
function allocateToStrategies() external onlyOwner {
    uint256 available = address(this).balance;

    for (uint i = 0; i < strategies.length; i++) {
        uint amount = available * allocations[i] / 100;
        strategies[i].deposit{value: amount}();
    }
}
```

### ZK Privacy Integration

```solidity
function depositWithProof(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[3] memory publicSignals
) external payable returns (uint256) {
    require(zkVerifier.verifyProof(a, b, c, publicSignals));
    return _processDeposit(msg.sender, msg.value);
}
```

---

**Next**: [Compliance Manager](./compliance-manager)
