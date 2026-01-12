---
title: Known Risks
sidebar_position: 5
---

# Known Risks

Transparent disclosure of risks associated with using Veilfi.

## Smart Contract Risks

### Code Vulnerabilities

**Risk**: Bugs in smart contracts could lead to loss of funds

**Mitigation**:

- Extensive testing
- Professional audit (planned)
- Gradual TVL limits
- Bug bounty program

**Severity**: Medium (pre-audit), Low (post-audit)

### Strategy Protocol Risks

**Risk**: Underlying protocols (Aave/Lido/Uniswap) could be exploited

**Mitigation**:

- Only use battle-tested protocols (2+ years, $1B+ TVL)
- Diversification (max 50% per strategy)
- Emergency withdrawal mechanism

**Severity**: Low

## Economic Risks

### Impermanent Loss (Uniswap)

**Risk**: Uniswap LP positions can lose value vs. holding

**Mitigation**:

- Limited to 30% allocation
- High trading fees offset IL
- Active monitoring

**Severity**: Medium

### Market Volatility

**Risk**: Crypto market crashes affect all strategies

**Mitigation**:

- Diversification across uncorrelated strategies
- Stable yields from Aave/Lido
- No leverage used

**Severity**: Medium (inherent to crypto)

## Operational Risks

### Oracle Failures

**Risk**: Price oracles could fail or be manipulated

**Mitigation**:

- Use Chainlink (most reliable)
- Multiple oracle sources
- Sanity checks on price data

**Severity**: Low

### Liquidity Risks

**Risk**: Cannot withdraw during strategy illiquidity

**Mitigation**:

- 10% vault reserve for instant withdrawals
- Multi-strategy approach
- Staggered rebalancing

**Severity**: Low

## Privacy Risks

### Wallet Linkability

**Risk**: Wallet addresses still public (Ethereum limitation)

**Mitigation**:

- Use fresh wallet
- ZK proofs hide amounts
- Recommend privacy best practices

**Severity**: Medium (inherent to blockchain)

### Trusted Setup

**Risk**: ZK trusted setup could be compromised

**Mitigation**:

- Public Powers of Tau ceremony
- Multiple independent contributors
- Transparent process

**Severity**: Low (requires all participants dishonest)

## Regulatory Risks

### Compliance Changes

**Risk**: Regulatory requirements could change

**Mitigation**:

- Optional KYC system (adaptable)
- Tiered compliance approach
- Transparent operations

**Severity**: Medium (evolving landscape)

## User Risks

### User Error

**Risk**: Users send funds to wrong address, lose keys, etc.

**Mitigation**:

- Clear UI warnings
- Transaction confirmations
- Educational content

**Severity**: High (user responsibility)

## Risk Summary

| Risk Category          | Severity | Mitigation         |
| ---------------------- | -------- | ------------------ |
| **Smart Contracts**    | Medium   | Audit, testing     |
| **Strategy Protocols** | Low      | Battle-tested only |
| **Impermanent Loss**   | Medium   | Limited allocation |
| **Market Volatility**  | Medium   | Diversification    |
| **Privacy**            | Medium   | Best practices     |
| **Regulatory**         | Medium   | Adaptable design   |

## Risk Disclosure

⚠️ **WARNING**: Veilfi is experimental DeFi software. Do not invest more than you can afford to lose.

**No Guarantees**:

- APY not guaranteed
- Principal not FDIC-insured
- Smart contracts could have bugs
- Underlying protocols could fail

**Use at Your Own Risk**

---

**Congratulations!** You've completed the **Technical Details** section.

**Recommendation**: Review [Frontend & UX](../frontend-ux/tech-stack) for frontend implementation.
