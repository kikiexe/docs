---
title: Admin Panel
sidebar_position: 4
---

# Admin Panel

⚠️ **Note**: For hackathon, most admin functions are automated via smart contracts.

## Monitoring Dashboard

```tsx
function AdminPanel() {
  return (
    <div className="container mx-auto p-8">
      <h1>Vault Monitoring</h1>

      {/* Read-only metrics */}
      <Grid cols={3}>
        <Metric label="Total TVL" value={tvl} />
        <Metric label="Active Users" value={userCount} />
        <Metric label="Blended APY" value={apy} />
      </Grid>

      {/* Strategy health */}
      <StrategyHealthCards />

      {/* Recent events */}
      <EventLog />
    </div>
  );
}
```

**Features**:

- View-only metrics
- Strategy health monitoring
- Event log
- No manual intervention needed (all automated)

---

**Next**: [Wallet Connector Component](../components/wallet-connector)
