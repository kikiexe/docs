---
title: KYC Compliance
sidebar_position: 4
---

# KYC Compliance

Know Your Customer (KYC) compliance ensures users

are verified and meet regulatory requirements. Veilfi implements **privacy-preserving KYC** through Zero-Knowledge proofs, enabling regulatory compliance without exposing personal information on-chain.

## What is KYC in DeFi?

### Traditional KYC (Centralized Exchanges)

**Process**:

```
1. User submits documents: Passport, ID, selfie
2. Exchange stores personal data in database
3. Exchange verifies identity manually/automatically
4. User approved or rejected
```

**Problems**:

- 🔴 Personal data centralized (breach risk)
- 🔴 Full identity exposure to company
- 🔴 Data sold to third parties
- 🔴 Government requests expose users

**Examples**: Coinbase, Binance, Kraken

### DeFi's KYC Challenge

Most DeFi protocols have **zero KYC**:

- ✅ Permissionless (anyone can use)
- ✅ Privacy-preserving (no data collection)
- ❌ Regulatory scrutiny (AML/CTF concerns)
- ❌ Institutional barriers (compliance requirements)

**Result**: Institutions can't use DeFi without regulatory clarity.

## Veilfi's Zero-Knowledge KYC

### The Innovation: ZK-KYC

**Concept**: Prove you're KYC-verified **without revealing your identity**.

```
Traditional KYC: "Here's my passport" → Identity exposed
ZK-KYC: "I have a valid KYC certificate" → Identity hidden
```

### How It Works

#### Step 1: Off-Chain KYC Verification

User completes KYC with trusted provider:

```
User → KYC Provider (e.g., Civic, Onfido, Synaps)
     ↓
Provider verifies:
├─ Government ID
├─ Proof of address
├─ Liveness check (selfie)
└─ AML/sanctions screening
     ↓
Provider issues: KYC Certificate
{
  userId: "user123",
  kycHash: hash(passport + timestamp),
  expiryDate: "2025-12-31",
  signature: provider's cryptographic signature
}
```

**Key Point**: This happens OFF-CHAIN (no blockchain yet).

#### Step 2: Generate ZK Proof

User generates cryptographic proof locally:

```circom
template KYCVerification() {
    // Private inputs (never revealed)
    signal private input userId;
    signal private input kycHash;
    signal private input timestamp;
    signal private input providerSignature;

    // Public output (goes on-chain)
    signal public output isValid;

    // Verify provider's signature
    component sigCheck = ECDSAVerify();
    sigCheck.signature <== providerSignature;
    sigCheck.message <== hash(userId, kycHash, timestamp);

    // Check expiry
    component dateCheck = TimestampValid();
    dateCheck.timestamp <== timestamp;
    dateCheck.currentTime <== getCurrentTime();

    // Output 1 if valid, 0 otherwise
    isValid <== sigCheck.valid AND dateCheck.valid;
}
```

