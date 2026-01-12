---
title: ZK Verifier
sidebar_position: 3
---

# ZK Verifier

The **Groth16Verifier** contract validates Zero-Knowledge proofs on-chain, enabling privacy-preserving operations.

## Contract Overview

Auto-generated from Circom circuits:

```solidity
contract Groth16Verifier {
    using Pairing for *;

    struct VerifyingKey {
        Pairing.G1Point alpha;
        Pairing.G2Point beta;
        Pairing.G2Point gamma;
        Pairing.G2Point delta;
        Pairing.G1Point[] gamma_abc;
    }

    function verifyProof(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[N] memory input  // Public signals
    ) public view returns (bool);
}
```

## Verification Process

### Elliptic Curve Pairing

Verifies proof using BN254 curve:

```solidity
function pairing(
    G1Point[] memory p1,
    G2Point[] memory p2
) internal view returns (bool) {
    // Calls precompiled contract at address 0x08
    // Performs optimal Ate pairing check
    assembly {
        success := staticcall(
            gas(),
            8,  // Pairing precompile
            add(p1, 0x20),
            mul(length, 0xc0),
            out,
            0x20
        )
    }

    return success && (result != 0);
}
```

**Gas Cost**: ~280k-320k per verification

## Integration Example

```solidity
contract MyContract {
    Groth16Verifier public verifier;

    function submitWithProof(
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[3] memory signals
    ) external {
        require(verifier.verifyProof(a, b, c, signals), "Invalid proof");

        // Proof valid - execute action
        _processAction(msg.sender);
    }
}
```

## Security

**Cryptographic Guarantees**:

- Soundness: Invalid proofs cannot pass verification
- Zero-Knowledge: Proofs reveal nothing beyond validity
- Non-interactive: No back-and-forth required

---

**Next**: [Yield Distributor](./yield-distributor)
