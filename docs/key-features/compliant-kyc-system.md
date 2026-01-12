---
title: Compliant KYC System
sidebar_position: 3
---

# Compliant KYC System

Veilfi's Zero-Knowledge KYC enables regulatory compliance without compromising user privacy.

## The KYC Dilemma

### Traditional KYC (Privacy Loss)

```
User submits:
├─ Full name
├─ Passport scan
├─ Address proof
├─ Selfie photo
└─ All stored on-chain or centralized DB

Result: Complete identity exposure
```

### Veilfi ZK-KYC (Privacy Preserved)

```
User submits:
├─ KYC done off-chain with provider
├─ Generate ZK proof of verification
└─ Submit proof to smart contract

Blockchain sees: "User is KYC-verified" ✅
Blockchain doesn't see: Any personal data ❌
```

## How ZK-KYC Works

### Step 1: Off-Chain Verification

```
User → KYC Provider (Civic/Onfido/Synaps)
     → Upload documents
     → Provider verifies identity
     → Receive signed KYC certificate
```

### Step 2: Generate ZK Proof

```tsx
const proof = await generateKYCProof({
  userId: certificate.userId, // PRIVATE
  kycHash: certificate.hash, // PRIVATE
  timestamp: certificate.timestamp, // PRIVATE
  providerSignature: certificate.sig, // PRIVATE
});

// Proof proves: "I am KYC-verified"
// Proof doesn't reveal: WHO you are
```

### Step 3: On-Chain Submission

```solidity
function submitKYCProof(...) external {
    require(kycVerifier.verifyProof(a, b, c, publicSignals));
    require(publicSignals[0] == 1, "KYC not valid");

    // Mark user as verified (no PII stored)
    kycStatus[msg.sender] = KYCStatus({
        verified: true,
        expiryTimestamp: block.timestamp + 365 days,
        proofHash: keccak256(abi.encode(a, b, c))
    });
}
```

## Tiered Compliance

### Tier 1: No KYC (Retail)

```
Deposit limit: < 10 ETH
Requirements: None
Privacy: Maximum
Use case: Individual users, privacy-focused
```

### Tier 2: Optional KYC (Standard)

```
Deposit limit: 10-100 ETH
Requirements: Recommended KYC
Privacy: High (ZK-KYC)
Use case: Larger deposits, better rates
```

### Tier 3: Required KYC (Institutional)

```
Deposit limit: > 100 ETH
Requirements: Mandatory ZK-KYC
Privacy: Medium (verified status public)
Use case: Institutions, DAOs, compliance-required
```

## Privacy Guarantees

### What's Stored On-Chain

```solidity
struct KYCStatus {
    bool verified;              // true/false only
    uint256 expiryTimestamp;    // When verification expires
    bytes32 proofHash;          // Meaningless without inputs
}
```

### What's NOT Stored

❌ Name  
❌ Passport/ID number  
❌ Date of birth  
❌ Address  
❌ Photo  
❌ KYC provider details  
❌ Any personally identifiable information

## Regulatory Advantages

### For Users

✅ **Privacy**: Identity stays off-chain  
✅ **Control**: Users manage their data  
✅ **Portability**: One KYC, multiple platforms  
✅ **Revocation**: Can remove verification

### For Institutions

✅ **Compliance**: Meet regulatory requirements  
✅ **Privacy**: Don't store sensitive PII  
✅ **Auditable**: Verification status provable  
✅ **Scalable**: No centralized database

### For Regulators

✅ **Verifiable**: Can confirm users are KYC'd  
✅ **Selective Disclosure**: Access with court order  
✅ **Transparent**: All verifications on-chain  
✅ **Traceable**: Audit trail of compliance

## KYC Providers

### Supported Providers

| Provider   | Type          | Features                |
| ---------- | ------------- | ----------------------- |
| **Civic**  | Decentralized | On-chain attestations   |
| **Onfido** | Centralized   | AI-powered verification |
| **Synaps** | Hybrid        | ZK-ready integration    |

### Integration Example

```javascript
// Civic integration
import { CivicPass } from "@civic/pass";

async function getKYCCertificate() {
  const civic = new CivicPass();

  // User completes KYC with Civic
  const pass = await civic.verify();

  // Generate Veilfi-compatible proof
  const certificate = {
    userId: pass.userId,
    hash: pass.kycHash,
    timestamp: pass.timestamp,
    signature: pass.signature,
  };

  return certificate;
}
```

## Expiry & Renewal

### Automatic Expiry

```solidity
// KYC expires after 1 year
uint256 public constant KYC_VALIDITY = 365 days;

function isKYCValid(address user) external view returns (bool) {
    KYCStatus memory status = kycStatus[user];

    return status.verified &&
           block.timestamp < status.expiryTimestamp;
}
```

### Renewal Process

```
1. KYC expires after 365 days
   ↓
2. User re-verifies with provider
   ↓
3. Generate new ZK proof
   ↓
4. Submit to contract (extends validity)
```

## Privacy vs Compliance Balance

```
Maximum Privacy          Maximum Compliance
      ←─────────────────────────→
      │                         │
 No KYC              Full Traditional KYC
 (Tornado)           (Coinbase)
                │
                ↓
            Veilfi ZK-KYC
        (Sweet spot)
```

**Veilfi Position**: Regulatory compliant without sacrificing privacy

---

**Next**: [Automated Yield Optimization](./automated-yield-optimization) - Set and forget earning.
