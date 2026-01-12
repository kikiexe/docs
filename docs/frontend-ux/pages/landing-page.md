---
title: Landing Page
sidebar_position: 1
---

# Landing Page

First impression page showcasing Veilfi's value proposition and key features.

## Design

### Hero Section

```tsx
function Hero() {
  return (
    <section className="bg-gradient-to-r from-purple-600 to-blue-600 text-white py-20">
      <div className="container mx-auto text-center">
        <h1 className="text-5xl font-bold mb-4">
          Privacy-Preserving Yield Aggregator
        </h1>
        <p className="text-xl mb-8">
          Earn 7% APY on ETH with Zero-Knowledge privacy
        </p>
        <ConnectButton />
      </div>
    </section>
  );
}
```

### Features Grid

```tsx
const features = [
  {
    icon: "🔒",
    title: "Privacy First",
    description: "ZK proofs hide your deposit amounts",
  },
  {
    icon: "📈",
    title: "7% APY",
    description: "Diversified across Aave, Lido, Uniswap",
  },
  {
    icon: "⚡",
    title: "Automated",
    description: "Set and forget yield optimization",
  },
];

function Features() {
  return (
    <div className="grid md:grid-cols-3 gap-8">
      {features.map((f) => (
        <FeatureCard key={f.title} {...f} />
      ))}
    </div>
  );
}
```

### Stats Section

```tsx
function Stats() {
  const { data: tvl } = useVaultTVL();
  const { data: apy } = useVaultAPY();

  return (
    <div className="grid md:grid-cols-3 gap-4">
      <Stat label="Total Value Locked" value={`${tvl} ETH`} />
      <Stat label="Current APY" value={`${apy}%`} />
      <Stat label="Active Users" value="250+" />
    </div>
  );
}
```

---

**Next**: [Login & KYC](./login-kyc)
