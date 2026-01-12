---
title: Smart Contract Audit
sidebar_position: 3
---

# Smart Contract Audit

Veilfi contracts are designed with security best practices and planned for professional audit.

## Current Status

⚠️ **Hackathon Version**: Testnet deployment, not yet audited

**Planned**: Full audit before mainnet launch

## Audit Scope

Contracts to be audited:

- StrategyVaultV2_Multi
- ComplianceManagerV2
- All strategy contracts
- ZK verifier contracts

## Security Testing

### Automated Testing

```bash
# Run test suite
npx hardhat test

# Coverage report
npx hardhat coverage
```

### Manual Review

- Code review by team
- Security checklist verification
- Common vulnerability checks

## Pre-Mainnet Checklist

- [ ] Professional security audit
- [ ] Bug bounty program
- [ ] Gradual TVL limits
- [ ] Multi-sig governance

---

**Next**: [Best Practices](./best-practices)
