---
title: Core Vault Layer
sidebar_position: 1
---

# Core Vault Layer

The **Core Vault Layer** is Veilfi's central smart contract that coordinates all deposits, withdrawals, share management, and interactions with underlying yield strategies.

## Architecture Overview

```
┌─────────────────────────────────────────┐
│        StrategyVaultV2_Multi            │
│  (Core Vault - ERC-4626 Compliant)      │
├─────────────────────────────────────────┤
│                                         │
│  State Management:                      │
│  ├─ Total Assets (TVL)                  │
│  ├─ User Shares (ERC-20)                │
│  ├─ Strategy Allocations                │
│  └─ ZK Proof Verifications              │
│                                         │
│  Core Functions:                        │
│  ├─ deposit() / depositWithProof()      │
│  ├─ withdraw()                          │
│  ├─ allocateToStrategies()              │
│  └─ harvestYields()                     │
│                                         │
└─────────────────────────────────────────┘
           ↓         ↓         ↓
    ┌──────┴───┐ ┌──┴────┐ ┌──┴──────┐
    │  Aave    │ │ Lido  │ │ Uniswap │
    │ Strategy │ │Strategy│ │ Strategy│
    └──────────┘ └───────┘ └─────────┘
```

## Key Responsibilities

### 1. Asset Custody

Vault holds all deposited ETH/USDC:

```solidity
contract StrategyVaultV2_Multi {
    uint256 public totalAssets;  // Total ETH in vault + strategies

    function totalAssets() public view returns (uint256) {
        uint256 vaultBalance = address(this).balance;

        // Add assets deployed in strategies
        for (uint i = 0; i < strategies.length; i++) {
            vaultBalance += strategies[i].totalAssets();
        }

        return vaultBalance;
    }
}
```

**Non-Custodial Design**: Vault is a smart contract, not controlled by team.

### 2. Share Management (ERC-4626)

Implements tokenized vault standard:

```solidity
contract StrategyVaultV2_Multi is ERC4626 {
    // Mint shares on deposit
    function deposit(uint256 assets, address receiver)
        public virtual override returns (uint256 shares)
    {
        shares = _convertToShares(assets, Math.Rounding.Down);
        _deposit(msg.sender, receiver, assets, shares);
        return shares;
    }

    // Burn shares on withdrawal
    function withdraw(uint256 assets, address receiver, address owner)
        public virtual override returns (uint256 shares)
    {
        shares = _convertToShares(assets, Math.Rounding.Up);
        _withdraw(msg.sender, receiver, owner, assets, shares);
        return shares;
    }
}
```

**Share Price Calculation**:

```
sharePrice = totalAssets() / totalSupply()
```

### 3. ZK Proof Verification

Validates privacy-preserving deposits:

```solidity
IGroth16Verifier public zkVerifier;

function depositWithProof(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[3] memory publicSignals
) external payable returns (uint256 shares) {
    // Verify zero-knowledge proof
    require(
        zkVerifier.verifyProof(a, b, c, publicSignals),
        "Invalid ZK proof"
    );

    // Process deposit privately
    shares = _deposit(msg.sender, msg.sender, msg.value, 0);

    emit PrivateDeposit(msg.sender, keccak256(abi.encode(a, b, c)));
    return shares;
}
```

**Privacy Guarantee**: Deposit amount hidden in ZK proof.

### 4. Strategy Coordination

Allocates capital to yield strategies:

```solidity
IStrategy[] public strategies;
uint256[] public allocations; // [40, 30, 30] = percentages

function allocateToStrategies() external onlyOwner {
    uint256 availableAssets = address(this).balance;

    for (uint i = 0; i < strategies.length; i++) {
        uint256 amountToAllocate = availableAssets * allocations[i] / 100;
        strategies[i].deposit{value: amountToAllocate}();
    }

    emit FundsAllocated(availableAssets);
}
```

### 5. Yield Collection

Harvests yields from all strategies:

```solidity
function harvestYields() external onlyOwner {
    uint256 totalYield = 0;

    for (uint i = 0; i < strategies.length; i++) {
        uint256 strategyYield = strategies[i].harvest();
        totalYield += strategyYield;
    }

    // Yields automatically added to totalAssets
    // Share price increases proportionally
    emit YieldHarvested(totalYield);
}
```

## State Variables

### Core State

