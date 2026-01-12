---
title: Allocate Funds
sidebar_position: 2
---

# Allocate Funds

Deploy capital from vault to strategies according to target allocations.

## Allocation Function

```solidity
function allocateToStrategies() external onlyOwner {
    uint256 totalAssets = address(this).balance;
    require(totalAssets > 0, "Nothing to allocate");

    // Keep 10% reserve
    uint256 reserve = totalAssets * 10 / 100;
    uint256 allocatable = totalAssets - reserve;

    for (uint i = 0; i < strategies.length; i++) {
        uint256 amount = allocatable * allocations[i] / 100;
        strategies[i].deposit{value: amount}();
    }

    emit FundsAllocated(allocatable);
}
```

## Admin Interface

```tsx
function AllocationInterface() {
  const { data: vaultBalance } = useBalance({ address: VAULT_ADDRESS });

  const { write: allocate } = useContractWrite({
    address: VAULT_ADDRESS,
    abi: VAULT_ABI,
    functionName: "allocateToStrategies",
  });

  return (
    <Card>
      <h2>Allocate Funds</h2>
      <p>Unallocated Balance: {vaultBalance?.formatted} ETH</p>

      <AllocationPreview
        amount={parseFloat(vaultBalance?.formatted || "0")}
        allocations={[40, 30, 30]}
      />

      <Button onClick={() => allocate()}>Execute Allocation</Button>
    </Card>
  );
}
```

---

**Next**: [Harvest Yields](./harvest-yields)
