---
title: Interact with Vault
sidebar_position: 3
---

# Interact with Vault

Learn how to deposit, withdraw, and manage vault interactions.

## Deposit ETH

### Basic Deposit

```typescript
import { parseEther } from "viem";

const hash = await walletClient.writeContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "deposit",
  value: parseEther("1.0"), // Deposit 1 ETH
});

await publicClient.waitForTransactionReceipt({ hash });
console.log("Deposit successful!");
```

### React Component

```tsx
function DepositButton() {
  const [amount, setAmount] = useState("");

  const { write: deposit, isLoading } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "deposit",
    value: amount ? parseEther(amount) : undefined,
    onSuccess: () => {
      alert("Deposit successful!");
      setAmount("");
    },
  });

  return (
    <div>
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder="Amount in ETH"
      />
      <button onClick={() => deposit()} disabled={!amount || isLoading}>
        {isLoading ? "Depositing..." : "Deposit"}
      </button>
    </div>
  );
}
```

## Withdraw ETH

### Calculate Withdrawal Amount

```typescript
// User wants to withdraw 1 ETH
const ethAmount = parseEther("1.0");

// Calculate shares to burn
const sharePrice = await publicClient.readContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "pricePerShare",
});

const sharesToBurn = (ethAmount * BigInt(1e18)) / sharePrice;
```

### Execute Withdrawal

```typescript
const hash = await walletClient.writeContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "withdraw",
  args: [sharesToBurn],
});

await publicClient.waitForTransactionReceipt({ hash });
```

### React Component

```tsx
function WithdrawButton() {
  const { address } = useAccount();
  const [amount, setAmount] = useState("");

  // Get user's max withdrawable
  const { data: shares } = useContractRead({
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

  const maxWithdraw =
    shares && sharePrice
      ? formatEther((shares * sharePrice) / BigInt(1e18))
      : "0";

  const sharesToBurn =
    amount && sharePrice
      ? (parseEther(amount) * BigInt(1e18)) / sharePrice
      : BigInt(0);

  const { write: withdraw, isLoading } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "withdraw",
    args: [sharesToBurn],
    onSuccess: () => {
      alert("Withdrawal successful!");
      setAmount("");
    },
  });

  return (
    <div>
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        max={maxWithdraw}
        placeholder="Amount in ETH"
      />
      <p className="text-sm text-gray-600">Max: {maxWithdraw} ETH</p>
      <button onClick={() => withdraw()} disabled={!amount || isLoading}>
        {isLoading ? "Withdrawing..." : "Withdraw"}
      </button>
    </div>
  );
}
```

## Transaction Handling

### Wait for Confirmation

```typescript
const hash = await walletClient.writeContract({...});

// Wait for 1 confirmation
const receipt = await publicClient.waitForTransactionReceipt({
  hash,
  confirmations: 1
});

if (receipt.status === 'success') {
  console.log('Transaction confirmed!');
}
```

### Handle Errors

```tsx
const { write: deposit } = useContractWrite({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "deposit",
  onError: (error) => {
    if (error.message.includes("insufficient funds")) {
      alert("Insufficient balance");
    } else if (error.message.includes("User denied")) {
      alert("Transaction rejected");
    } else {
      alert("Transaction failed: " + error.message);
    }
  },
});
```

## Gas Estimation

```typescript
// Estimate gas before transaction
const gas = await publicClient.estimateContractGas({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "deposit",
  value: parseEther("1.0"),
});

console.log(`Estimated gas: ${gas}`);

// Execute with gas limit
const hash = await walletClient.writeContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "deposit",
  value: parseEther("1.0"),
  gas: (gas * 120n) / 100n, // Add 20% buffer
});
```

## Event Monitoring

### Listen for Deposits

```typescript
const unwatch = publicClient.watchContractEvent({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  eventName: "Deposit",
  onLogs: (logs) => {
    logs.forEach((log) => {
      console.log("New deposit:", {
        user: log.args.user,
        amount: formatEther(log.args.amount),
        shares: formatEther(log.args.shares),
      });
    });
  },
});

// Stop watching
// unwatch();
```

### React Hook

```tsx
function useDepositEvents() {
  const [deposits, setDeposits] = useState([]);

  useContractEvent({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    eventName: "Deposit",
    listener: (logs) => {
      setDeposits((prev) => [...prev, ...logs]);
    },
  });

  return deposits;
}
```

## Complete Integration Example

```tsx
function VeilfiVault() {
  const { address } = useAccount();
  const [depositAmount, setDepositAmount] = useState("");
  const [withdrawAmount, setWithdrawAmount] = useState("");

  // Read data
  const { data: balance } = useUserPosition(address);
  const { data: apy } = useContractRead({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "getBlendedAPY",
  });

  // Write functions
  const { write: deposit, isLoading: depositing } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "deposit",
    value: depositAmount ? parseEther(depositAmount) : undefined,
  });

  const { write: withdraw, isLoading: withdrawing } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "withdraw",
  });

  return (
    <Card>
      <h2>Veilfi Vault</h2>

      <div className="mb-4">
        <p>Your Balance: {balance?.formattedValue} ETH</p>
        <p>Current APY: {apy / 100}%</p>
      </div>

      <div className="space-y-4">
        <div>
          <h3>Deposit</h3>
          <input
            type="number"
            value={depositAmount}
            onChange={(e) => setDepositAmount(e.target.value)}
          />
          <button onClick={() => deposit()} disabled={depositing}>
            Deposit
          </button>
        </div>

        <div>
          <h3>Withdraw</h3>
          <input
            type="number"
            value={withdrawAmount}
            onChange={(e) => setWithdrawAmount(e.target.value)}
          />
          <button onClick={() => withdraw()} disabled={withdrawing}>
            Withdraw
          </button>
        </div>
      </div>
    </Card>
  );
}
```

---

**Next**: [ZK Proof Generation](./zk-proof-generation) - Enable private deposits
