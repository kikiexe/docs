---
title: Tech Stack Overview
sidebar_position: 1
---

# Tech Stack Overview

Veilfi's frontend is built with modern web technologies optimized for Web3 and DeFi applications.

## Core Stack

### Framework: Next.js 14

```
Why Next.js?
✅ Server-side rendering for SEO
✅ File-based routing
✅ API routes for backend logic
✅ Optimized production builds
✅ Great developer experience
```

### Styling: TailwindCSS

```
Why Tailwind?
✅ Utility-first CSS
✅ Consistent design system
✅ Small bundle size (tree-shaking)
✅ Dark mode support
✅ Responsive by default
```

### Web3 Integration

#### RainbowKit + Wagmi

```tsx
import { RainbowKitProvider } from "@rainbow-me/rainbowkit";
import { WagmiConfig } from "wagmi";

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

**Features**:

- Beautiful wallet connection UI
- Multi-wallet support
- Network switching
- Transaction handling
- Account management

## Technology Breakdown

### Frontend Libraries

| Library         | Purpose                     | Version |
| --------------- | --------------------------- | ------- |
| **Next.js**     | React framework             | 14.x    |
| **React**       | UI library                  | 18.x    |
| **TypeScript**  | Type safety                 | 5.x     |
| **TailwindCSS** | Styling                     | 3.x     |
| **RainbowKit**  | Wallet connection           | 2.x     |
| **Wagmi**       | React hooks for Ethereum    | 2.x     |
| **Viem**        | TypeScript Ethereum library | 2.x     |
| **Recharts**    | Data visualization          | 2.x     |
| **SnarkJS**     | ZK proof generation         | 0.7.x   |

### Development Tools

```json
{
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/node": "^20.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "hardhat": "^2.19.0"
  }
}
```

## Project Structure

```
veilfi-frontend/
├── src/
│   ├── app/              # Next.js 14 app directory
│   │   ├── page.tsx      # Landing page
│   │   ├── dashboard/    # Dashboard route
│   │   └── layout.tsx    # Root layout
│   │
│   ├── components/       # Reusable components
│   │   ├── WalletConnector.tsx
│   │   ├── YieldDisplay.tsx
│   │   └── StrategyCards.tsx
│   │
│   ├── contracts/        # Contract ABIs & addresses
│   │   ├── abis/
│   │   └── addresses.ts
│   │
│   ├── hooks/            # Custom React hooks
│   │   ├── useVaultData.ts
│   │   └── useStrategies.ts
│   │
│   └── lib/              # Utilities
│       ├── wagmi.ts      # Wagmi config
│       └── zkProofs.ts   # ZK proof generation
│
├── public/               # Static assets
│   ├── circuits/         # ZK circuit files
│   └── images/
│
└── tailwind.config.js    # Tailwind configuration
```

## Key Features

### Responsive Design

```tsx
// Mobile-first approach
<div
  className="
  px-4 py-6           // Mobile
  md:px-8 md:py-12    // Tablet
  lg:px-16 lg:py-16   // Desktop
"
>
  <Content />
</div>
```

### Dark Mode Support

```tsx
// Automatic dark mode
<div className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-white
">
```

### Performance Optimization

```tsx
// Image optimization
import Image from "next/image";

<Image src="/logo.png" alt="Veilfi" width={200} height={50} priority />;

// Code splitting
const DashboardChart = dynamic(() => import("@/components/DashboardChart"), {
  loading: () => <Skeleton />,
});
```

## Web3 Tooling

### Contract Interaction

```tsx
import { useContractRead, useContractWrite } from "wagmi";

function DepositButton() {
  const { write: deposit } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "deposit",
  });

  return (
    <button onClick={() => deposit({ value: parseEther("1") })}>
      Deposit 1 ETH
    </button>
  );
}
```

### ZK Proof Generation

```tsx
import { groth16 } from "snarkjs";

async function generateProof(amount: bigint) {
  const { proof, publicSignals } = await groth16.fullProve(
    { amount: amount.toString() },
    "/circuits/deposit.wasm",
    "/circuits/deposit_final.zkey"
  );

  return { proof, publicSignals };
}
```

## Development Workflow

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint

# Format code
npm run format
```

## Environment Variables

```.env
# Network
NEXT_PUBLIC_CHAIN_ID=5003
NEXT_PUBLIC_RPC_URL=https://rpc.sepolia.mantle.xyz

# Contracts
NEXT_PUBLIC_VAULT_ADDRESS=0x...
NEXT_PUBLIC_COMPLIANCE_ADDRESS=0x...

# WalletConnect
NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=...
```

---

**Next**: [Landing Page](./pages/landing-page) - First user touchpoint
