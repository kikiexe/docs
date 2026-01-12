---
title: Login & KYC
sidebar_position: 2
---

# Login & KYC Page

Wallet connection and optional KYC verification flow.

## Wallet Connection

```tsx
import { ConnectButton } from "@rainbow-me/rainbowkit";

function LoginPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl mb-8">Connect to Veilfi</h1>
      <ConnectButton />
    </div>
  );
}
```

## Optional KYC Flow

```tsx
function KYCFlow() {
  const [step, setStep] = useState(1);

  return (
    <Card>
      <Stepper activeStep={step}>
        <Step label="Choose Provider" />
        <Step label="Submit Documents" />
        <Step label="Generate ZK Proof" />
        <Step label="Submit On-Chain" />
      </Stepper>

      {step === 1 && <ProviderSelector />}
      {step === 2 && <DocumentUpload />}
      {step === 3 && <ProofGenerator />}
      {step === 4 && <ProofSubmitter />}
    </Card>
  );
}
```

**Note**: KYC optional for deposits &lt; 10 ETH

---

**Next**: [Dashboard](./dashboard)
