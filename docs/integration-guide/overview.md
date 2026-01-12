---
title: Integration Overview
sidebar_position: 1
---

# Integration Overview

Guide for developers integrating Veilfi into their applications or building on top of the protocol.

## Integration Options

### Option 1: Direct Contract Integration

Interact directly with Veilfi smart contracts:

```typescript
import { createPublicClient, http } from "viem";
import { mantleSepoliaTestnet } from "viem/chains";

const client = createPublicClient({
  chain: mantleSepoliaTestnet,
  transport: http("https://rpc.sepolia.mantle.xyz"),
});

const balance = await client.readContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "balanceOf",
  args: [userAddress],
});
```

### Option 2: React Hooks (Wagmi)

Use Wagmi hooks for React applications:

```tsx
import { useContractRead, useContractWrite } from "wagmi";

function VeilfiIntegration() {
  const { data: balance } = useContractRead({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "balanceOf",
    args: [address],
  });

  const { write: deposit } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "deposit",
  });

  return <div>Balance: {balance}</div>;
}
```

### Option 3: SDK (Future)

Veilfi SDK for simplified integration (coming soon):

```typescript
import { VeilfiSDK } from "@veilfi/sdk";

const veilfi = new VeilfiSDK({
  network: "mantle-sepolia",
  provider: window.ethereum,
});

await veilfi.deposit({ amount: "1.0" });
const balance = await veilfi.getBalance(userAddress);
```

## Prerequisites

### Required Knowledge

✅ Basic Solidity/Smart Contracts  
✅ Web3 libraries (ethers.js or viem)  
✅ TypeScript/JavaScript  
✅ React (for frontend integration)

### Required Tools

```bash
# Install dependencies
npm install viem wagmi @rainbow-me/rainbowkit
```

### Contract Addresses

```typescript
// Mantle Sepolia Testnet
export const CONTRACTS = {
  VAULT: "0x...", // StrategyVaultV2_Multi
  COMPLIANCE: "0x...", // ComplianceManagerV2
  AAVE_STRATEGY: "0x...",
  LIDO_STRATEGY: "0x...",
  UNISWAP_STRATEGY: "0x...",
};
```

## Quick Start

### 1. Setup Client

```typescript
import { createPublicClient, createWalletClient, http } from "viem";
import { mantleSepoliaTestnet } from "viem/chains";

const publicClient = createPublicClient({
  chain: mantleSepoliaTestnet,
  transport: http(),
});

const walletClient = createWalletClient({
  chain: mantleSepoliaTestnet,
  transport: http(),
});
```

### 2. Read Data

```typescript
const totalAssets = await publicClient.readContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "totalAssets",
});

console.log(`TVL: ${formatEther(totalAssets)} ETH`);
```

### 3. Write Data

```typescript
const hash = await walletClient.writeContract({
  address: VAULT_ADDRESS,
  abi: VAULT_ABI,
  functionName: "deposit",
  value: parseEther("1.0"),
});

await publicClient.waitForTransactionReceipt({ hash });
```

## Integration Patterns

### Pattern 1: Portfolio Tracker

Display user's Veilfi position:

```tsx
function MyVeilfiPosition() {
  const { address } = useAccount();
  const { data: shares } = useContractRead({...});
  const { data: sharePrice } = useContractRead({...});

  const value = shares * sharePrice / 1e18;

  return <div>Your Veilfi Position: {value} ETH</div>;
}
```

### Pattern 2: Aggregator Integration

Include Veilfi in yield aggregator:

```typescript
async function getVeilfiAPY() {
  const apy = await publicClient.readContract({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "getBlendedAPY",
  });

  return {
    protocol: "Veilfi",
    apy: Number(apy) / 100,
    tvl: await getTVL(),
    risk: "Low",
  };
}
```

### Pattern 3: DeFi Dashboard

Multi-protocol dashboard:

```tsx
function DeFiDashboard() {
  const veilfiBalance = useVeilfiBalance();
  const aaveBalance = useAaveBalance();
  // ... other protocols

  return (
    <Grid>
      <ProtocolCard protocol="Veilfi" balance={veilfiBalance} />
      <ProtocolCard protocol="Aave" balance={aaveBalance} />
    </Grid>
  );
}
```

## Testing Integration

### Local Testing

```bash
# Run local Hardhat node
npx hardhat node

# Deploy contracts
npx hardhat run scripts/deploy.js --network localhost

# Test integration
npm run test:integration
```

### Testnet Testing

```bash
# Switch to Mantle Sepolia
# Fund wallet with test MNT
# Test on live testnet contracts
```

## Common Use Cases

| Use Case                 | Complexity | Recommended Approach   |
| ------------------------ | ---------- | ---------------------- |
| **Read balances**        | Simple     | Direct contract read   |
| **Deposit/Withdraw**     | Medium     | Wagmi hooks            |
| **ZK Proof integration** | Advanced   | Custom implementation  |
| **Full dashboard**       | Advanced   | React + Wagmi + Charts |

## Support

Need help with integration?

- 📖 [Read Contract Data](./read-contract-data)
- 🔄 [Interact with Vault](./interact-with-vault)
- 🔐 [ZK Proof Generation](./zk-proof-generation)
- 💬 [Community Discord](#)
- 🐛 [GitHub Issues](#)

---

**Next**: [Read Contract Data](./read-contract-data) - Learn to query vault state
