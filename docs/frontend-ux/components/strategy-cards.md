---
title: Strategy Cards
sidebar_position: 3
---

# Strategy Cards Component

Visual breakdown of strategy allocations and performance.

## Implementation

```tsx
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

const STRATEGIES = [
  {
    name: "Aave",
    allocation: 40,
    apy: 5.2,
    color: "#8884d8",
    icon: "🏦",
    risk: "Low",
  },
  {
    name: "Lido",
    allocation: 30,
    apy: 4.5,
    color: "#82ca9d",
    icon: "⛓️",
    risk: "Low",
  },
  {
    name: "Uniswap",
    allocation: 30,
    apy: 18.0,
    color: "#ffc658",
    icon: "🦄",
    risk: "Medium",
  },
];

export function StrategyCards() {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Strategy Allocation</h2>

      {/* Pie Chart */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg">
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={STRATEGIES}
              dataKey="allocation"
              nameKey="name"
              cx="50%"
              cy="50%"
              label
            >
              {STRATEGIES.map((strategy, index) => (
                <Cell key={index} fill={strategy.color} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Strategy Cards */}
      <div className="grid md:grid-cols-3 gap-4">
        {STRATEGIES.map((strategy) => (
          <StrategyCard key={strategy.name} {...strategy} />
        ))}
      </div>
    </div>
  );
}
```

## StrategyCard Component

```tsx
function StrategyCard({ name, allocation, apy, color, icon, risk }) {
  return (
    <div
      className="bg-white dark:bg-gray-800 p-6 rounded-lg border-l-4"
      style={{ borderColor: color }}
    >
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold">{name}</h3>
          <span className="text-sm text-gray-600">
            {allocation}% allocation
          </span>
        </div>
        <span className="text-3xl">{icon}</span>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between">
          <span className="text-sm text-gray-600">APY</span>
          <span className="font-semibold text-green-600">{apy}%</span>
        </div>

        <div className="flex justify-between">
          <span className="text-sm text-gray-600">Risk</span>
          <span
            className={`text-sm font-medium ${
              risk === "Low" ? "text-green-600" : "text-yellow-600"
            }`}
          >
            {risk}
          </span>
        </div>

        <ProgressBar value={allocation} max={100} color={color} />
      </div>
    </div>
  );
}
```

## ProgressBar Component

```tsx
function ProgressBar({ value, max, color }) {
  const percentage = (value / max) * 100;

  return (
    <div className="w-full bg-gray-200 rounded-full h-2">
      <div
        className="h-2 rounded-full transition-all duration-300"
        style={{
          width: `${percentage}%`,
          backgroundColor: color,
        }}
      />
    </div>
  );
}
```

## Features

✅ Visual allocation breakdown  
✅ Real-time APY display  
✅ Risk indicators  
✅ Interactive pie chart  
✅ Responsive grid layout

## Usage

```tsx
import { StrategyCards } from "@/components/StrategyCards";

function Dashboard() {
  return (
    <div>
      <YieldDisplay />
      <StrategyCards />
    </div>
  );
}
```

---

**Congratulations!** You've completed the **Frontend & UX** section.

**Next Steps**: Review [Integration Guide](../integration-guide/getting-started) or other documentation sections.
