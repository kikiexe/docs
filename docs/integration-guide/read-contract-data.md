---
title: Read Contract Data
sidebar_position: 2
---

# Read Contract Data

Learn how to query Veilfi vault state and metrics.

## Essential Read Functions

### Get Total Assets (TVL)

```typescript
const totalAssets = await publicClient.readContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "totalAssets",
});

console.log(`Total TVL: ${formatEther(totalAssets)} ETH`);
```

### Get Share Price

```typescript
const pricePerShare = await publicClient.readContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "pricePerShare",
});

console.log(`1 share = ${formatEther(pricePerShare)} ETH`);
```

### Get User Balance

```typescript
const shares = await publicClient.readContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "balanceOf",
  args: [userAddress],
});

const value = (shares * pricePerShare) / BigInt(1e18);
console.log(`User has ${formatEther(value)} ETH in vault`);
```

### Get Current APY

```typescript
const blendedAPY = await publicClient.readContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "getBlendedAPY",
});

console.log(`Current APY: ${blendedAPY / 100}%`);
```

## Strategy Data

### Get Strategy Allocations

```typescript
const allocations = await publicClient.readContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "getAllocations",
});

// Returns: [40, 30, 30] (percentages)
console.log("Aave:", allocations[0], "%");
console.log("Lido:", allocations[1], "%");
console.log("Uniswap:", allocations[2], "%");
```

### Get Strategy Assets

```typescript
const aaveAssets = await publicClient.readContract({
  address: AAVE_STRATEGY_ADDRESS,
  abi: STRATEGY_ABI,
  functionName: "totalAssets",
});

console.log(`Aave has ${formatEther(aaveAssets)} ETH`);
```

### Get Strategy APYs

```typescript
const strategies = [AAVE_STRATEGY, LIDO_STRATEGY, UNISWAP_STRATEGY];

const apys = await Promise.all(
  strategies.map((addr) =>
    publicClient.readContract({
      address: addr,
      abi: STRATEGY_ABI,
      functionName: "apy",
    })
  )
);

console.log("Aave APY:", apys[0] / 100, "%");
console.log("Lido APY:", apys[1] / 100, "%");
console.log("Uniswap APY:", apys[2] / 100, "%");
```

## React Hooks

### useVaultData Hook

```tsx
import { useContractReads } from "wagmi";

function useVaultData() {
  const { data } = useContractReads({
    contracts: [
      {
        address: VAULT_ADDRESS,
        abi: VAULT_ABI,
        functionName: "totalAssets",
      },
      {
        address: VAULT_ADDRESS,
        abi: VAULT_ABI,
        functionName: "totalSupply",
      },
      {
        address: VAULT_ADDRESS,
        abi: VAULT_ABI,
        functionName: "pricePerShare",
      },
      {
        address: VAULT_ADDRESS,
        abi: VAULT_ABI,
        functionName: "getBlendedAPY",
      },
    ],
  });

  return {
    totalAssets: data?.[0],
    totalShares: data?.[1],
    sharePrice: data?.[2],
    apy: data?.[3],
  };
}
```

### useUserPosition Hook

```tsx
function useUserPosition(address: Address) {
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

  const value =
    shares && sharePrice ? (shares * sharePrice) / BigInt(1e18) : BigInt(0);

  return {
    shares,
    value,
    formattedValue: formatEther(value),
  };
}
```

## Dashboard Example

```tsx
function VeilfiDashboard() {
  const { address } = useAccount();
  const vaultData = useVaultData();
  const userPosition = useUserPosition(address);

  return (
    <div className="grid md:grid-cols-3 gap-4">
      <MetricCard
        label="Total TVL"
        value={`${formatEther(vaultData.totalAssets)} ETH`}
      />
      <MetricCard label="Current APY" value={`${vaultData.apy / 100}%`} />
      <MetricCard
        label="Your Position"
        value={`${userPosition.formattedValue} ETH`}
      />
    </div>
  );
}
```

## Batch Reading

Optimize multiple reads with multicall:

```typescript
const results = await publicClient.multicall({
  contracts: [
    { address: VAULT_ADDRESS, abi: VAULT_ABI, functionName: "totalAssets" },
    { address: VAULT_ADDRESS, abi: VAULT_ABI, functionName: "pricePerShare" },
    { address: AAVE_STRATEGY, abi: STRATEGY_ABI, functionName: "apy" },
    { address: LIDO_STRATEGY, abi: STRATEGY_ABI, functionName: "apy" },
    { address: UNISWAP_STRATEGY, abi: STRATEGY_ABI, functionName: "apy" },
  ],
});

// Single RPC call instead of 5 separate calls
```

---

**Next**: [Interact with Vault](./interact-with-vault) - Learn to deposit and withdraw
