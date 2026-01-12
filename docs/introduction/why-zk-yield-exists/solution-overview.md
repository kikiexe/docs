---
title: Solution Overview
sidebar_position: 2
---

# Solution Overview

Veilfi solves the DeFi privacy paradox through a novel architecture combining **Privacy Pools** + **Multi-Strategy Aggregation** + **ZK-Proof Compliance**. This page explains our core technical approach.

## The Veilfi Model

### Three-Layer Architecture

```
┌─────────────────────────────────────────────┐
│         Privacy Layer (ZK Circuits)          │
│  • KYC Verification (no data exposure)      │
│  • Balance Proofs (hidden amounts)          │
│  • Ownership Verification (anonymous)       │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│       Vault Layer (StrategyVaultV2)         │
│  • Shared anonymity pool                    │
│  • Proportional share minting              │
│  • Privacy-preserving withdrawals          │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│      Strategy Layer (Yield Protocols)       │
│  • Aave (Lending)                          │
│  • Lido (Staking)                          │
│  • Uniswap (Liquidity)                     │
└─────────────────────────────────────────────┘
```

## Core Innovation: Privacy-Preserving Vault

### How Traditional Vaults Expose Privacy

**Standard ERC-4626 Vault** (Yearn, Beefy):

```solidity
// ❌ All public - anyone can query
mapping(address => uint256) public balances;

function deposit(uint256 amount) public {
    balances[msg.sender] += amount; // EXPOSED!
}
```

**Result**: Every user's balance is public forever.

### Veilfi's Approach

**Privacy-First Vault**:

```solidity
// ✅ Only proof hashes stored, not amounts
mapping(address => bool) private isKYCVerified;
mapping(bytes32 => bool) private proofUsed;

function depositWithProof(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[3] memory publicSignals
) external payable {
    // Verify ZK proof instead of exposing amount
    require(zkVerifier.verifyProof(a, b, c, publicSignals));
    // Deposit processed with hidden amount
}
```

**Result**: Deposit amounts remain private; only cryptographic proofs are public.

## Mechanism Breakdown

### 1. Deposit Flow (Privacy Mode)

**Traditional DeFi**:

1. Alice deposits 100 ETH → _Public transaction_
2. Everyone sees: `Alice owns 100 ETH in Vault X`

**Veilfi**:

1. Alice deposits ETH → _Amount hidden in ZK proof_
2. Vault verifies proof → _Confirms validity without seeing amount_
3. Shares minted → _Proportional but unlinked to public address_
4. Everyone sees: `A valid deposit occurred` (amount unknown)

**Privacy Gain**: Deposit amount remains secret; only Alice knows her balance.

### 2. Anonymity Set Creation

The vault creates a **shared pool** where deposits mix:

```
Vault Total: 1,000 ETH
├─ User A: ??? ETH (only they know)
├─ User B: ??? ETH (only they know)
├─ User C: ??? ETH (only they know)
└─ ... 100+ more users
```

**Result**: Outsiders can't determine individual balances, only total TVL.

### 3. Yield Aggregation

Vault allocates mixed funds across strategies:

| Strategy  | Allocation           | Expected APY    | Monthly Yield |
| --------- | -------------------- | --------------- | ------------- |
| Aave      | 40% (400 ETH)        | 5%              | ~1.67 ETH     |
| Lido      | 30% (300 ETH)        | 4.5%            | ~1.13 ETH     |
| Uniswap   | 30% (300 ETH)        | 12%             | ~3.00 ETH     |
| **Total** | **100% (1,000 ETH)** | **~7% blended** | **~5.80 ETH** |

**Privacy Benefit**: Individual user allocations remain hidden; only aggregate is visible.

### 4. Compliant KYC (Without Data Exposure)

**Problem**: Institutions need KYC but can't expose identity on-chain.

**Veilfi's ZK-KYC**:

```circom
template KycVerification() {
    signal input userId;       // Private
    signal input kycHash;      // Private
    signal input timestamp;    // Private
    signal output isValid;     // Public (1 or 0)

    // Cryptographic verification WITHOUT revealing inputs
    isValid <== checkKYCValidity(userId, kycHash, timestamp);
}
```

**What's Stored On-Chain**:

- ✅ Proof that user is KYC'd (`isValid = 1`)
- ❌ NO name, address, passport, or PII

