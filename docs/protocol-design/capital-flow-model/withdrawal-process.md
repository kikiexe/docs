---
title: Withdrawal Process
sidebar_position: 3
---

# Withdrawal Process

The withdrawal process allows users to redeem their vault shares for underlying assets (ETH/USDC) while maintaining share price fairness for remaining depositors.

## Withdrawal Flow

### Step 1: User Requests Withdrawal

```javascript
// User initiates withdrawal
const sharesToBurn = ethers.utils.parseEther("10");
await vaultContract.withdraw(sharesToBurn);
```

### Step 2: Vault Calculates Value

```solidity
function withdraw(uint256 shares) external nonReentrant returns (uint256 assets) {
    require(shares > 0, "Zero shares");
    require(balanceOf(msg.sender) >= shares, "Insufficient shares");

    // Calculate ETH value of shares
    assets = _convertToAssets(shares);

    // Burn user's shares
    _burn(msg.sender, shares);

    // Determine funding source
    if (address(this).balance >= assets) {
        // Sufficient vault balance
        _withdrawFromVault(msg.sender, assets);
    } else {
        // Need to liquidate from strategies
        _withdrawFromStrategies(msg.sender, assets);
    }

    emit Withdraw(msg.sender, assets, shares);
}
```

### Step 3: Asset Conversion

```solidity
function _convertToAssets(uint256 shares) internal view returns (uint256) {
    uint256 supply = totalSupply();

    if (supply == 0) return 0;

    // assets = shares × (totalAssets / totalSupply)
    return (shares * totalAssets()) / supply;
}
```

**Example**:

```
Vault TVL: 1005 ETH
Total Shares: 900
Share Price: 1005/900 = 1.1167 ETH

User redeems 10 shares:
ETH received = 10 × 1.1167 = 11.167 ETH
```

## Liquidity Management

### Vault Reserve

Maintain unallocated ETH for instant withdrawals:

```solidity
uint256 public constant RESERVE_RATIO = 10; // 10%

function _maintainReserve(uint256 totalAmount) internal {
    uint256 reserve = totalAmount * RESERVE_RATIO / 100;
    uint256 toAllocate = totalAmount - reserve;

    // Keep 10% in vault, allocate 90%
    allocateToStrategies(toAllocate);
}
```

### Fast Withdrawals

Small withdrawals served instantly:

```
Vault balance: 50 ETH (unallocated)
User withdraws: 5 ETH → Instant ✅
User withdraws: 30 ETH → Instant ✅
User withdraws: 60 ETH → Need strategy liquidation ⏳
```

### Strategy Liquidation

For large withdrawals, liquidate from strategies:

```solidity
function _withdrawFromStrategies(address user, uint256 amount) internal {
    uint256 remaining = amount - address(this).balance;

    // Withdraw from strategies in order of liquidity
    for (uint i = 0; i < strategies.length; i++) {
        if (remaining == 0) break;

        uint256 strategyBalance = strategies[i].totalAssets();
        uint256 toWithdraw = min(remaining, strategyBalance);

        strategies[i].withdraw(toWithdraw);
        remaining -= toWithdraw;
    }

    // Transfer to user
    payable(user).transfer(amount);
}
```

## Withdrawal Fees

### Anti-Manipulation Fee (0.1%)

Prevents flash-loan attacks:

```solidity
uint256 public constant WITHDRAWAL_FEE = 10; // 0.1% in basis points

function _deductWithdrawalFee(uint256 amount) internal returns (uint256) {
    uint256 fee = amount * WITHDRAWAL_FEE / 10000;
    protocolFees += fee;
    return amount - fee;
}
```

**Example**:

```
Withdrawal: 100 ETH
Fee: 100 × 0.001 = 0.1 ETH
User receives: 99.9 ETH
```

### No Lock-Up Period

Users can withdraw anytime:

```
❌ Other protocols: 7-30 day lock-up
✅ Veilfi: Withdraw anytime (subject to liquidity)
```

## Edge Cases

### Insufficient Liquidity

If strategies cannot provide immediate liquidity:

```solidity
function withdraw(uint256 shares) external returns (uint256) {
    uint256 assets = _convertToAssets(shares);
    uint256 available = _getAvailableLiquidity();

    if (available < assets) {
        // Partial withdrawal + IOU for remainder
        _burn(msg.sender, shares);
        payable(msg.sender).transfer(available);

        // Queue remaining for next harvest
        withdrawalQueue[msg.sender] += (assets - available);

        emit PartialWithdrawal(msg.sender, available, assets - available);
    } else {
        // Full withdrawal
        _processFullWithdrawal(msg.sender, shares, assets);
    }
}
```

### Strategy Exploit

If strategy is compromised:

```solidity
function emergencyWithdraw(uint256 strategyIndex) external onlyOwner {
    // Pull all assets from strategy immediately
    strategies[strategyIndex].emergencyWithdraw();

    // Pause strategy
    strategyActive[strategyIndex] = false;

    // Users can still withdraw from remaining strategies
}
```

## Privacy Considerations

### Public Withdrawals

Standard withdrawals are transparent:

```
Event: Withdraw(user: 0xAlice..., amount: 10 ETH, shares: 9)
↑ Public on blockchain
```

### Private Withdrawals (Future)

Using ZK proofs to hide withdrawal amounts:

```solidity
function withdrawWithProof(
    uint256 shares,
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[3] memory publicSignals
) external {
    // Verify ZK proof of share ownership
    require(zkVerifier.verifyProof(a, b, c, publicSignals));

    // Process withdrawal without revealing amount
    _processPrivateWithdrawal(msg.sender, shares);
}
```

## Withdrawal Limits

### Per-User Limits

No individual withdrawal limits:

```
User can withdraw 100% of their shares in one transaction
(subject to vault liquidity)
```

### Protocol-Level Limits

Daily withdrawal cap for security:

```solidity
uint256 public dailyWithdrawalLimit = 1000 ether;
uint256 public totalWithdrawnToday;
uint256 public lastWithdrawalResetTime;

modifier withinDailyLimit(uint256 amount) {
    if (block.timestamp > lastWithdrawalResetTime + 1 days) {
        totalWithdrawnToday = 0;
        lastWithdrawalResetTime = block.timestamp;
    }

    require(
        totalWithdrawnToday + amount <= dailyWithdrawalLimit,
        "Daily limit exceeded"
    );

    totalWithdrawnToday += amount;
    _;
}
```

**Rationale**: Prevent bank-run scenarios during exploits.

## Gas Optimization

### Minimize Strategy Withdrawals

```solidity
// Check vault balance first (cheap)
if (address(this).balance >= assets) {
    payable(user).transfer(assets);  // ~21k gas
} else {
    // Only liquidate from strategies if needed
    _withdrawFromStrategies(user, assets);  // ~150k gas
}
```

### Batch Withdrawals

Process multiple queued withdrawals together:

```solidity
function processWithdrawalQueue(address[] memory users) external onlyOwner {
    for (uint i = 0; i < users.length; i++) {
        uint256 pending = withdrawalQueue[users[i]];
        if (pending > 0 && address(this).balance >= pending) {
            withdrawalQueue[users[i]] = 0;
            payable(users[i]).transfer(pending);
        }
    }
}
```

---

**Congratulations!** You've completed the **Protocol Design** section.

**Next Steps**:

- [DeFi Strategies](../../defi-strategies/overview) - Explore yield strategies in detail
- [Core Flow](../../core-flow/user-flow/wallet-connection) - Learn user interaction flows
