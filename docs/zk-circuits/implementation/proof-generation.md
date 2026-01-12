---
title: Proof Generation
sidebar_position: 2
---

# Proof Generation

Client-side proof generation enables users to create Zero-Knowledge proofs in their browser without revealing secrets to any server.

## Browser-Based Generation

### Why Client-Side?

**Privacy**: Secrets never leave user's device  
**Security**: No server to compromise  
**Decentralization**: No dependency on centralized infrastructure

## Implementation

### 1. Load Circuit Artifacts

```javascript
import { groth16 } from "snarkjs";

// Load WASM and proving key
async function loadCircuit() {
  const wasmBuffer = await fetch("/circuits/kyc_verification.wasm").then((r) =>
    r.arrayBuffer()
  );

  const zkeyBuffer = await fetch("/circuits/kyc_verification_final.zkey").then(
    (r) => r.arrayBuffer()
  );

  return { wasmBuffer, zkeyBuffer };
}
```

### 2. Prepare Inputs

```javascript
async function prepareKYCInputs(userData) {
  return {
    userId: userData.id.toString(),
    kycHash: ethers.utils.keccak256(userData.kycCertificate),
    timestamp: Math.floor(Date.now() / 1000).toString(),
    providerSignature: userData.signature.toString(),
  };
}
```

### 3. Generate Proof

```javascript
async function generateKYCProof(inputs) {
  try {
    // Show loading state
    setLoadingMessage("Generating proof (5-10 seconds)...");

    // Generate proof
    const { proof, publicSignals } = await groth16.fullProve(
      inputs,
      "/circuits/kyc_verification.wasm",
      "/circuits/kyc_verification_final.zkey"
    );

    console.log("Proof generated successfully!");
    console.log("Public outputs:", publicSignals);

    return { proof, publicSignals };
  } catch (error) {
    console.error("Proof generation failed:", error);
    throw new Error("Failed to generate ZK proof");
  }
}
```

### 4. Format for Solidity

```javascript
function formatProofForSolidity(proof, publicSignals) {
  // Convert to Solidity-compatible format
  const calldata = {
    a: [proof.pi_a[0], proof.pi_a[1]],
    b: [
      [proof.pi_b[0][1], proof.pi_b[0][0]],
      [proof.pi_b[1][1], proof.pi_b[1][0]],
    ],
    c: [proof.pi_c[0], proof.pi_c[1]],
    input: publicSignals.map((s) => s.toString()),
  };

  return calldata;
}
```

## Complete Example: React Component

```tsx
import { useState } from "react";
import { groth16 } from "snarkjs";
import { ethers } from "ethers";

export function KYCProofGenerator() {
  const [loading, setLoading] = useState(false);
  const [proofData, setProofData] = useState(null);

  async function handleGenerateProof() {
    setLoading(true);

    try {
      // 1. Get KYC data from user
      const kycData = await getUserKYCData();

      // 2. Prepare circuit inputs
      const inputs = {
        userId: kycData.userId,
        kycHash: kycData.hash,
        timestamp: Math.floor(Date.now() / 1000),
        providerSignature: kycData.signature,
      };

      // 3. Generate proof
      const { proof, publicSignals } = await groth16.fullProve(
        inputs,
        "/circuits/kyc_verification.wasm",
        "/circuits/kyc_verification_final.zkey"
      );

      // 4. Format for Solidity
      const formattedProof = formatProofForSolidity(proof, publicSignals);
      setProofData(formattedProof);

      // 5. Submit to blockchain
      await submitProof(formattedProof);
    } catch (error) {
      alert("Proof generation failed: " + error.message);
    } finally {
      setLoading(false);
    }
  }

  async function submitProof(proofData) {
    const contract = new ethers.Contract(
      COMPLIANCE_MANAGER_ADDRESS,
      COMPLIANCE_ABI,
      signer
    );

    const tx = await contract.submitKYCProof(
      proofData.a,
      proofData.b,
      proofData.c,
      proofData.input
    );

    await tx.wait();
    alert("KYC verified on-chain!");
  }

  return (
    <div>
      <button onClick={handleGenerateProof} disabled={loading}>
        {loading ? "Generating Proof..." : "Verify KYC"}
      </button>

      {proofData && <div>✅ Proof generated and submitted!</div>}
    </div>
  );
}
```

