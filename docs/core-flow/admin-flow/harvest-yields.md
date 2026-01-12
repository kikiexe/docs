---
title: Harvest Yields
sidebar_position: 3
---

# Harvest Yields

Collect yields from all strategies and distribute to vault shareholders.

## Harvest Function

```solidity
function harvestYields() external onlyOwner {
    uint256 totalYield = 0;

    for (uint i = 0; i < strategies.length; i++) {
        uint256 yield = strategies[i].harvest();
        totalYield += yield;
    }

    // Yields automatically increase totalAssets()
    // Share price appreciates

    emit YieldHarvested(totalYield);
}
```

## Harvest Interface

```tsx
function HarvestInterface() {
  const { data: pendingYields } = useContractRead({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "calculatePendingYields",
  });

  const { write: harvest } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "harvestYields",
  });

  return (
    <Card>
      <h2>Harvest Yields</h2>
      <p>Pending: {formatEther(pendingYields)} ETH</p>
      <p>Last Harvest: 2 days ago</p>

      <Button onClick={() => harvest()}>Harvest Now</Button>
    </Card>
  );
}
```

---

**Next**: [KYC Management](./kyc-management)
