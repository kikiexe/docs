---
title: Yield Display
sidebar_position: 2
---

# Yield Display Component

Real-time yield and earnings display component.

## Implementation

```tsx
import { useContractRead } from "wagmi";
import { formatEther } from "viem";

export function YieldDisplay() {
  const { address } = useAccount();

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

  const { data: apy } = useContractRead({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "getBlendedAPY",
  });

  const totalValue =
    shares && sharePrice
      ? Number(formatEther((shares * sharePrice) / BigInt(1e18)))
      : 0;

  const dailyYield = totalValue * (apy / 100 / 365);

  return (
    <div className="grid md:grid-cols-3 gap-4">
      <MetricCard
        label="Total Value"
        value={`${totalValue.toFixed(4)} ETH`}
        icon="💰"
      />
      <MetricCard
        label="Current APY"
        value={`${apy}%`}
        icon="📈"
        trend="+0.5%"
      />
      <MetricCard
        label="Daily Yield"
        value={`${dailyYield.toFixed(6)} ETH`}
        icon="⚡"
      />
    </div>
  );
}
```

## MetricCard Component

```tsx
function MetricCard({ label, value, icon, trend }) {
  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
      <div className="flex justify-between items-start mb-2">
        <span className="text-sm text-gray-600 dark:text-gray-400">
          {label}
        </span>
        <span className="text-2xl">{icon}</span>
      </div>

      <div className="text-2xl font-bold mb-1">{value}</div>

      {trend && (
        <div className="text-sm text-green-600">{trend} vs yesterday</div>
      )}
    </div>
  );
}
```

## Features

✅ Real-time contract data  
✅ Auto-refresh on block updates  
✅ Responsive grid layout  
✅ Dark mode support  
✅ Trend indicators

---

**Next**: [Strategy Cards](./strategy-cards)
