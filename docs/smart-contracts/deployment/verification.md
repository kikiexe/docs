---
title: Contract Verification
sidebar_position: 3
---

# Contract Verification

All Veilfi contracts are verified on Mantle Sepolia Explorer for transparency.

## Verification Process

```bash
npx hardhat verify --network mantleSepolia \
  <CONTRACT_ADDRESS> \
  <CONSTRUCTOR_ARGS>
```

## Verified Contracts

✅ All contracts verified on https://explorer.sepolia.mantle.xyz

Users can:

- Read contract source code
- Verify bytecode matches source
- Interact with verified contracts directly

---

**Next**: [Security Overview](../../security/overview)
