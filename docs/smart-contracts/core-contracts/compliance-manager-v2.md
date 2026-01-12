---
title: ComplianceManagerV2
sidebar_position: 2
---

# ComplianceManagerV2

Manages ZK-KYC verification without storing personal data.

## Contract

```solidity
contract ComplianceManagerV2 {
    IGroth16Verifier public kycVerifier;

    mapping(address => KYCStatus) public kycStatus;

    struct KYCStatus {
        bool verified;
        uint256 expiryTimestamp;
        bytes32 proofHash;
    }
}
```

## Key Functions

### submitKYCProof()

```solidity
function submitKYCProof(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[1] memory publicSignals
) external {
    require(kycVerifier.verifyProof(a, b, c, publicSignals));
    require(publicSignals[0] == 1);

    kycStatus[msg.sender] = KYCStatus({
        verified: true,
        expiryTimestamp: block.timestamp + 365 days,
        proofHash: keccak256(abi.encode(a, b, c))
    });
}
```

### isKYCVerified()

```solidity
function isKYCVerified(address user) external view returns (bool) {
    KYCStatus memory status = kycStatus[user];
    return status.verified && block.timestamp < status.expiryTimestamp;
}
```

---

**Next**: [MockAaveStrategy](../strategy-contracts/mock-aave-strategy)
