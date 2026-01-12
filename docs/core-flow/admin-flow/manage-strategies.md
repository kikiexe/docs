---
title: Manage Strategies
sidebar_position: 1
---

# Manage Strategies

Admin functions for adding, removing, and configuring yield strategies.

## Add New Strategy

```solidity
function addStrategy(
    address strategyAddress,
    uint256 allocationPercentage
) external onlyOwner {
    IStrategy newStrategy = IStrategy(strategyAddress);

    // Validation
    require(strategies.length < MAX_STRATEGIES, "Max strategies");
    require(allocationPercentage <= 50, "Exceeds max allocation");
    require(newStrategy.totalAssets() >= 0, "Invalid strategy");

    strategies.push(newStrategy);
    allocations.push(allocationPercentage);

    emit StrategyAdded(strategyAddress, allocationPercentage);
}
```

## Remove Strategy

```solidity
function removeStrategy(uint256 index) external onlyOwner {
    // Withdraw all assets first
    strategies[index].emergencyWithdraw();

    // Remove from array
    strategies[index] = strategies[strategies.length - 1];
    strategies.pop();

    allocations[index] = allocations[allocations.length - 1];
    allocations.pop();

    emit StrategyRemoved(index);
}
```

## Update Allocations

```tsx
function AllocationManager() {
  const [newAllocations, setNewAllocations] = useState([40, 30, 30]);

  const { write: updateAllocations } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "updateAllocations",
    args: [newAllocations],
  });

  return (
    <Card>
      <h2>Strategy Allocations</h2>
      {strategies.map((strategy, i) => (
        <Slider
          key={strategy.name}
          label={strategy.name}
          value={newAllocations[i]}
          onChange={(val) => {
            const updated = [...newAllocations];
            updated[i] = val;
            setNewAllocations(updated);
          }}
          min={10}
          max={50}
        />
      ))}

      <p>Total: {newAllocations.reduce((a, b) => a + b, 0)}%</p>

      <Button
        onClick={() => updateAllocations()}
        disabled={newAllocations.reduce((a, b) => a + b) !== 100}
      >
        Update Allocations
      </Button>
    </Card>
  );
}
```

---

**Next**: [Allocate Funds](./allocate-funds)
