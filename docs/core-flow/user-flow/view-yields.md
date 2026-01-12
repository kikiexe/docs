---
title: View Yields
sidebar_position: 4
---

# View Yields

Monitor your earnings, track portfolio performance, and view detailed analytics on your Veilfi dashboard.

## Dashboard Overview

```tsx
function Dashboard() {
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

  const totalValue = shares && sharePrice ? (shares * sharePrice) / 1e18 : 0;

  return (
    <Grid>
      <MetricCard title="Your Shares" value={formatUnits(shares, 18)} />
      <MetricCard
        title="Share Price"
        value={`${formatEther(sharePrice)} ETH`}
      />
      <MetricCard title="Total Value" value={`${totalValue.toFixed(4)} ETH`} />
      <MetricCard title="Current APY" value="7.2%" />
    </Grid>
  );
}
```

## Yield Tracking

### Current Earnings

```tsx
function EarningsDisplay() {
  const { initialDeposit, currentValue } = useUserPosition();

  const earnings = currentValue - initialDeposit;
  const earningsPercent = (currentValue / initialDeposit - 1) * 100;

  return (
    <Card>
      <h3>Your Earnings</h3>
      <BigNumber value={earnings.toFixed(4)} unit="ETH" />
      <Percentage
        value={earningsPercent}
        color={earnings > 0 ? "green" : "red"}
      />

      <p>Since deposit {daysAgo} days ago</p>
    </Card>
  );
}
```

### Projected Returns

```javascript
function calculateProjectedEarnings(principal, apy, days) {
  const dailyRate = apy / 365 / 100;
  const futureValue = principal * Math.pow(1 + dailyRate, days);

  return {
    in7Days: futureValue - principal,
    in30Days: principal * Math.pow(1 + dailyRate, 30) - principal,
    in365Days: principal * (apy / 100),
  };
}

// Example: 10 ETH @ 7% APY
// 7 days: 0.0134 ETH
// 30 days: 0.0575 ETH
// 365 days: 0.7 ETH
```

## Performance Charts

### APY Over Time

```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

function APYChart({ data }) {
  return (
    <LineChart width={600} height={300} data={data}>
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="apy" stroke="#8884d8" />
    </LineChart>
  );
}
```

### Portfolio Value

```tsx
function PortfolioChart() {
  const history = usePortfolioHistory();

  return (
    <AreaChart data={history}>
      <Area type="monotone" dataKey="value" fill="#82ca9d" />
      <XAxis dataKey="date" />
      <YAxis />
    </AreaChart>
  );
}
```

## Strategy Allocation View

```tsx
function AllocationPieChart() {
  const allocations = [
    { name: "Aave", value: 40, apy: 5 },
    { name: "Lido", value: 30, apy: 4.5 },
    { name: "Uniswap", value: 30, apy: 18 },
  ];

  return (
    <PieChart width={400} height={400}>
      <Pie
        data={allocations}
        dataKey="value"
        nameKey="name"
        cx="50%"
        cy="50%"
        label
      />
      <Tooltip />
    </PieChart>
  );
}
```

## Transaction History

```tsx
function TransactionHistory() {
  const { address } = useAccount();
  const transactions = useTransactions(address);

  return (
    <Table>
      <thead>
        <tr>
          <th>Type</th>
          <th>Amount</th>
          <th>Date</th>
          <th>Tx</th>
        </tr>
      </thead>
      <tbody>
        {transactions.map((tx) => (
          <tr key={tx.hash}>
            <td>{tx.type}</td>
            <td>{tx.amount} ETH</td>
            <td>{new Date(tx.timestamp * 1000).toLocaleDateString()}</td>
            <td>
              <a href={`https://explorer.sepolia.mantle.xyz/tx/${tx.hash}`}>
                View
              </a>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}
```

---

**Next**: [Withdraw Funds](./withdraw-funds) - Exit your position.
