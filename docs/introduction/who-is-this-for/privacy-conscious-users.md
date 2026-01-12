---
title: Privacy-Conscious Users
sidebar_position: 2
---

# Privacy-Conscious Users

Veilfi is built for individuals who value financial privacy as a fundamental right, not a luxury. If you believe your wallet balance shouldn't be public knowledge, this protocol is for you.

## Key Benefits

### 1. True Financial Privacy

**What Veilfi Hides**:

- ✅ Deposit amounts (ZK proof verification)
- ✅ Vault balance (hidden in shared pool)
- ✅ Withdrawal sizes (cryptographic protection)
- ✅ Transaction history linkage (anonymity set)
- ✅ Yield earnings (proportional but private)

**What Remains Transparent** (for trust):

- 🔓 Total vault TVL (publicly verifiable)
- 🔓 Smart contract code (open source)
- 🔓 Proof verification (auditable by anyone)
- 🔓 Strategy allocations (aggregate percentages)

**Result**: Your privacy, the protocol's transparency.

### 2. Privacy Without Sacrificing Utility

Unlike privacy-only tools (Tornado Cash, mixers), Veilfi offers:

| Feature               | Privacy Mixers | **Veilfi**      |
| --------------------- | -------------- | --------------- |
| **Financial Privacy** | ✅ Strong      | ✅ Strong       |
| **Yield Generation**  | ❌ 0% APY      | ✅ 5-15% APY    |
| **Multi-Strategy**    | ❌ No          | ✅ Yes          |
| **Composability**     | ⚠️ Limited     | ✅ DeFi-native  |
| **Regulatory Risk**   | 🔴 High        | 🟢 Low (ZK-KYC) |

**Philosophy**: Privacy is a feature, not a trade-off.

### 3. No Identity Exposure (ZK-KYC)

Traditional KYC:

```
Submit passport scan → Stored by company → Risk of data breach
                                          → Identity theft risk
                                          → Centralized control
```

Veilfi's ZK-KYC:

```
Generate cryptographic proof → Only hash stored on-chain
                             → No personal data exposed
                             → You control your identity
```

**What's Stored On-Chain**:

- ✅ Proof that you're KYC-verified (`isValid = 1`)
- ❌ NO name, passport, address, or PII

**Result**: Regulatory compliance without identity exposure.

### 4. Protection from Surveillance

**Threats Veilfi Mitigates**:

| Threat                      | Without Veilfi            | With Veilfi            |
| --------------------------- | ------------------------- | ---------------------- |
| **Blockchain Analytics**    | Every transaction tracked | Deposit amounts hidden |
| **Competitor Surveillance** | Portfolio visible         | Balances private       |
| **Employer Tracking**       | Side income exposed       | Earnings confidential  |
| **Government Monitoring**   | Full transparency         | Selective disclosure   |
| **Targeted Scams**          | High-value wallets doxxed | Net worth invisible    |

**Example**: You can prove you're compliant without revealing your entire financial life.

## Use Cases

### Use Case 1: Institutional Privacy

**Profile**: A decentralized venture capital DAO managing $20M.

**Problem**:

