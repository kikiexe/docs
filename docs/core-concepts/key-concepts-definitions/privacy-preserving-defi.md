---
title: Privacy-Preserving DeFi
sidebar_position: 3
---

# Privacy-Preserving DeFi

Privacy-Preserving DeFi refers to decentralized finance protocols that enable users to transact, earn yield, and interact with smart contracts **without exposing sensitive financial information** to the public blockchain.

## The DeFi Privacy Problem

### Radical Transparency = Privacy Nightmare

Traditional DeFi is **completely transparent** by default:

```
Every transaction reveals:
✅ Sender address
✅ Receiver address
✅ Amount transacted
✅ Token type
✅ Smart contract interaction
✅ Timestamp
✅ Historical activity

Result: Your entire financial life is public forever
```

**Example**:

> _You deposit 50 ETH to Aave. Now everyone knows:_
>
> - _You have at least 50 ETH_
> - _You're risk-averse (chose lending over trading)_
> - _Your wallet address (can track all future activity)_

## Privacy-Preserving Solutions

### Approach 1: Mixers (Tornado Cash Model)

**How it works**:

```
10 users deposit 1 ETH each
        ↓
    [BLACK BOX]
      (mixing)
        ↓
10 users withdraw 1 ETH each
```

**Privacy Achieved**:

- Input/output linkage broken
- Deposit address ≠ withdrawal address

**Limitations**:

- ❌ Fixed denominations only (1 ETH, 10 ETH, etc.)
- ❌ Zero yield generation
- ❌ Regulatory scrutiny (OFAC sanctions)
- ❌ Not composable with DeFi

### Approach 2: Privacy Chains (Monero, Zcash)

**How it works**:

- Separate blockchain with privacy by default
- All transactions confidential

**Privacy Achieved**:

- Full transaction privacy
- Hidden amounts, addresses

**Limitations**:

- ❌ Isolated ecosystems (limited DeFi)
- ❌ No yield opportunities
- ❌ Not integrated with Ethereum/Mantle

### Approach 3: ZK Rollups (Aztec, StarkNet)

**How it works**:

- Layer 2 blockchain with privacy features
- Transactions batched and proven with ZK proofs

**Privacy Achieved**:

- Private transactions on L2
- Growing DeFi ecosystem

**Limitations**:

- ⚠️ Limited protocol integrations
- ⚠️ Complex user experience
- ⚠️ Early stage (not battle-tested)

### Approach 4: Privacy-First Applications (Veilfi)

**How it works**:

- Application-layer privacy on existing chains
- ZK proofs for specific interactions
- Composable with standard DeFi

**Privacy Achieved**:

- Private deposits/withdrawals
- Hidden balances
- Regulatory compliance option (ZK-KYC)

**Advantages**:

- ✅ Earns yield (5-15% APY)
- ✅ Multi-protocol aggregation
- ✅ Native to Mantle (no bridge needed)
- ✅ Simpler UX than full privacy chains

## Veil fi's Privacy Model

### What Veilfi Hides

| Data Type            | Visibility | Privacy Mechanism              |
| -------------------- | ---------- | ------------------------------ |
| **Deposit Amounts**  | 🔒 Private | ZK proof of valid deposit      |
| **User Balances**    | 🔒 Private | Shares minted, amounts hidden  |
| **Withdrawal Sizes** | 🔒 Private | Cryptographic proofs           |
| **KYC Identity**     | 🔒 Private | ZK-KYC (only hash stored)      |
| **Yield Earnings**   | 🔒 Private | Proportional to hidden balance |

### What Remains Transparent

| Data Type                | Visibility | Reason                |
| ------------------------ | ---------- | --------------------- |
| **Total Vault TVL**      | 🔓 Public  | Trust & audibility    |
| **Strategy Allocations** | 🔓 Public  | Protocol transparency |
| **Smart Contracts**      | 🔓 Public  | Open source security  |
| **Proof Validity**       | 🔓 Public  | Anyone can verify     |

**Philosophy**: Maximize user privacy, maximize protocol transparency.

## Privacy Techniques Used

### 1. Anonymity Sets

**Concept**: Hide individual users among a group.

```
Shared Vault Pool:
├─ User A: ??? ETH
├─ User B: ??? ETH
├─ User C: ??? ETH
├─ User D: ??? ETH
└─ ... 100+ more users

Outsiders see: "Vault has 1,000 ETH total"
Outsiders CANNOT see: Individual balances
```

**Privacy Gain**: Larger anonymity set = stronger privacy.

### 2. Commitment Schemes

**Concept**: Prove you made a deposit without revealing details.

```javascript
// User generates commitment
commitment = hash(depositAmount + userSecret);

// Commitment stored on-chain (reveals nothing)
// Later, user can "open" commitment to withdraw
```

**Example**:

```
Alice deposits 10 ETH
Commitment: 0x7a3f2b1c...
↓
Blockchain stores: 0x7a3f2b1c... (meaningless to outsiders)
Blockchain CANNOT deduce: 10 ETH amount
```

### 3. Zero-Knowledge Proofs (Core Privacy Layer)

**Concept**: Prove facts without revealing underlying data.

**Veilfi's ZK Circuits**:

```circom
// Prove deposit without revealing amount
template PrivateDeposit() {
    signal private input amount;      // HIDDEN
    signal private input userSecret;  // HIDDEN
    signal public output commitment;  // PUBLIC

    commitment <== hash(amount, userSecret);
}
```

**Result**: Blockchain verifies proof is valid, learns nothing about `amount`.

