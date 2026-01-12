---
title: Deposit Funds
sidebar_position: 3
---

# Deposit Funds

Deposit ETH to Veilfi vault to start earning diversified yields across Aave, Lido, and Uniswap.

## Deposit Options

### Standard Deposit (Public)

Amount visible on-chain, simplest option:

```tsx
import { useContractWrite } from "wagmi";

function StandardDeposit() {
  const [amount, setAmount] = useState("");

  const { write: deposit } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "deposit",
    value: parseEther(amount),
  });

  return (
    <div>
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder="Amount in ETH"
      />
      <button onClick={() => deposit()}>Deposit {amount} ETH</button>
    </div>
  );
}
```

### Private Deposit (ZK Proof)

Amount hidden from public, enhanced privacy:

```tsx
async function privateDeposit(amount) {
  // 1. Generate ZK proof (hides amount)
  const proof = await generateDepositProof({
    amount: parseEther(amount),
    userSecret: wallet.privateKey,
  });

  // 2. Submit with proof
  const tx = await vault.depositWithProof(
    proof.a,
    proof.b,
    proof.c,
    proof.publicSignals,
    { value: parseEther(amount) }
  );

  await tx.wait();
}
```

## Deposit Flow

```
1. Enter amount
   ↓
2. Choose deposit type (Standard/Private)
   ↓
3. Review transaction details
   ↓
4. Sign in wallet
   ↓
5. Wait for confirmation
   ↓
6. Receive vault shares
   ↓
7. Start earning yield!
```

## Smart Contract Interaction

### Calculate Shares Received

```tsx
const { data: shares } = useContractRead({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "convertToShares",
  args: [parseEther(depositAmount)],
});

// Display: "You will receive ~X shares"
```

### Deposit Component

```tsx
function DepositComponent() {
  const [amount, setAmount] = useState("");
  const [usePrivacy, setUsePrivacy] = useState(false);
  const { address } = useAccount();

  const { data: balance } = useBalance({ address });
  const { data: sharePrice } = useContractRead({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "pricePerShare",
  });

  const estimatedShares =
    amount && sharePrice ? (parseEther(amount) / sharePrice).toFixed(4) : "0";

  return (
    <Card>
      <h2>Deposit to Vault</h2>

      <Input
        label="Amount (ETH)"
        value={amount}
        onChange={setAmount}
        max={balance?.formatted}
      />

      <InfoBox>
        <p>Share Price: {formatEther(sharePrice)} ETH</p>
        <p>You will receive: ~{estimatedShares} shares</p>
        <p>Current APY: 7.2%</p>
      </InfoBox>

      <Checkbox checked={usePrivacy} onChange={setUsePrivacy}>
        Use private deposit (hide amount on-chain)
      </Checkbox>

      <Button
        onClick={() =>
          usePrivacy ? privateDeposit(amount) : standardDeposit(amount)
        }
        disabled={!amount || parseFloat(amount) === 0}
      >
        Deposit {amount} ETH
      </Button>
    </Card>
  );
}
```

## Minimum & Maximum

- **Minimum**: 0.01 ETH (prevent dust)
- **Maximum**: 1000 ETH per transaction (gradually increase TVL cap)

## Fee Structure

- **Deposit Fee**: 0% (FREE)
- **Management Fee**: 1% annual (from yields)
- **Performance Fee**: 10% of profits
- **Withdrawal Fee**: 0.1% (anti-manipulation)

## After Deposit

1. **Shares Minted**: ERC-20 tokens representing your vault position
2. **Auto-Allocation**: Funds automatically allocated to strategies (40/30/30) via smart contract
3. **Yield Accrual**: Earn from Aave + Lido + Uniswap immediately
4. **Share Price Growth**: Your shares increase in value as yields compound

## Transaction Confirmation

```tsx
function DepositConfirmation({ txHash }) {
  return (
    <SuccessModal>
      <h2>✅ Deposit Successful!</h2>
      <p>Transaction: {txHash}</p>
      <p>Your funds are now earning 7% APY</p>
      <p>Funds allocated to strategies automatically</p>

      <Button href={`https://explorer.sepolia.mantle.xyz/tx/${txHash}`}>
        View on Explorer
      </Button>

      <Button to="/dashboard">View Dashboard</Button>
    </SuccessModal>
  );
}
```

---

**Next**: [View Yields](./view-yields) - Monitor your earnings.
