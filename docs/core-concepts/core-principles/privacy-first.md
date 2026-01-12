---
title: Privacy First
sidebar_position: 1
---

# Privacy First

**Privacy First** is Veilfi's foundational design principle: every feature, every decision, and every technical choice prioritizes user financial privacy without compromise.

## Core Philosophy

> "Financial privacy should be the default, not an opt-in feature."

Traditional DeFi forces users to choose between **earning yield** OR **maintaining privacy**. Veilfi rejects this false dichotomy by making privacy **the default state**.

## Privacy-First Design Decisions

### 1. ZK Proofs by Default

**Standard Approach** (most DeFi):

```solidity
// Public deposit - amount ALWAYS visible
function deposit(uint256 amount) public {
    balances[msg.sender] += amount;  // ← EXPOSED!
}
```

**Veilfi's Approach**:

```solidity
// Privacy-first deposit - amount HIDDEN by default
function depositWithProof(...) external payable {
    // Verify ZK proof (amount never exposed on-chain)
    require(zkVerifier.verifyProof(...));
    _mint(msg.sender, shares);  // Shares minted, amounts private
}
```

**Impact**: Privacy is built-in, not bolted-on.

### 2. Shared Anonymity Pools

Instead of individual accounts, Veilfi uses **shared vault pools**:

```
❌ Traditional Model:
User A → Personal Vault A (isolated, balance visible)
User B → Personal Vault B (isolated, balance visible)

✅ Veilfi Model:
User A ─┐
User B ─┼→ Shared Vault (pooled, individual balances hidden)
User C ─┘
```

**Benefit**: Larger anonymity set = stronger privacy.

### 3. No Unnecessary Data Collection

**What Veilfi Collects**:

- ✅ Wallet address (public anyway)
- ✅ Proof hashes (meaningless without secrets)
- ✅ Transaction timestamps (unavoidable on blockchain)

**What Veilfi Does NOT Collect**:

- ❌ IP addresses
- ❌ Email addresses
- ❌ Personal names
- ❌ Geographic location
- ❌ Usage analytics

**Result**: Minimal attack surface for privacy breaches.

### 4. Client-Side Proof Generation

**Wrong Way** (privacy leak):

```
User → Sends data to server → Server generates proof
                             ↑
                        Privacy leaked!
```

**Veilfi's Way**:

```
User's Browser → Generates proof locally → Submits proof to blockchain
               ↑
          Secrets never leave device!
```

**Implementation**:

```javascript
// All proof generation happens in-browser
const proof = await generateProof({
  privateInput: userBalance, // NEVER sent to server
  publicInput: minRequired,
});

// Only proof (no secrets) transmitted
await contract.submit(proof);
```

## Privacy vs. Other Priorities

### When Privacy Conflicts with UX...

**Example**: Proof generation takes ~10 seconds.

**Temptation**: Generate proofs server-side (instant, but leaks data).

**Veilfi's Choice**: Keep client-side generation, improve UX through:

- Loading animations
- Progress indicators
- Web Workers (non-blocking UI)

**Principle**: Never sacrifice privacy for convenience.

### When Privacy Conflicts with Performance...

**Example**: ZK verification costs ~300k gas (expensive).

**Temptation**: Skip ZK proofs for small deposits (cheaper, but public).

**Veilfi's Choice**: Offer optional public deposits BUT:

- Private deposits clearly labeled as recommended
- Warning shown before public deposits
- Default to private mode

**Principle**: Privacy should be accessible, not forced, but always encouraged.

## Privacy Guarantees

### Cryptographic Privacy

✅ **Deposit Amounts**: Hidden via ZK-SNARKs (mathematically secure)  
✅ **User Balances**: Not queryable (smart contract design)  
✅ **Withdrawal Sizes**: Proven without revelation (zero-knowledge property)

### Operational Privacy

✅ **No Logging**: Veilfi team cannot see user data  
✅ **No Analytics**: No tracking scripts or cookies  
✅ **No Third Parties**: No data sharing with partners

### Auditability

🔓 **Open Source**: All code public (community can verify)  
🔓 **Verifiable Proofs**: Anyone can check proof validity  
🔓 **Transparent TVL**: Total deposits visible (trust building)

**Balance**: Maximum user privacy, maximum protocol transparency.

## Privacy Attack Resistance

### Threat Model

| Attack Vector            | Veilfi's Defense                 |
| ------------------------ | -------------------------------- |
| **On-chain analysis**    | ZK proofs hide amounts           |
| **Timing correlation**   | Encourages delayed withdrawals   |
| **Network surveillance** | Recommends VPN/Tor usage         |
| **Frontend compromise**  | Open-source code (self-hostable) |
| **Server-side logging**  | Client-side proof generation     |

### What Veilfi Cannot Prevent

⚠️ **User mistakes**: Sharing wallet addresses publicly  
⚠️ **Browser tracking**: Use privacy-focused browsers  
⚠️ **Network metadata**: Use VPN for IP privacy  
⚠️ **Social engineering**: Phishing attacks still possible

**Recommendation**: Veilfi provides tools; users must use them correctly.

## Privacy Best Practices (For Users)

### Maximum Privacy Setup

1. **Fresh Wallet**:

   ```
   Create new MetaMask → Not linked to identity
   Fund via privacy-preserving method (DEX, not CEX)
   ```

2. **Network Privacy**:

   ```
   Use Tor Browser OR VPN
   Never connect from public WiFi without VPN
   ```

3. **Always Use ZK Proofs**:

   ```
   Choose "Private Deposit" option (not standard)
   Wait for proof generation (don't skip!)
   ```

4. **Timing Obfuscation**:
   ```
   Don't withdraw immediately after deposit
   Add random delays (hours/days)
   ```

## Privacy Philosophy in Code

Every technical decision reflects privacy-first thinking:

### Example 1: Event Emissions

**Privacy-Leaking Approach**:

```solidity
// ❌ Bad: Reveals deposit amount
event Deposit(address user, uint256 amount);

emit Deposit(msg.sender, depositAmount);  // PUBLIC!
```

**Veilfi's Approach**:

```solidity
// ✅ Good: Hides deposit amount
event PrivateDeposit(address indexed user, bytes32 commitment);

emit PrivateDeposit(msg.sender, proofHash);  // Amount unknown
```

### Example 2: View Functions

**Privacy-Leaking Approach**:

```solidity
// ❌ Bad: Anyone can query balance
function balanceOf(address user) public view returns (uint256) {
    return userBalances[user];  // EXPOSED!
}
```

**Veilfi's Approach**:

```solidity
// ✅ Good: Balances not publicly queryable
// Users know their balance from shares, but outsiders cannot query
function shares(address user) public view returns (uint256) {
    return _shares[user];  // Shares visible, but value requires calculation
}

// Share price public, but individual holdings unknown to outsiders
function pricePerShare() public view returns (uint256);
```

## Privacy vs. Regulatory Compliance

**False Dichotomy**: Privacy OR compliance.

**Veilfi's Reality**: Privacy AND compliance via ZK-KYC.

```
Traditional View:
Privacy ←──────────┼──────────→ Compliance
       (illegal)   │   (no privacy)

Veilfi's Innovation:
Privacy ←──ZK-KYC──→ Compliance
     (both achieved simultaneously)
```

**How**:

- Users prove KYC status without revealing identity
- Regulators satisfied (AML/KYC requirements met)
- Privacy preserved (no PII on-chain)

---

**Next**: Explore [Yield Optimization](./yield-optimization) to see how Veilfi maximizes returns.

**More on Privacy**: See [Privacy-Preserving DeFi](../key-concepts-definitions/privacy-preserving-defi).