**Result**: Regulatory compliance without sacrificing privacy.

## Why This Works: Privacy + Utility

### Comparison with Existing Solutions

| Feature               | Tornado Cash | Aztec      | Yearn    | **Veilfi**       |
| --------------------- | ------------ | ---------- | -------- | ---------------- |
| **Privacy Mechanism** | Mixing pool  | ZK rollup  | None     | ZK proofs + pool |
| **Yield Generation**  | ❌ 0%        | ⚠️ Limited | ✅ 5-15% | ✅ 5-15%         |
| **KYC Compatible**    | ❌ No        | ⚠️ Maybe   | ✅ Yes   | ✅ ZK-KYC        |
| **Multi-Strategy**    | ❌ No        | ❌ No      | ✅ Yes   | ✅ Yes           |
| **Gas Efficiency**    | ⚠️ Medium    | ✅ High    | ✅ High  | ✅ High          |
| **Regulatory Risk**   | 🔴 High      | 🟡 Medium  | 🟢 Low   | 🟢 Low           |

**Veilfi's Advantage**: Only solution combining ALL benefits.

## Technical Guarantees

### What Veilfi Hides

✅ **Individual deposit amounts**  
✅ **User vault balances**  
✅ **Withdrawal sizes**  
✅ **Personal KYC data**  
✅ **Transaction linkage** (deposit → withdrawal)

### What Remains Transparent

🔓 **Total vault TVL** (for trust/auditing)  
🔓 **Strategy allocations** (40/30/30 split)  
🔓 **Smart contract logic** (open source)  
🔓 **Yield performance** (APY tracking)  
🔓 **Proof validity** (anyone can verify)

**Philosophy**: Maximum privacy for individuals, maximum transparency for the protocol.

## Example: Real-World Scenario

**DAOCorp Treasury Management**

**Before Veilfi** (Public Aave):

```
1. DAOCorp deposits 5M USDC to Aave
   → Transaction visible to all
   → Competitors see treasury strategy
   → MEV bots front-run large movements

2. Earns 5% APY
   → Yield public (competitors copy strategy)
   → 0 financial privacy
```

**With Veilfi** (Private Multi-Strategy):

```
1. DAOCorp deposits to Veilfi
   → Amount hidden via ZK proof
   → Only "valid deposit" is public
   → Competitors see nothing useful

2. Earns 7% blended APY
   → Vault auto-allocates to Aave/Lido/Uniswap
   → Individual allocation invisible
   → MEV bots can't target specific strategies

3. Compliance maintained
   → ZK-KYC proves DAO is verified
   → No governance token addresses exposed
```

**Result**: 40% higher yield + complete privacy + regulatory compliance.

## Security Properties

### Cryptographic Guarantees

1. **Zero-Knowledge Soundness**: Invalid proofs cannot be created (computational hardness)
2. **Completeness**: Valid operations always produce valid proofs
3. **Privacy**: Proofs reveal nothing beyond validity (zero-knowledge property)

### Economic Security

1. **Non-custodial**: Users retain full control (vault is just a coordinator)
2. **Strategy diversification**: Risk spread across protocols (no single point of failure)
3. **Transparent verification**: Anyone can audit proofs without seeing amounts

### Operational Security

1. **Admin controls**: Multi-sig for critical functions (allocate, harvest)
2. **Emergency pause**: Circuit breaker for detected exploits
3. **Gradual rollout**: TVL caps during testnet phase

## Limitations & Trade-offs

### What Veilfi Doesn't Solve

❌ **Timing analysis**: Deposit/withdrawal timing is still visible  
❌ **Network-level privacy**: IP addresses not hidden (use VPN)  
❌ **Mobile tracking**: Wallet apps may leak metadata  
❌ **Social engineering**: Privacy can't protect against phishing

### Performance Considerations

- **ZK proof generation**: ~5-10 seconds on modern hardware
- **Gas costs**: ~2x higher than non-private deposits (proof verification overhead)
- **Withdrawal delays**: May require strategy liquidation (minutes to hours)

**Trade-off Philosophy**: We accept small UX costs for significant privacy gains.

---

**Key Takeaway**: Veilfi proves that privacy and yield aren't mutually exclusive. Through Zero-Knowledge cryptography, we achieve both without compromise.

**Next**: Learn about [who benefits most from Veilfi](../who-is-this-for/privacy-conscious-users).