## Web Workers for Non-Blocking UI

### Why Web Workers?

Proof generation takes 5-15 seconds and blocks the main thread. Web Workers solve this:

```javascript
// worker.js
import { groth16 } from "snarkjs";

self.addEventListener("message", async (event) => {
  const { inputs, wasmPath, zkeyPath } = event.data;

  try {
    // Generate proof in background thread
    const { proof, publicSignals } = await groth16.fullProve(
      inputs,
      wasmPath,
      zkeyPath
    );

    // Send result back to main thread
    self.postMessage({
      success: true,
      proof,
      publicSignals,
    });
  } catch (error) {
    self.postMessage({
      success: false,
      error: error.message,
    });
  }
});
```

### Using Web Worker

```javascript
// main.js
const worker = new Worker("worker.js");

async function generateProofWithWorker(inputs) {
  return new Promise((resolve, reject) => {
    // Send task to worker
    worker.postMessage({
      inputs,
      wasmPath: "/circuits/kyc_verification.wasm",
      zkeyPath: "/circuits/kyc_verification_final.zkey",
    });

    // Wait for result
    worker.onmessage = (event) => {
      if (event.data.success) {
        resolve({
          proof: event.data.proof,
          publicSignals: event.data.publicSignals,
        });
      } else {
        reject(new Error(event.data.error));
      }
    };
  });
}

// Usage (non-blocking!)
const { proof, publicSignals } = await generateProofWithWorker(inputs);
```

## Optimization Strategies

### 1. Lazy Loading

```javascript
// Only load heavy files when needed
async function loadCircuitLazy() {
  const [wasm, zkey] = await Promise.all([
    import("/circuits/kyc_verification.wasm"),
    import("/circuits/kyc_verification_final.zkey"),
  ]);

  return { wasm, zkey };
}
```

### 2. Caching

```javascript
// Cache loaded circuits
const circuitCache = new Map();

async function getCircuit(name) {
  if (circuitCache.has(name)) {
    return circuitCache.get(name);
  }

  const circuit = await loadCircuit(name);
  circuitCache.set(name, circuit);
  return circuit;
}
```

### 3. Progress Indicators

```javascript
async function generateProofWithProgress(inputs, onProgress) {
  onProgress(0, "Loading circuit...");
  const circuit = await loadCircuit();

  onProgress(20, "Calculating witness...");
  const witness = await calculateWitness(inputs);

  onProgress(60, "Generating proof...");
  const proof = await groth16.prove(witness, circuit.zkey);

  onProgress(100, "Done!");
  return proof;
}
```

## Error Handling

```javascript
async function generateProofSafely(inputs) {
  try {
    return await groth16.fullProve(inputs, wasm, zkey);
  } catch (error) {
    if (error.message.includes("witness")) {
      throw new Error("Invalid inputs provided");
    } else if (error.message.includes("memory")) {
      throw new Error("Circuit too large for device");
    } else if (error.message.includes("network")) {
      throw new Error("Failed to load circuit files");
    } else {
      throw new Error("Proof generation failed: " + error.message);
    }
  }
}
```

## Performance Metrics

| Circuit              | Constraints | Desktop (i7) | Mobile (A15) | Memory |
| -------------------- | ----------- | ------------ | ------------ | ------ |
| **KYC Verification** | ~1,200      | 3-5s         | 8-12s        | ~200MB |
| **Balance Proof**    | ~500        | 2-3s         | 5-8s         | ~100MB |
| **Complex Circuit**  | ~10,000     | 15-30s       | 40-60s       | ~1GB   |

**Recommendation**: Optimize circuits to stay under 5,000 constraints for mobile compatibility.

---

**Next**: [Proof Verification](./proof-verification) - Verify proofs on-chain.
