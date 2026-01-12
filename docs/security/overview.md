---
title: Security Overview
sidebar_position: 1
---

# Security Overview

Veilfi implements multiple security layers to protect user funds and maintain system integrity.

## Security Layers

### Layer 1: Smart Contract Security

✅ **ReentrancyGuard** - All external functions protected  
✅ **Access Control** - Role-based permissions  
✅ **Input Validation** - All parameters checked  
✅ **Safe Math** - Solidity 0.8+ overflow protection

### Layer 2: ZK Proof Security

✅ **Groth16 SNARKs** - Cryptographically secure  
✅ **Trusted Setup** - Powers of Tau ceremony  
✅ **Client-Side Generation** - Secrets never leave browser

### Layer 3: Protocol Security

✅ **Diversification** - Max 50% per strategy  
✅ **Battle-Tested Protocols** - Only 2+ year old protocols  
✅ **Emergency Pause** - Can stop deposits if needed

## Security Features

### Reentrancy Protection

```solidity
function withdraw(uint256 shares) external nonReentrant {
    // Protected from reentrancy attacks
}
```

### Access Control

```solidity
modifier onlyOwner() {
    require(msg.sender == owner);
     _;
}
```

### Emergency Pause

```solidity
function pause() external onlyOwner {
    paused = true;
}
```

---

**Next**: [ZK Proof Security](./zk-proof-security)
