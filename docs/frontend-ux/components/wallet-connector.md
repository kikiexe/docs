---
title: Wallet Connector
sidebar_position: 1
---

# Wallet Connector Component

Reusable wallet connection component using RainbowKit.

## Implementation

```tsx
import { ConnectButton } from "@rainbow-me/rainbowkit";

export function WalletConnector() {
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
              <button
                onClick={openConnectModal}
                className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700"
              >
                Connect Wallet
              </button>
            ) : chain.unsupported ? (
              <button
                onClick={openChainModal}
                className="bg-red-600 text-white px-6 py-3 rounded-lg"
              >
                Wrong Network
              </button>
            ) : (
              <div className="flex gap-2">
                <button
                  onClick={openChainModal}
                  className="bg-gray-200 px-4 py-2 rounded"
                >
                  {chain.name}
                </button>
                <button
                  onClick={openAccountModal}
                  className="bg-gray-200 px-4 py-2 rounded"
                >
                  {account.displayName}
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

## Features

✅ Multi-wallet support  
✅ Network switching  
✅ Account management  
✅ Custom styling  
✅ Error handling

## Usage

```tsx
import { WalletConnector } from "@/components/WalletConnector";

function Header() {
  return (
    <nav>
      <Logo />
      <WalletConnector />
    </nav>
  );
}
```

---

**Next**: [Yield Display](./yield-display)
