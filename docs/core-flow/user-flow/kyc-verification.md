---
title: KYC Verification
sidebar_position: 2
---

# KYC Verification

Optional KYC verification for institutional users and those depositing large amounts (&gt;100 ETH) through privacy-preserving Zero-Knowledge proofs.

## When is KYC Required?

| User Type     | Deposit Amount | KYC Required   |
| ------------- | -------------- | -------------- |
| Retail        | &lt; 10 ETH    | ❌ Optional    |
| Standard      | 10-100 ETH     | ⚠️ Recommended |
| Institutional | &gt; 100 ETH   | ✅ Required    |

## ZK-KYC Process

### Step 1: Off-Chain KYC

```
User → KYC Provider (Civic/Onfido/Synaps)
     → Submit documents (passport, ID, selfie)
     → Provider verifies identity
     → Receive KYC certificate
```

### Step 2: Generate ZK Proof

```tsx
import { generateKYCProof } from "@veilfi/zk-circuits";

async function submitKYC(kycCertificate) {
  // Generate proof CLIENT-SIDE (secrets never leave browser)
  const proof = await generateKYCProof({
    userId: kycCertificate.userId, // PRIVATE
    kycHash: kycCertificate.hash, // PRIVATE
    timestamp: kycCertificate.timestamp, // PRIVATE
    providerSignature: kycCertificate.sig, // PRIVATE
  });

  // Submit only proof to blockchain
  const tx = await complianceContract.submitKYCProof(
    proof.a,
    proof.b,
    proof.c,
    proof.publicSignals // [isValid: 1 or 0]
  );

  await tx.wait();
  alert("KYC verified on-chain! Your identity remains private.");
}
```

### Step 3: On-Chain Verification

Smart contract verifies proof without seeing identity:

```solidity
function submitKYCProof(...) external {
    require(kycVerifier.verifyProof(a, b, c, publicSignals));
    require(publicSignals[0] == 1, "KYC not valid");

    kycStatus[msg.sender] = KYCStatus({
        verified: true,
        expiryTimestamp: block.timestamp + 365 days,
        proofHash: keccak256(abi.encode(a, b, c))
    });
}
```

## What's Stored On-Chain

✅ **Proof hash** (meaningless without private inputs)  
✅ **Verification status** (true/false)  
✅ **Expiry timestamp**

❌ **NOT stored**: Name, passport, address, or any PII

## Implementation

### KYC Status Check

```tsx
import { useContractRead } from "wagmi";

function KYCStatus() {
  const { address } = useAccount();

  const { data: isVerified } = useContractRead({
    address: COMPLIANCE_MANAGER_ADDRESS,
    abi: COMPLIANCE_ABI,
    functionName: "isKYCVerified",
    args: [address],
  });

  return (
    <div>
      {isVerified ? (
        <Badge color="green">✓ KYC Verified</Badge>
      ) : (
        <Button onClick={initiateKYC}>Complete KYC</Button>
      )}
    </div>
  );
}
```

### KYC Flow UI

```tsx
function KYCFlow() {
  const [step, setStep] = useState(1);

  return (
    <Stepper activeStep={step}>
      <Step>
        <StepLabel>Choose KYC Provider</StepLabel>
        <ProviderSelector onSelect={setProvider} />
      </Step>

      <Step>
        <StepLabel>Submit Documents</StepLabel>
        <DocumentUpload provider={provider} />
      </Step>

      <Step>
        <StepLabel>Generate ZK Proof</StepLabel>
        <ProofGenerator certificate={certificate} />
      </Step>

      <Step>
        <StepLabel>Submit to Blockchain</StepLabel>
        <ProofSubmitter proof={proof} />
      </Step>
    </Stepper>
  );
}
```

## Privacy Guarantees

**Blockchain sees**: "User 0xABC... is KYC-verified"  
**Blockchain CANNOT see**: Who they are, where they're from, what documents they submitted

---

**Next**: [Deposit Funds](./deposit-funds) - Start earning yield.