### 4. Selective Disclosure

**Concept**: Users choose what to reveal (and to whom).

**Example Scenario**:

```
Alice's vault balance: 100 ETH (PRIVATE by default)

Tax auditor requests proof:
├─ Alice generates ZK proof: "I have ≥ 80 ETH"
├─ Auditor verifies proof
├─ Auditor learns: Alice has at least $80k equivalent
└─ Auditor CANNOT see: Exact 100 ETH balance

Selective disclosure: Compliance without full exposure
```

## Privacy vs. Compliance

### The Spectrum

```
Full Privacy ←──────────────────────→ Full Transparency
(Monero)          (Veilfi)          (Standard DeFi)
     │                │                    │
     └─ No KYC       └─ ZK-KYC           └─ Public KYC
     └─ High risk    └─ Compliant       └─ No privacy
```

**Veilfi's Position**: Privacy + Compliance via ZK-KYC

### ZK-KYC: Best of Both Worlds

**Traditional KYC** (Coinbase, Binance):

```
Submit passport → Company stores it → Data breach risk
                                     → Privacy lost forever
```

**Veilfi's ZK-KYC**:

```
Generate cryptographic proof → Only hash stored on-chain
                             → No PII exposure
                             → Privacy preserved
```

**What Regulators See**:

- ✅ User is verified by trusted KYC provider
- ✅ Compliance requirement satisfied

**What Regulators CANNOT See**:

- ❌ User's name, address, passport details
- ❌ Exact balance or transaction history

**Result**: Regulatory compliance without sacrificing privacy.

## Use Cases

### Institutional Treasury Privacy

**Problem**:

```
DAO has $10M USDC earning yield on Aave
↓
Every competitor sees:
- Treasury size ($10M)
- Investment strategy (Aave)
- Rebalancing timing
↓
Competitors front-run large movements
```

**Veilfi Solution**:

```
DAO deposits $10M privately to Veilfi
↓
Outsiders see:
- "A deposit occurred" (amount hidden)
- Total vault TVL increased (not specific to DAO)
↓
Competitors cannot track DAO's specific moves
```

### Personal Financial Security

**Problem**:

```
You have $500k in crypto
↓
Share wallet address on Twitter for NFT drop
↓
Now everyone knows your net worth
↓
Targeted scams, phishing, $5 wrench attacks
```

**Veilfi Solution**:

```
Move funds to Veilfi privately
↓
Public sees: "Wallet balance now low"
Scammers think: "Not worth targeting"
Reality: Your $500k earning yield in Veilfi (hidden)
```

### Activist Protection

**Problem**:

```
Activist receives donations for movement
↓
Government tracks all donations on-chain
↓
Donor addresses identified → intimidation
```

**Veilfi Solution**:

```
Donations routed through Veilfi
↓
Amounts hidden via ZK proofs
↓
Government sees: "Transactions occurred" (not amounts)
↓
Donors protected from retaliation
```

## Privacy Guarantees & Limitations

### What Veilfi Guarantees

✅ **Deposit Privacy**: Amounts cryptographically hidden  
✅ **Balance Privacy**: Not queryable by outsiders  
✅ **Withdrawal Privacy**: Sizes remain confidential  
✅ **Identity Privacy**: ZK-KYC without PII exposure  
✅ **Open Verification**: Anyone can verify proofs (trustless)

### What Veilfi Cannot Hide

❌ **Wallet Addresses**: Public on blockchain (mitigation: use fresh wallet)  
❌ **Transaction Timing**: Timestamps visible (mitigation: delay transactions)  
❌ **Network Metadata**: IP addresses (mitigation: use VPN/Tor)  
❌ **Transaction Existence**: Events are public, just amounts hidden

### Privacy Best Practices

**For Maximum Privacy**:

1. **Use Fresh Wallet**:

   ```
   ❌ Don't: Use wallet linked to your identity
   ✅ Do: Create new MetaMask for Veilfi only
   ```

2. **Enable ZK Proofs**:

   ```
   ❌ Don't: Use standard public deposits
   ✅ Do: Always deposit with ZK proofs
   ```

3. **Network Privacy**:

   ```
   ❌ Don't: Connect from home IP
   ✅ Do: Use VPN or Tor Browser
   ```

4. **Timing Obfuscation**:
   ```
   ❌ Don't: Withdraw immediately after deposit
   ✅ Do: Wait days/weeks to break timing correlation
   ```

## Comparison with Alternatives

| Solution          | Privacy Level | Yield      | Compliance   | UX Complexity |
| ----------------- | ------------- | ---------- | ------------ | ------------- |
| **Tornado Cash**  | 🟢 95%        | ❌ 0%      | 🔴 Banned    | 🟡 Medium     |
| **Aztec Network** | 🟢 90%        | 🟡 Limited | 🟡 Unclear   | 🔴 High       |
| **Monero**        | 🟢 99%        | ❌ 0%      | 🔴 High Risk | 🟢 Low        |
| **Standard DeFi** | 🔴 0%         | ✅ High    | ✅ Yes       | 🟢 Low        |
| **🎯 Veilfi**     | 🟢 85%        | ✅ 7% APY  | ✅ ZK-KYC    | 🟢 Low        |

**Veilfi's Niche**: Privacy + Yield + Compliance in one solution.

---

**Next**: Learn about [KYC Compliance](./kyc-compliance) and how Veilfi achieves it privately.

**Technical Details**: Explore [ZK Circuits](../../zk-circuits/introduction) for implementation.
