---
title: Wallet Connection
sidebar_position: 1
---

# Wallet Connection

The first step for users to interact with Veilfi is connecting their Web3 wallet to the application.

## Supported Wallets

Veilfi supports all major Ethereum-compatible wallets through RainbowKit:

- **MetaMask** - Most popular browser extension
- **WalletConnect** - Mobile wallet connection
- **Coinbase Wallet** - Integrated with Coinbase
- **Rainbow Wallet** - Mobile-first wallet
- **Trust Wallet** - Multi-chain support

## Connection Flow

### Step-by-Step Process

```
1. User visits app.veilfi.xyz
   ↓
2. Click "Connect Wallet" button
   ↓
3. Select wallet provider
   ↓
4. Approve connection in wallet
   ↓
5. Network check (Mantle Sepolia)
   ↓
6. Connected! Show user dashboard
```

## Implementation

### Frontend Connection (RainbowKit)

```tsx
import "@rainbow-me/rainbowkit/styles.css";
import {
  RainbowKitProvider,
  connectorsForWallets,
  getDefaultWallets,
} from "@rainbow-me/rainbowkit";
import { configureChains, createConfig, WagmiConfig } from "wagmi";
import { mantleSepoliaTestnet } from "wagmi/chains";
import { publicProvider } from "wagmi/providers/public";

// Configure chains
const { chains, publicClient } = configureChains(
  [mantleSepoliaTestnet],
  [publicProvider()]
);

// Setup wallets
const { wallets } = getDefaultWallets({
  appName: "Veilfi",
  projectId: "YOUR_WALLETCONNECT_PROJECT_ID",
  chains,
});

const connectors = connectorsForWallets([...wallets]);

const wagmiConfig = createConfig({
  autoConnect: true,
  connectors,
  publicClient,
});

function App() {
  return (
    <WagmiConfig config={wagmiConfig}>
      <RainbowKitProvider chains={chains}>
        <YourApp />
      </RainbowKitProvider>
    </WagmiConfig>
  );
}
```

### Connect Button Component

```tsx
import { ConnectButton } from "@rainbow-me/rainbowkit";

export function CustomConnectButton() {
  return (
    <ConnectButton.Custom>
      {({
        account,
        chain,
        openAccountModal,
        openChainModal,
        openConnectModal,
        mounted,
      }) => {
        const connected = mounted && account && chain;

        return (
          <div>
            {!connected ? (
              <button onClick={openConnectModal} className="connect-btn">
                Connect Wallet
              </button>
            ) : chain.unsupported ? (
              <button onClick={openChainModal} className="wrong-network-btn">
                Wrong Network
              </button>
            ) : (
              <div className="wallet-info">
                <button onClick={openChainModal}>{chain.name}</button>
                <button onClick={openAccountModal}>
                  {account.displayName}
                  {account.displayBalance ? ` (${account.displayBalance})` : ""}
                </button>
              </div>
            )}
          </div>
        );
      }}
    </ConnectButton.Custom>
  );
}
```

## Network Configuration

### Mantle Sepolia Testnet

```javascript
const mantleSepoliaTestnet = {
  id: 5003,
  name: "Mantle Sepolia Testnet",
  network: "mantle-sepolia",
  nativeCurrency: {
    decimals: 18,
    name: "MNT",
    symbol: "MNT",
  },
  rpcUrls: {
    public: { http: ["https://rpc.sepolia.mantle.xyz"] },
    default: { http: ["https://rpc.sepolia.mantle.xyz"] },
  },
  blockExplorers: {
    default: {
      name: "Mantle Sepolia Explorer",
      url: "https://explorer.sepolia.mantle.xyz",
    },
  },
  testnet: true,
};
```

### Auto Network Switching

```tsx
import { useSwitchNetwork } from "wagmi";

function NetworkGuard({ children }) {
  const { chain } = useAccount();
  const { switchNetwork } = useSwitchNetwork();

  useEffect(() => {
    if (chain && chain.id !== 5003) {
      // Auto-switch to Mantle Sepolia
      switchNetwork?.(5003);
    }
  }, [chain, switchNetwork]);

  if (chain?.id !== 5003) {
    return (
      <div className="wrong-network">
        <p>Please switch to Mantle Sepolia</p>
        <button onClick={() => switchNetwork?.(5003)}>Switch Network</button>
      </div>
    );
  }

  return <>{children}</>;
}
```

## Account Management

### Display User Info

```tsx
import { useAccount, useBalance } from "wagmi";

function UserInfo() {
  const { address, isConnected } = useAccount();
  const { data: balance } = useBalance({ address });

  if (!isConnected) return null;

  return (
    <div className="user-info">
      <p>
        Address: {address?.slice(0, 6)}...{address?.slice(-4)}
      </p>
      <p>
        Balance: {balance?.formatted} {balance?.symbol}
      </p>
    </div>
  );
}
```

### Disconnect Handler

```tsx
import { useDisconnect } from "wagmi";

function DisconnectButton() {
  const { disconnect } = useDisconnect();

  return <button onClick={() => disconnect()}>Disconnect Wallet</button>;
}
```

## Security Considerations

### Best Practices

✅ **Always verify network** - Prevent wrong network transactions  
✅ **Show transaction confirmations** - Users review before signing  
✅ **Handle disconnections gracefully** - Clear state on disconnect  
✅ **Sanitize displayed addresses** - Prevent injection attacks  
✅ **Use HTTPS only** - Secure connection required

### Privacy Tips for Users

```markdown
For Maximum Privacy:

1. Use a fresh wallet address (not linked to your identity)
2. Fund wallet via DEX or privacy-preserving method
3. Use VPN when connecting (hide IP address)
4. Don't share wallet address publicly
5. Consider using hardware wallet for large amounts
```

## Error Handling

### Common Issues

```tsx
function WalletErrorHandler({ error }) {
  if (error?.message.includes("User rejected")) {
    return <Alert>You rejected the connection request</Alert>;
  }

  if (error?.message.includes("network")) {
    return <Alert>Network error. Please check your connection</Alert>;
  }

  if (error?.message.includes("unsupported")) {
    return <Alert>Please switch to Mantle Sepolia network</Alert>;
  }

  return <Alert>Failed to connect wallet: {error?.message}</Alert>;
}
```

## Testing Connection

### Local Development

```bash
# Add Mantle Sepolia to MetaMask manually:
Network Name: Mantle Sepolia Testnet
RPC URL: https://rpc.sepolia.mantle.xyz
Chain ID: 5003
Currency Symbol: MNT
Block Explorer: https://explorer.sepolia.mantle.xyz
```

### Getting Test MNT

```
1. Visit Mantle Sepolia Faucet
2. Enter your wallet address
3. Request test MNT
4. Wait for confirmation (~30 seconds)
```

---

**Next**: [KYC Verification](./kyc-verification) - Optional compliance step.
