---
title: Best Practices
sidebar_position: 4
---

# Best Practices

Security recommendations for users, developers, and integrators.

## For Users

### Wallet Security

✅ Use hardware wallet for large amounts  
✅ Verify contract addresses before interacting  
✅ Start with small test deposits  
✅ Enable 2FA on wallet apps

### Privacy Best Practices

✅ Use fresh wallet for maximum privacy  
✅ Use VPN/Tor when connecting  
✅ Don't share wallet address publicly  
✅ Fund via DEX for anonymity

## For Developers

### Smart Contract Development

✅ Use ReentrancyGuard on external functions  
✅ Validate all input parameters  
✅ Use SafeMath (Solidity 0.8+)  
✅ Emit events for important state changes  
✅ Write comprehensive tests

### ZK Circuit Development

✅ Minimize constraint count  
✅ Use ZK-friendly hash functions (Poseidon)  
✅ Test with edge cases  
✅ Audit circuits separately

## For Integrators

✅ Read contract documentation  
✅ Test on testnet first  
✅ Handle errors gracefully  
✅ Monitor contract events  
✅ Implement rate limiting

---

**Next**: [Known Risks](./known-risks)
