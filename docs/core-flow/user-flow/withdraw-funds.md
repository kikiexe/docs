---
title: Withdraw Funds
sidebar_position: 5
---

# Withdraw Funds

Withdraw your funds from the vault at any time. Withdrawals are processed by burning your vault shares in exchange for ETH.

## Withdrawal Process

```
1. Enter amount to withdraw
   ↓
2. Calculate shares to burn
   ↓
3. Check vault liquidity
   ↓
4. Sign transaction
   ↓
5. Burn shares
   ↓
6. Receive ETH
```

## Implementation

### Withdrawal Component

```tsx
function WithdrawComponent() {
  const [amount, setAmount] = useState("");
  const { address } = useAccount();

  const { data: userShares } = useContractRead({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "balanceOf",
    args: [address],
  });

  const { data: sharePrice } = useContractRead({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "pricePerShare",
  });

  const maxWithdrawable =
    userShares && sharePrice
      ? formatEther((userShares * sharePrice) / 1e18)
      : "0";

  const sharesToBurn =
    amount && sharePrice ? (parseEther(amount) * 1e18) / sharePrice : 0;

  const { write: withdraw } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "withdraw",
    args: [sharesToBurn],
  });

  return (
    <Card>
      <h2>Withdraw from Vault</h2>

      <Input
        label="Amount to Withdraw (ETH)"
        value={amount}
        onChange={setAmount}
        max={maxWithdrawable}
      />

      <InfoBox>
        <p>Your Max: {maxWithdrawable} ETH</p>
        <p>Shares to Burn: {formatUnits(sharesToBurn, 18)}</p>
        <p>
          Withdrawal Fee: 0.1% ({(parseFloat(amount) * 0.001).toFixed(4)} ETH)
        </p>
      </InfoBox>

      <Button
        onClick={() => withdraw()}
        disabled={!amount || parseFloat(amount) > parseFloat(maxWithdrawable)}
      >
        Withdraw {amount} ETH
      </Button>
    </Card>
  );
}
```

## Liquidity Options

### Instant Withdrawal

If vault has sufficient balance:

```
Available in vault: 50 ETH
User withdraws: 5 ETH
→ Instant (no strategy liquidation needed)
```

### Partial Strategy Withdrawal

If vault needs to liquidate:

```
Available in vault: 5 ETH
User withdraws: 10 ETH
→ Withdraw 5 ETH from Aave strategy
→ Total: 5 ETH (vault) + 5 ETH (Aave) = 10 ETH
→ Time: ~30 seconds
```

## Withdrawal Fees

```javascript
// 0.1% withdrawal fee
const fee = withdrawAmount * 0.001;
const netReceived = withdrawAmount - fee;

// Example: Withdraw 100 ETH
// Fee: 0.1 ETH
// You receive: 99.9 ETH
```

**Why fee?**: Prevents flash-loan attacks and wash trading.

## Transaction Confirmation

```tsx
function WithdrawalConfirmation({ txHash, amount }) {
  return (
    <SuccessModal>
      <h2>✅ Withdrawal Successful!</h2>
      <p>Amount: {amount} ETH</p>
      <p>Transaction: {txHash}</p>

      <Button href={` https://explorer.sepolia.mantle.xyz/tx/${txHash}`}>
        View on Explorer
      </Button>
    </SuccessModal>
  );
}
```

## Edge Cases

### Insufficient Liquidity

```tsx
if (requestedAmount > availableLiquidity) {
  return (
    <Alert severity="warning">
      Requested ${requestedAmount} ETH, but only ${availableLiquidity} ETH
      available. Large withdrawals may take 1-2 hours for strategy liquidation.
      Proceed anyway?
    </Alert>
  );
}
```

### Daily Limit

```solidity
// Protect against bank runs
uint256 public dailyWithdrawalLimit = 1000 ether;

require(
  totalWithdrawnToday + amount <= dailyWithdrawalLimit,
  "Daily limit exceeded"
);
```

---

**Up Next**: Check out [Admin Flow](../admin-flow/manage-strategies) or [Privacy Flow](../privacy-flow/private-deposits).
