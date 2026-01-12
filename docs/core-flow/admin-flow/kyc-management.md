---
title: KYC Management
sidebar_position: 4
---

# KYC Management

Admin interface for managing KYC requirements and reviewing compliance status.

## View KYC Status

```tsx
function KYCManagement() {
  const [users, setUsers] = useState([]);

  return (
    <Card>
      <h2>KYC Management</h2>

      <Table>
        <thead>
          <tr>
            <th>Address</th>
            <th>KYC Status</th>
            <th>Expiry</th>
            <th>Deposit Amount</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.address}>
              <td>{user.address}</td>
              <td>
                {user.kycVerified ? (
                  <Badge color="green">Verified</Badge>
                ) : (
                  <Badge color="gray">Not Verified</Badge>
                )}
              </td>
              <td>{new Date(user.kycExpiry * 1000).toLocaleDateString()}</td>
              <td>{user.depositAmount} ETH</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Card>
  );
}
```

## Update KYC Requirements

```solidity
function updateKYCThreshold(uint256 newThreshold) external onlyOwner {
    kycRequiredThreshold = newThreshold;
    emit KYCThresholdUpdated(newThreshold);
}
```

---

**Next**: [Privacy Flow](../privacy-flow/private-deposits)
