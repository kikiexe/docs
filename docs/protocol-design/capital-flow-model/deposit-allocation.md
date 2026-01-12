---
title: Deposit & Allocation
sidebar_position: 1
---

# Deposit & Allocation

The deposit and allocation flow manages user capital from entry to deployment across yield strategies.

## Deposit Flow

### Step 1: User Initiates Deposit

```javascript
// Standard public deposit
await vaultContract.deposit({ value: ethers.utils.parseEther("10") });

// OR private deposit with ZK proof
const proof = await generateDepositProof(amount);
await vaultContract.depositWithProof(
  proof.a,
  proof.b,
  proof.c,
  proof.publicSignals,
  { value: amount }
);
```

### Step 2: Vault Receives Funds

```solidity
function deposit() external payable returns (uint256 shares) {
    require(msg.value > 0, "Zero deposit");

    // Calculate shares based on current price
    shares = _convertToShares(msg.value);

    // Mint shares to user
    _mint(msg.sender, shares);

    emit Deposit(msg.sender, msg.value, shares);
}
```

### Step 3: Share Calculation

```solidity
function _convertToShares(uint256 assets) internal view returns (uint256) {
    uint256 supply = totalSupply();

    if (supply == 0) {
        // First deposit: 1:1 ratio
        return assets;
    }

    // Subsequent deposits: proportional to share price
    return (assets * supply) / totalAssets();
}
```

**Example**:

```
Vault TVL: 1000 ETH
Total Shares: 900
Share Price: 1000/900 = 1.111 ETH

User deposits 10 ETH:
Shares minted = 10 / 1.111 = 9 shares
```

## Allocation Flow

### Step 1: Admin Triggers Allocation

```solidity
function allocateToStrategies() external onlyOwner {
    uint256 availableBalance = address(this).balance;
    require(availableBalance > 0, "Nothing to allocate");

    _allocateToStrategies(availableBalance);
}
```

### Step 2: Distribution to Strategies

```solidity
function _allocateToStrategies(uint256 totalAmount) internal {
    // Current allocations: [40, 30, 30] = percentages

    for (uint i = 0; i < strategies.length; i++) {
        uint256 amountForStrategy = totalAmount * allocations[i] / 100;

        if (amountForStrategy > 0) {
            strategies[i].deposit{value: amountForStrategy}();
        }
    }

    emit FundsAllocated(totalAmount);
}
```

**Example**:

```
Available: 100 ETH
Allocations: [40, 30, 30]

Aave receives: 100 × 40% = 40 ETH
Lido receives: 100 × 30% = 30 ETH
Uniswap receives: 100 × 30% = 30 ETH
```

### Step 3: Strategy Deployment

Each strategy deploys capital to its protocol:

```solidity
// Aave Strategy
function deposit() external payable override {
    aavePool.supply(WETH, msg.value, address(this), 0);
}

// Lido Strategy
function deposit() external payable override {
    lido.submit{value: msg.value}(address(0));
}

// Uniswap Strategy
function deposit() external payable override {
    positionManager.mint(...);
}
```

## Allocation Timing

### Batch Allocation

Deposits accumulate, then allocated in batches:

```
Day 1:  User A deposits 10 ETH → Held in vault
Day 2: User B deposits 20 ETH → Held in vault
Day 3: User C deposits 15 ETH → Held in vault
Day 7: Admin allocates 45 ETH → Deployed to strategies

Reason: Save gas, optimize capital deployment
```

### Minimum Allocation Threshold

```solidity
uint256 public constant MIN_ALLOCATION = 1 ether;

function allocateToStrategies() external onlyOwner {
    require(address(this).balance >= MIN_ALLOCATION);
    // ... allocate
}
```

**Rationale**: Avoid expensive gas for tiny amounts.

## Capital Efficiency

### Instant Availability

Small withdrawals served from vault balance:

```
Vault balance: 50 ETH (unallocated)
User withdraws: 5 ETH → Instant (no strategy liquidation)
```

### Reserve Buffer

Maintain 5-10% unallocated for withdrawals:

```solidity
function _allocateToStrategies(uint256 totalAmount) internal {
    // Keep 10% reserve
    uint256 reserve = totalAmount * 10 / 100;
    uint256 toAllocate = totalAmount - reserve;

    // Allocate remaining 90%
    for (uint i = 0; i < strategies.length; i++) {
        uint256 amount = toAllocate * allocations[i] / 100;
        strategies[i].deposit{value: amount}();
    }
}
```

---

**Next**: [Yield Harvest Cycle](./yield-harvest-cycle)
