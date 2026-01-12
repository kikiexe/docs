---
title: ZK Proof Security
sidebar_position: 2
---

# ZK Proof Security

Zero-Knowledge proofs provide cryptographic security for Veilfi's privacy features.

## Cryptographic Security

### Groth16 SNARKs

**Properties**:

- Soundness: Cannot forge invalid proofs
- Zero-Knowledge: Proofs reveal nothing beyond validity
- Succinctness: Constant size (~200 bytes)

### Trusted Setup

```
Phase 1: Powers of Tau (universal)
Phase 2: Circuit-specific setup

Security: Requires 1+ honest participant (N-of-N)
```

## Attack Resistance

| Attack              | Prevention                               |
| ------------------- | ---------------------------------------- |
| **Forge proof**     | Computationally infeasible (BN254 curve) |
| **Extract secrets** | Zero-knowledge property                  |
| **Replay proof**    | Nonce tracking                           |

## Best Practices

✅ Use Web Workers for proof generation  
✅ Never share proving keys publicly  
✅ Verify proofs on-chain before accepting

---

**Next**: [Smart Contract Audit](./smart-contract-audit)
