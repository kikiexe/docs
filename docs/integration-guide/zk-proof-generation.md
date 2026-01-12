---
title: ZK Proof Generation
sidebar_position: 4
---

# ZK Proof Generation

Learn how to generate Zero-Knowledge proofs for private deposits and KYC verification.

## Setup

### Install Dependencies

```bash
npm install snarkjs circomlibjs
```

### Circuit Files

Place circuit files in `public/circuits/`:

```
public/
└── circuits/
    ├── deposit.wasm           # Circuit WebAssembly
    ├── deposit_final.zkey     # Proving key
    ├── deposit_vkey.json      # Verification key
    ├── kyc.wasm
    ├── kyc_final.zkey
    └── kyc_vkey.json
```

## Private Deposit Proof

### Generate Proof

```typescript
import { groth16 } from "snarkjs";

async function generateDepositProof(amount: bigint, secret: bigint) {
  // 1. Prepare circuit inputs
  const input = {
    depositAmount: amount.toString(),
    userSecret: secret.toString(),
  };

  // 2. Generate proof (takes 5-10 seconds)
  const { proof, publicSignals } = await groth16.fullProve(
    input,
    "/circuits/deposit.wasm",
    "/circuits/deposit_final.zkey"
  );

  // 3. Format for smart contract
  const formattedProof = {
    a: [proof.pi_a[0], proof.pi_a[1]],
    b: [
      [proof.pi_b[0][1], proof.pi_b[0][0]],
      [proof.pi_b[1][1], proof.pi_b[1][0]],
    ],
    c: [proof.pi_c[0], proof.pi_c[1]],
    publicSignals: publicSignals.map((s) => BigInt(s)),
  };

  return formattedProof;
}
```

### Use in React

```tsx
import { useState } from "react";

function PrivateDepositButton() {
  const [amount, setAmount] = useState("");
  const [generating, setGenerating] = useState(false);

  async function handlePrivateDeposit() {
    setGenerating(true);

    try {
      // Generate random secret
      const secret = BigInt("0x" + randomBytes(32).toString("hex"));

      // Generate proof
      const proof = await generateDepositProof(parseEther(amount), secret);

      // Submit to contract
      const hash = await walletClient.writeContract({
        address: VAULT_ADDRESS,
        abi: VAULT_ABI,
        functionName: "depositWithProof",
        args: [proof.a, proof.b, proof.c, proof.publicSignals],
        value: parseEther(amount),
      });

      await publicClient.waitForTransactionReceipt({ hash });
      alert("Private deposit successful!");
    } catch (error) {
      console.error("Proof generation failed:", error);
      alert("Failed to generate proof");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div>
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder="Amount in ETH"
      />
      <button onClick={handlePrivateDeposit} disabled={generating || !amount}>
        {generating ? "Generating Proof..." : "Deposit Privately"}
      </button>
    </div>
  );
}
```

## Web Worker Optimization

For better UX, generate proofs in Web Worker:

### Create Worker

```typescript
// worker/zkProof.worker.ts
import { groth16 } from "snarkjs";

self.onmessage = async (e) => {
  const { type, input, wasmPath, zkeyPath } = e.data;

  try {
    const { proof, publicSignals } = await groth16.fullProve(
      input,
      wasmPath,
      zkeyPath
    );

    self.postMessage({
      type: "success",
      proof,
      publicSignals,
    });
  } catch (error) {
    self.postMessage({
      type: "error",
      error: error.message,
    });
  }
};
```

### Use Worker

```tsx
import { useEffect, useRef } from "react";

function useZKProofWorker() {
  const workerRef = useRef<Worker>();

  useEffect(() => {
    workerRef.current = new Worker(
      new URL("../worker/zkProof.worker.ts", import.meta.url)
    );

    return () => workerRef.current?.terminate();
  }, []);

  async function generateProof(input: any) {
    return new Promise((resolve, reject) => {
      workerRef.current.onmessage = (e) => {
        if (e.data.type === "success") {
          resolve(e.data);
        } else {
          reject(e.data.error);
        }
      };

      workerRef.current.postMessage({
        input,
        wasmPath: "/circuits/deposit.wasm",
        zkeyPath: "/circuits/deposit_final.zkey",
      });
    });
  }

  return { generateProof };
}
```

## KYC Proof Generation

```typescript
async function generateKYCProof(kycData: {
  userId: string;
  kycHash: string;
  timestamp: bigint;
  providerSignature: string;
}) {
  const input = {
    userId: kycData.userId,
    kycHash: kycData.kycHash,
    timestamp: kycData.timestamp.toString(),
    signature: kycData.providerSignature,
  };

  const { proof, publicSignals } = await groth16.fullProve(
    input,
    "/circuits/kyc.wasm",
    "/circuits/kyc_final.zkey"
  );

  return formatProofForContract(proof, publicSignals);
}
```

## Verify Proof Off-Chain

```typescript
import verificationKey from "/circuits/deposit_vkey.json";

async function verifyProof(proof: any, publicSignals: any[]) {
  const isValid = await groth16.verify(verificationKey, publicSignals, proof);

  return isValid;
}

// Verify before sending to blockchain
const valid = await verifyProof(proof, publicSignals);
if (!valid) {
  throw new Error("Invalid proof");
}
```

## Error Handling

```tsx
function ProofGenerator() {
  const [error, setError] = useState<string>();

  async function handleGenerate() {
    try {
      setError(undefined);

      const proof = await generateDepositProof(amount, secret);

      // Verify locally first
      const valid = await verifyProof(proof, proof.publicSignals);
      if (!valid) {
        throw new Error("Generated invalid proof");
      }

      // Submit to contract
      await submitProof(proof);
    } catch (err) {
      if (err.message.includes("Out of memory")) {
        setError("Browser ran out of memory. Try smaller circuit.");
      } else if (err.message.includes("timeout")) {
        setError("Proof generation timed out. Try again.");
      } else {
        setError("Failed to generate proof: " + err.message);
      }
    }
  }

  return (
    <div>
      {error && <Alert severity="error">{error}</Alert>}
      <button onClick={handleGenerate}>Generate Proof</button>
    </div>
  );
}
```

## Performance Tips

### Preload Circuit Files

```tsx
useEffect(() => {
  // Preload circuits on component mount
  fetch("/circuits/deposit.wasm");
  fetch("/circuits/deposit_final.zkey");
}, []);
```

### Show Progress

```tsx
function ProofGeneratorWithProgress() {
  const [progress, setProgress] = useState(0);

  async function generateWithProgress() {
    setProgress(10); // Starting

    const proof = await generateDepositProof(amount, secret);
    setProgress(50); // Proof generated

    const valid = await verifyProof(proof, proof.publicSignals);
    setProgress(70); // Verified

    await submitProof(proof);
    setProgress(100); // Complete
  }

  return (
    <div>
      {progress > 0 && <ProgressBar value={progress} />}
      <button onClick={generateWithProgress}>Generate Proof</button>
    </div>
  );
}
```

## Security Notes

⚠️ **Never expose private inputs**:

- Don't log inputs to console
- Don't send inputs to analytics
- Don't store inputs in localStorage

✅ **Best practices**:

- Generate proofs client-side only
- Use random secrets (never reuse)
- Verify proofs before submitting
- Use Web Workers for better UX

---

**Congratulations!** You've completed the **Integration Guide** section.

**Next**: Check out [Conclusion](../roadmap/current-status) for project roadmap and future plans.
