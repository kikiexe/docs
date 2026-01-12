---
title: Dashboard
sidebar_position: 3
---

# Dashboard

Main user interface showing portfolio, yields, and actions.

## Layout

```tsx
function Dashboard() {
  return (
    <div className="container mx-auto p-8">
      <Grid cols={2} gap={6}>
        {/* Left: Portfolio Overview */}
        <PortfolioCard />

        {/* Right: Quick Actions */}
        <ActionsCard />

        {/* Full Width: Strategy Breakdown */}
        <StrategyCards span={2} />

        {/* Charts */}
        <APYChart />
        <AllocationPieChart />

        {/* Transaction History */}
        <TransactionHistory span={2} />
      </Grid>
    </div>
  );
}
```

## Portfolio Card

```tsx
function PortfolioCard() {
  const { data: balance } = useUserBalance();
  const { data: shares } = useUserShares();
  const { data: earnings } = useUserEarnings();

  return (
    <Card>
      <h2>Your Portfolio</h2>
      <Metric label="Total Balance" value={`${balance} ETH`} />
      <Metric label="Shares Owned" value={shares} />
      <Metric label="Total Earned" value={`${earnings} ETH`} />
      <Metric label="Current APY" value="7.2%" />
    </Card>
  );
}
```

## Actions Card

```tsx
function ActionsCard() {
  const [depositOpen, setDepositOpen] = useState(false);

  return (
    <Card>
      <h2>Actions</h2>
      <Button onClick={() => setDepositOpen(true)}>Deposit</Button>
      <Button variant="outline">Withdraw</Button>

      <DepositModal open={depositOpen} onClose={() => setDepositOpen(false)} />
    </Card>
  );
}
```

## Charts

```tsx
import { LineChart, Line, PieChart, Pie } from "recharts";

function APYChart() {
  const history = useAPYHistory();

  return (
    <Card>
      <h3>APY History (30 days)</h3>
      <LineChart data={history}>
        <Line dataKey="apy" stroke="#8884d8" />
      </LineChart>
    </Card>
  );
}
```

---

**Next**: [Admin Panel](./admin-panel)
