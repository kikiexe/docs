---
title: Design Philosophy
sidebar_position: 1
---

# Design Philosophy

The core principles and values that guided Veilfi's design and development.

## Core Principles

### 1. Privacy as a Default, Not an Afterthought

```
Traditional DeFi:
Design protocol → Add privacy as feature (maybe)

Veilfi:
Start with privacy → Build everything around it
```

**Why it matters**: Privacy should be fundamental, not optional. Users shouldn't have to trade financial transparency for DeFi access.

**Implementation**:

- ZK proofs integrated at the protocol layer
- Private by default, transparent when needed
- No PII stored on-chain, ever

### 2. Simplicity for Users, Complexity Under the Hood

```
User Experience:
"Deposit ETH → Earn 7% APY"

Behind the Scenes:
- Multi-strategy allocation
- ZK proof generation
- Automated harvesting
- Rebalancing algorithms
```

**Why it matters**: DeFi is too complex. Users want yields, not PhD-level math.

**Implementation**:

- One-click deposits
- Automated everything
- Clear, honest APY display
- No hidden mechanics

### 3. Trust Through Transparency

```
"Don't trust, verify"

Vault-level: 100% transparent
├─ Total TVL: Public
├─ Strategy allocations: Public
├─ APY calculations: Public
└─ Smart contract code: Open source

User-level: Privacy preserved
├─ Individual amounts: Private (ZK)
├─ Balances: Private (shares)
└─ Identity: Private (ZK-KYC)
```

**Why it matters**: Users need to verify the system works without exposing their financial data.

**Implementation**:

- All contracts verified on Explorer
- Public APY and TVL metrics
- Open source codebase
- Auditable ZK circuits

### 4. Sustainable Over Spectacular

```
❌ Risky: "300% APY on new token!"
✅ Sustainable: "7% APY on diversified strategies"

Veilfi chooses:
- Proven protocols over new experiments
- Gradual growth over explosive hype
- Long-term viability over short-term gains
```

**Why it matters**: DeFi needs sustainable yields, not Ponzi schemes.

**Implementation**:

- Only battle-tested protocols (2+ years)
- Diversification limits risk
- No native token farming
- Transparent fee structure

### 5. Compliance Without Compromise

```
Traditional path:
Full KYC → Privacy loss → Regulatory compliance

Veilfi path:
ZK-KYC → Privacy maintained → Regulatory compliance
```

**Why it matters**: DeFi will face regulation. We can comply without sacrificing user privacy.

**Implementation**:

- Tiered KYC (optional for small amounts)
- ZK proofs hide identity details
- Verifiable compliance status
- No personal data on-chain

## Design Decisions

### Why Zero-Knowledge Proofs?

**Problem**: How to prove something without revealing it?

```
Traditional: "I deposited 100 ETH" (amount exposed)
ZK Proof: "I made a valid deposit" (amount hidden)
```

**Decision**: Use Groth16 SNARKs for succinct, fast verification

**Trade-offs**:

- ✅ Strong privacy guarantees
- ✅ Small proof size (~200 bytes)
- ✅ Fast verification (~5ms on-chain)
- ⚠️ Requires trusted setup
- ⚠️ Proof generation takes 5-10s

### Why ERC-4626?

**Problem**: How to represent vault shares?

**Decision**: Use ERC-4626 tokenized vault standard

**Why**:

- ✅ Composable with other DeFi
- ✅ Standard interface (familiar to devs)
- ✅ Share price automatically reflects yields
- ✅ Compatible with wallets, explorers, aggregators

### Why Mantle Sepolia?

**Problem**: Which network to deploy on?

**Decision**: Mantle Sepolia Testnet (for hackathon)

**Why**:

- ✅ EVM-compatible (easy migration)
- ✅ Low gas fees
- ✅ Testnet for safe experimentation
- ✅ Mantle ecosystem growth potential

**Future**: Deploy to Mantle Mainnet, then expand to other L2s

### Why No Governance Token?

**Problem**: How to govern the protocol?

**Decision**: No native token (for now)

**Why**:

- ❌ Avoid token farming dumping
- ❌ Avoid regulatory token security issues
- ❌ Avoid liquidity mining unsustainability
- ✅ Focus on product-market fit first

**Future**: Community governance if protocol proves successful

## What We Don't Do

### We Don't Promise the Moon

```
❌ "Guaranteed 100% APY!"
✅ "Historical 7% APY, no guarantees"

❌ "Zero risk!"
✅ "Low risk, but still DeFi risks exist"
```

**Why**: Honesty builds trust. DeFi has enough snake oil.

### We Don't Custody Funds

```
Your ETH → Smart Contract (not Veilfi team)
Your keys → Your control

Veilfi team: Cannot access user funds
Users: Can withdraw anytime
```

**Why**: Non-custodial is fundamental to DeFi.

### We Don't Sell Your Data

```
What we collect: Nothing (wallet interactions are public blockchain data)
What we store: Nothing (no servers, no databases)
What we sell: Nothing (no data = nothing to sell)
```

**Why**: Privacy-first means no data harvesting.

## Lessons from DeFi History

### Learn from Failures

**2022 UST/Luna collapse**: Don't use algorithmic stablecoins  
**2023 FTX**: Non-custodial is non-negotiable  
**Multiple hacks**: Only use audited, battle-tested protocols

**Veilfi response**:

- No stablecoins (yet)
- Non-custodial always
- Only 2+ year old protocols

### Learn from Successes

**Uniswap**: Simple, elegant interface  
**Aave**: Modular, upgradeable architecture  
**Tornado Cash**: ZK privacy works (before sanctions)

**Veilfi borrows**:

- Simple UX (Uniswap style)
- Modular strategies (Aave style)
- ZK privacy (Tornado style, but compliant)

## The Veilfi Way

### Before Every Decision, Ask:

1. **Does this preserve user privacy?**
2. **Is this sustainable long-term?**
3. **Would I use this with my own money?**
4. **Can we verify this on-chain?**
5. **Does this add unnecessary complexity?**

If the answer to any is "no," we rethink.

### Our Commitment

```
We promise to:
✅ Be transparent about how the protocol works
✅ Protect user privacy as a core feature
✅ Only deploy to battle-tested protocols
✅ Charge fair, transparent fees
✅ Build sustainable, not spectacular

We will never:
❌ Lie about APYs or risks
❌ Custody user funds
❌ Sell user data
❌ Sacrifice security for speed
❌ Compromise on privacy
```

---

**Next**: [Long-term Vision](./long-term-vision) - Where we're headed
