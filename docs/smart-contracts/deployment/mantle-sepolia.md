---
title: Mantle Sepolia Deployment
sidebar_position: 1
---

# Mantle Sepolia Deployment

Veilfi is deployed on Mantle Sepolia Testnet for hackathon demonstration.

## Network Details

```
Network: Mantle Sepolia Testnet
Chain ID: 5003
RPC URL: https://rpc.sepolia.mantle.xyz
Explorer: https://explorer.sepolia.mantle.xyz
Currency: MNT (test tokens)
```

## Deployment Steps

```bash
# 1. Compile contracts
npx hardhat compile

# 2. Deploy to Mantle Sepolia
npx hardhat run scripts/deploy.js --network mantleSepolia

# 3. Verify contracts
npx hardhat verify --network mantleSepolia <CONTRACT_ADDRESS>
```

## Getting Test MNT

Visit Mantle Sepolia Faucet to get test tokens.

---

**Next**: [Contract Addresses](./contract-addresses)