```solidity
contract StrategyVaultV2_Multi {
    // ERC-4626 compliance
    IERC20 public asset;           // Underlying asset (WETH)

    // Strategy management
    IStrategy[] public strategies;
    uint256[] public allocations;

    // ZK verification
    IGroth16Verifier public zkVerifier;
    IComplianceManager public complianceManager;

    // Access control
    address public owner;
    bool public paused;

    // Accounting
    uint256 public totalDeposits;
    uint256 public totalWithdrawals;
    uint256 public totalYieldEarned;
}
```

### Mappings

```solidity
// Track user shares (inherited from ERC20)
mapping(address => uint256) private _shares;

// Track KYC status (via ComplianceManager)
mapping(address => bool) public isKYCVerified;

// Track used proof commitments (prevent replay)
mapping(bytes32 => bool) public usedProofs;
```

## Security Features

### 1. Access Control

```solidity
modifier onlyOwner() {
    require(msg.sender == owner, "Not owner");
    _;
}

modifier whenNotPaused() {
    require(!paused, "Contract paused");
    _;
}
```

### 2. Reentrancy Protection

```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract StrategyVaultV2_Multi is ReentrancyGuard {
    function withdraw(uint256 shares) external nonReentrant {
        // Safe from reentrancy attacks
    }
}
```

### 3. Strategy Limits

```solidity
uint256 public constant MAX_STRATEGIES = 10;
uint256 public constant MAX_ALLOCATION_PER_STRATEGY = 50; // 50%

function addStrategy(IStrategy newStrategy) external onlyOwner {
    require(strategies.length < MAX_STRATEGIES, "Too many strategies");
    strategies.push(newStrategy);
}
```

### 4. Emergency Pause

```solidity
function pause() external onlyOwner {
    paused = true;
    emit Paused(msg.sender);
}

function unpause() external onlyOwner {
    paused = false;
    emit Unpaused(msg.sender);
}
```

## Events

```solidity
event Deposit(address indexed user, uint256 assets, uint256 shares);
event PrivateDeposit(address indexed user, bytes32 proofHash);
event Withdraw(address indexed user, uint256 assets, uint256 shares);
event FundsAllocated(uint256 totalAmount);
event YieldHarvested(uint256 totalYield);
event StrategyAdded(address indexed strategy);
event StrategyRemoved(address indexed strategy);
event Paused(address account);
event Unpaused(address account);
```

## Integration Points

### Upstream (Users)

```javascript
// User deposits via web3
const vaultContract = new ethers.Contract(VAULT_ADDRESS, VAULT_ABI, signer);

// Standard deposit
await vaultContract.deposit({ value: ethers.utils.parseEther("10") });

// Private deposit with ZK proof
const proof = await generateDepositProof(amount);
await vaultContract.depositWithProof(
  proof.a,
  proof.b,
  proof.c,
  proof.publicSignals,
  { value: amount }
);
```

### Downstream (Strategies)

```solidity
// Vault calls strategy contracts
interface IStrategy {
    function deposit() external payable;
    function withdraw(uint256 amount) external returns (uint256);
    function harvest() external returns (uint256 yield);
    function totalAssets() external view returns (uint256);
}
```

## Gas Optimization

### Batch Operations

```solidity
// Single transaction for harvest + reallocate
function harvestAndReallocate() external onlyOwner {
    // 1. Harvest all yields
    for (uint i = 0; i < strategies.length; i++) {
        strategies[i].harvest();
    }

    // 2. Reallocate with new yields
    allocateToStrategies();

    // Saves ~30% gas vs separate calls
}
```

### View Function Caching

```solidity
// Cache total assets to avoid multiple external calls
uint256 private cachedTotalAssets;
uint256 private lastUpdateBlock;

function totalAssets() public view returns (uint256) {
    if (block.number == lastUpdateBlock) {
        return cachedTotalAssets;
    }
    return _calculateTotalAssets();
}
```

## Upgrade Path

### Current: Non-Upgradeable

Vault is immutable for security:

```solidity
// No proxy pattern - direct deployment
// Users trust code, not admin
```

### Future: Strategy Migration

If new vault needed:

```solidity
function migrateToNewVault(address newVault) external onlyOwner {
    // 1. Pause deposits
    paused = true;

    // 2. Withdraw from all strategies
    for (uint i = 0; i < strategies.length; i++) {
        strategies[i].withdrawAll();
    }

    // 3. Transfer assets to new vault
    payable(newVault).transfer(address(this).balance);

    // Users redeem shares in old vault, deposit to new vault
}
```

**Principle**: Immutable core, upgradeable strategies.

---

**Next**: [Strategy Layer](./strategy-layer) - How yield strategies integrate with the vault.

**Related**: [StrategyVaultV2 Contract](../../smart-contracts/core-contracts/strategy-vault-v2) for full implementation.