**Proof Generation** (User's Browser):

```javascript
const proof = await generateKYCProof({
  userId: "user123", // PRIVATE
  kycHash: "0x7a3f...", // PRIVATE
  timestamp: 1704067200, // PRIVATE
  providerSignature: "0xabc...", // PRIVATE
});

// Proof created locally, secrets never leave user's device
```

#### Step 3: Submit Proof On-Chain

Smart contract verifies proof:

```solidity
contract ComplianceManagerV2 {
    mapping(address => bool) public isKYCVerified;

    function submitKYCProof(
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[1] memory publicSignals  // Only isValid (1 or 0)
    ) external {
        // Verify ZK proof
        bool proofValid = zkVerifier.verifyProof(a, b, c, publicSignals);
        require(proofValid, "Invalid KYC proof");

        // Mark user as KYC'd
        require(publicSignals[0] == 1, "KYC not valid");
        isKYCVerified[msg.sender] = true;

        emit KYCVerified(msg.sender);  // Public event
    }
}
```

**What's Stored On-Chain**:

```
✅ Wallet address: 0xAlice...
✅ KYC status: true
✅ Proof hash: 0x9f2e... (meaningless to outsiders)
❌ NO name, passport, address, or personal data
```

### Privacy Guarantees

**What Blockchain Knows**:

- ✅ This wallet is KYC-verified
- ✅ Proof was valid at time of submission

**What Blockchain CANNOT Know**:

- ❌ User's real name
- ❌ Passport number
- ❌ Date of birth
- ❌ Address
- ❌ Which KYC provider was used

**Result**: Compliance without surveillance.

## Benefits of ZK-KYC

### For Users

✅ **Privacy Preserved**: No PII on public blockchain  
✅ **Control**: You decide what to reveal (and to whom)  
✅ **Reusability**: One KYC proof, multiple protocols  
✅ **Security**: No centralized honeypot of user data

### For Institutions

✅ **Regulatory Compliance**: Meet AML/KYC requirements  
✅ **Reduced Liability**: No user data storage = no breach risk  
✅ **DeFi Access**: Use privacy-preserving protocols compliantly  
✅ **Auditor-Friendly**: Can selectively disclose to regulators

### For Veilfi Protocol

✅ **Institutional Adoption**: Compliance opens doors  
✅ **Regulatory Defense**: Not anonymity tool, but privacy tool  
✅ **Selective Access**: Can require KYC for large deposits  
✅ **Flexible Model**: KYC optional for small users, required for whales

## Compliance Tiers

Veilfi supports **tiered compliance** based on deposit size:

| Tier       | Deposit Limit | KYC Required | Privacy Level   |
| ---------- | ------------- | ------------ | --------------- |
| **Tier 1** | < 1 ETH       | ❌ No        | 🟢 Full Privacy |
| **Tier 2** | 1-100 ETH     | ⚠️ Optional  | 🟢 Full Privacy |
| **Tier 3** | > 100 ETH     | ✅ ZK-KYC    | 🟢 Full Privacy |

**Rationale**: Small users = no KYC burden; large users = compliance for institutions.

### Example: Tiered Access

```solidity
function deposit() external payable {
    if (msg.value > 100 ether) {
        // Large deposit requires KYC
        require(complianceManager.isKYCVerified(msg.sender), "KYC required");
    }
    // Process deposit
    _processDeposit(msg.sender, msg.value);
}
```

**Benefit**: Balances privacy (small users) with compliance (institutions).

## ZK-KYC vs Alternatives

| Approach                     | Privacy    | Compliance | User Friction | Protocol Risk        |
| ---------------------------- | ---------- | ---------- | ------------- | -------------------- |
| **No KYC** (Most DeFi)       | ✅ Full    | ❌ None    | 🟢 Zero       | 🔴 High (regulatory) |
| **Public KYC** (Coinbase)    | ❌ None    | ✅ Full    | 🔴 High       | 🟢 Low (compliant)   |
| **Allowlist** (Permissioned) | 🟡 Partial | 🟡 Partial | 🔴 High       | 🟡 Medium            |
| **🎯 ZK-KYC** (Veilfi)       | ✅ Full    | ✅ Full    | 🟡 Medium     | 🟢 Low               |

**Veilfi's Advantage**: Only solution with BOTH privacy AND compliance.

## Regulatory Perspective

### What Regulators Want

1. **AML Compliance**: Prevent money laundering
2. **Sanctions Screening**: Block sanctioned entities
3. **Audibility**: Ability to investigate suspicious activity
4. **Transparency**: Access to data when legally required

### How ZK-KYC Satisfies Regulators

✅ **AML**: Users verified by licensed KYC providers (off-chain)  
✅ **Sanctions**: Can integrate OFAC screening in KYC process  
✅ **Audibility**: Users can selectively disclose to authorities  
✅ **Transparency**: Regulators can request user to reveal KYC (user controls)

**Key Difference from Tornado Cash**:

```
Tornado Cash: No compliance mechanism → Sanctioned
Veilfi: ZK-KYC + selective disclosure → Compliant
```

## Selective Disclosure

**Concept**: Users can prove compliance to specific parties without public exposure.

### Example: Tax Auditor Request

```
Tax Authority: "Prove you earned yield and paid taxes"
↓
User generates ZK proof:
├─ "I earned between $10k-$50k in yield" (range proof)
├─ "I paid taxes on this income" (tax receipt hash)
└─ "I am this KYC-verified person" (identity proof)
↓
Tax Authority verifies proof
↓
Tax Authority learns: User complied with tax law
Tax Authority CANNOT see: Exact yield amount or full balance
```

**Result**: Selective compliance without full financial exposure.

## Privacy vs. Anonymity

### Important Distinction

**Anonymity** (Tornado Cash):

```
- No identity tied to transactions
- Impossible to trace
- Regulatory nightmare
```

**Privacy** (Veilfi):

```
- Identity verifiable (via ZK proof)
- Traceable if user chooses to disclose
- Regulatory compatible
```

**Veilfi's Stance**:

> "Privacy is a right. Anonymity is a choice. We provide privacy with accountability."

## Implementation Details

### KYC Provider Integration

Veilfi supports multiple KYC providers:

- **Civic**: Decentralized identity
- **Onfido**: AI-powered verification
- **Synaps**: Compliance-as-a-service
- **Custom APIs**: Enterprises can use internal KYC

**Integration Flow**:

```javascript
// User completes KYC with provider
const kycResult = await provider.verifyUser({
  document: passport,
  selfie: userPhoto,
});

// If approved, provider returns certificate
if (kycResult.status === "APPROVED") {
  const cert = kycResult.certificate;

  // User generates ZK proof
  const proof = await generateKYCProof(cert);

  // Submit to Veilfi
  await veilfiCompliance.submitKYCProof(proof);
}
```

### Proof Expiry & Renewal

**Problem**: KYC certificates expire (usually 1 year).

**Solution**: Renewable ZK proofs.

```solidity
struct KYCStatus {
    bool verified;
    uint256 expiryTimestamp;
}

mapping(address => KYCStatus) public kycStatus;

function renewKYC(proof) external {
    // Verify new proof
    bool valid = zkVerifier.verify(proof);
    require(valid, "Invalid renewal proof");

    // Update expiry (new 1-year period)
    kycStatus[msg.sender].expiryTimestamp = block.timestamp + 365 days;
}
```

**User Experience**: Once/year renewal (similar to passport renewal).

---

**Next**: Explore [Core Principles](../core-principles/privacy-first) to understand Veilfi's design philosophy.

**Technical Details**: See [ComplianceManagerV2](../../smart-contracts/core-contracts/compliance-manager-v2) contract.
