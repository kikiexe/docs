---
title: Compliance Manager
sidebar_position: 2
---

# Compliance Manager

**ComplianceManagerV2** manages KYC verification through Zero-Knowledge proofs, enabling regulatory compliance without storing personal data.

## Contract Overview

```solidity
contract ComplianceManagerV2 {
    IGroth16Verifier public kycVerifier;

    mapping(address => KYCStatus) public kycStatus;
    mapping(bytes32 => bool) public usedProofs;

    struct KYCStatus {
        bool verified;
        uint256 expiryTimestamp;
        bytes32 proofHash;
    }
}
```

## Core Functions

### Submit KYC Proof

```solidity
function submitKYCProof(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[1] memory publicSignals  // isValid: 1 or 0
) external {
    // Verify ZK proof
    require(kycVerifier.verifyProof(a, b, c, publicSignals));
    require(publicSignals[0] == 1, "KYC not valid");

    // Mark user as KYC-verified
    kycStatus[msg.sender] = KYCStatus({
        verified: true,
        expiryTimestamp: block.timestamp + 365 days,
        proofHash: keccak256(abi.encode( a, b, c))
    });

    emit KYCVerified(msg.sender);
}
```

### Check KYC Status

```solidity
function isKYCVerified(address user) external view returns (bool) {
    KYCStatus memory status = kycStatus[user];

    // Check verified AND not expired
    return status.verified && block.timestamp < status.expiryTimestamp;
}
```

## Privacy Guarantees

**Stored On-Chain**:

- ✅ Proof hash (meaningless without secrets)
- ✅ Verification status (true/false)
- ✅ Expiry timestamp

**NOT Stored**:

- ❌ Name, passport, address
- ❌ KYC provider details
- ❌ Any PII

**Result**: Compliance without surveillance.

---

**Next**: [ZK Verifier](./zk-verifier)