- Portfolio companies can see DAO's entire treasury on-chain
- Competitors track investment strategies via public transactions
- Negotiating power weakened (startups know DAO's cash position)
- Board members uncomfortable with public wallet exposure

**How Veilfi Helps**:

1. Deposit $20M privately (amount hidden via ZK proof)
2. Earn 7% blended yield from Aave + Lido + Uniswap
3. Withdraw to specific investments without revealing total treasury
4. Use ZK-KYC to prove compliance to regulators if needed

**Result**: Privacy restored, negotiation leverage maintained, fiduciary duty fulfilled.

### Use Case 2: Personal Financial Security

**Profile**: Maria, a developer with $100k in crypto.

**Problem**:

- Ex-partner knows her wallet address (from old joint transactions)
- Uncomfortable with ex seeing her current net worth
- Worried about potential legal claims: "She has more money than she says"
- Can't change wallet address (NFTs, ENS tied to it)

**How Veilfi Helps**:

1. Transfer funds to Veilfi privately
2. Balance hidden from ex-partner's view
3. Earns yield safely (7% APY)
4. Can prove solvency to court via ZK proof if needed (without full exposure)

**Result**: Financial independence restored, legal protection maintained.

### Use Case 3: Activist Protection

**Profile**: Alex, an activist in a country with capital controls.

**Problem**:

- Government monitors blockchain for "illegal" foreign transactions
- Traditional banking freezes activist accounts
- DeFi offers escape but transparent addresses are risky
- Needs plausible deniability for savings

**How Veilfi Helps**:

1. Deposit savings privately to Veilfi
2. Earn yield to combat inflation
3. Government sees "a deposit occurred" but not amount
4. Can withdraw anonymously when needed

**Disclaimer**: Veilfi doesn't encourage illegal activity. This scenario assumes Alex's use is legitimate under international law.

**Result**: Financial freedom, reduced surveillance risk.

## How It Works (Privacy-Focused Flow)

### Step 1: Maximum Privacy Setup

**Network-Level Privacy**:

```
Use Tor Browser → Hide IP address
    OR
Use VPN → Mask location from RPC providers
```

**Wallet Privacy**:

```
Create fresh MetaMask wallet → Not linked to identity
    Optional: Use Burner wallet
```

### Step 2: Private Deposit

**Generate ZK Proof** (off-chain):

```javascript
// Your browser generates proof locally
const proof = await generateDepositProof({
  amount: ethers.utils.parseEther("10"), // Private input
  userSecret: wallet.privateKey, // Private input
});

// Only proof hash goes on-chain (amount hidden)
```

**Submit Transaction**:

```
Send depositWithProof() transaction
↓
Blockchain sees: "Valid proof submitted"
Blockchain CANNOT see: Actual deposit amount
↓
You receive proportional vault shares
```

### Step 3: Earning Yield Privately

```
Your funds mixed in shared vault:
├─ Total Pool: 1,000 ETH (public)
├─ Your Amount: 10 ETH (PRIVATE - only you know)
├─ Other Users: 990 ETH (distributed among many)
↓
Vault allocates to strategies (aggregate is public):
├─ 400 ETH → Aave
├─ 300 ETH → Lido
└─ 300 ETH → Uniswap
↓
You earn proportional yield
(7% APY on your hidden 10 ETH = 0.7 ETH/year)
```

**Privacy Guarantee**: Outsiders see total TVL, not your individual balance.

### Step 4: Anonymous Withdrawal

**Generate Withdrawal Proof**:

```circom
// Prove you own X shares without revealing X
circuit OwnershipProof {
    signal private input shares;      // Hidden
    signal private input userSecret;  // Hidden
    signal public output isValid;     // Public (1 or 0)

    // Cryptographic verification
}
```

**Withdraw**:

```
Submit withdrawal proof
↓
Vault verifies: "Yes, this user owns shares"
Vault CANNOT determine: Exact share amount
↓
You receive ETH/USDC
↓
On-chain observers see: "A withdrawal occurred"
On-chain observers CANNOT see: Withdrawal size
```

## Requirements

### For Maximum Privacy

✅ **Fresh Wallet**: New address not linked to identity  
✅ **VPN/Tor**: Hide IP from RPC providers  
✅ **Non-KYC Exchange**: Acquire initial crypto privately (or use DEX)  
✅ **Patience**: ZK proof generation takes ~10 seconds

### For Compliance + Privacy

✅ **ZK-KYC Proof**: One-time generation (proves identity without exposing it)  
✅ **Record Keeping**: Save proof parameters (for tax purposes)  
✅ **Legal Advice**: Consult lawyer in your jurisdiction

## Privacy Guarantees & Limitations

### What Veilfi Guarantees

✅ **Deposit Amount Privacy**: Hidden via zero-knowledge proofs  
✅ **Balance Privacy**: Not queryable by outsiders  
✅ **Withdrawal Privacy**: Amounts cryptographically protected  
✅ **No Data Sales**: We don't collect or sell user data  
✅ **Open Source**: All code is auditable

### What Veilfi Cannot Hide

❌ **Wallet Address**: Public on blockchain (use fresh address)  
❌ **Transaction Timing**: Timestamp is visible (timing analysis possible)  
❌ **IP Address**: Use VPN/Tor for network privacy  
❌ **Network Fees**: Gas costs are public (unavoidable on blockchain)

### Trust Assumptions

**You Must Trust**:

1. **Cryptography**: ZK-SNARKs are secure (widely accepted assumption)
2. **Smart Contracts**: Code is bug-free (open source + auditable)
3. **Mantle Network**: Blockchain itself isn't compromised

**You DON'T Need to Trust**:

1. ❌ Veilfi team (non-custodial)
2. ❌ Third-party data providers (self-verifiable)
3. ❌ Centralized KYC services (ZK proofs instead)

## Comparison with Privacy Alternatives

| Solution          | Privacy Level | Yield      | Compliance    | Status    |
| ----------------- | ------------- | ---------- | ------------- | --------- |
| **Tornado Cash**  | 🟢 High       | ❌ 0%      | 🔴 Sanctioned | Risky     |
| **Aztec Network** | 🟢 High       | 🟡 Limited | 🟡 Unclear    | Early     |
| **Railgun**       | 🟢 High       | 🟡 Partial | 🟡 Partial    | Growing   |
| **Monero**        | 🟢 Highest    | ❌ 0%      | 🔴 Banned     | Off-chain |
| **🎯 Veilfi**     | 🟢 High       | ✅ 5-15%   | ✅ ZK-KYC     | Balanced  |

**Veilfi's Niche**: Privacy + Yield + Compliance = Unique position.

## Frequently Asked Questions

**Q: Is Veilfi legal?**  
A: Yes. Privacy ≠ illegality. Veilfi includes ZK-KYC for regulatory compliance.

**Q: Can governments seize my funds?**  
A: Veilfi is non-custodial. We cannot freeze or seize funds. Your keys = your control.

**Q: What if Veilfi gets shut down?**  
A: Smart contracts are permissionless. Even if our website disappears, you can interact directly with contracts.

**Q: How private is "private"?**  
A: Deposit amounts and balances are cryptographically hidden. However, wallet addresses and transaction timing are still visible.

**Q: Why not just use Monero?**  
A: Monero offers strong privacy but:

- ❌ No yield generation
- ❌ Limited DeFi ecosystem
- ❌ Exchange delistings (regulatory pressure)

Veilfi provides privacy WITHIN the DeFi yield ecosystem.

---

**Ready to experience private DeFi?** Start with the [Privacy Flow Guide](../../core-flow/privacy-flow/private-deposits).

**Want technical details?** Read about [ZK Circuit Design](../../zk-circuits/circuit-design/balance-proof).
