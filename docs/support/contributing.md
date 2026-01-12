---
title: Contributing
sidebar_position: 4
---

# Contributing

Help build Veilfi - contributions welcome from everyone!

## Ways to Contribute

### 1. Code Contributions

**Smart Contracts**:

- Bug fixes
- Gas optimizations
- New strategy integrations
- Test coverage improvements

**Frontend**:

- UI/UX improvements
- New features
- Accessibility enhancements
- Performance optimizations

**ZK Circuits**:

- Circuit optimizations
- New proof types
- Security audits
- Documentation

### 2. Documentation

**Needed**:

- Tutorial videos
- Integration guides
- Translations (non-English)
- API reference docs
- Code examples

**How to help**:

1. Fork docs repo
2. Make improvements
3. Submit pull request

### 3. Testing & QA

**Help us test**:

- New features on testnet
- Edge cases & bugs
- Cross-browser compatibility
- Mobile experience
- Different wallets

**Report bugs**: GitHub Issues with reproduction steps

### 4. Community Support

**Be helpful**:

- Answer Discord questions
- Write tutorials/guides
- Create educational content
- Moderate channels
- Organize meetups

## Getting Started

### Setup Development Environment

```bash
# 1. Fork & clone repo
git clone https://github.com/YOUR_USERNAME/veilfi-protocol
cd veilfi-protocol

# 2. Install dependencies
npm install

# 3. Setup environment
cp .env.example .env
# Edit .env with your values

# 4. Run tests
npm run test

# 5. Start local node
npx hardhat node

# 6. Deploy locally
npm run deploy:local
```

### Coding Standards

**Solidity**:

```solidity
// Use Solidity 0.8.19+
pragma solidity ^0.8.19;

// Clear naming
contract StrategyVaultV2_Multi { ... }

// Comprehensive comments
/**
 * @notice Deposit ETH to vault
 * @param amount Amount to deposit in wei
 * @return shares Number of shares minted
 */
function deposit(uint256 amount) external returns (uint256 shares) {
    // Implementation
}

// Use NatSpec format
```

**TypeScript/JavaScript**:

```typescript
// Use TypeScript for type safety
interface VaultData {
  totalAssets: bigint;
  sharePrice: bigint;
  apy: number;
}

// Clear function names
async function fetchVaultData(): Promise<VaultData> {
  // Implementation
}

// JSDoc comments
/**
 * Generates ZK proof for private deposit
 * @param amount - Deposit amount in wei
 * @param secret - Random secret (32 bytes)
 * @returns Formatted proof for contract
 */
```

**Style**:

- Use Prettier for formatting
- Follow ESLint rules
- Write descriptive variable names
- Keep functions small & focused
- Add inline comments for complex logic

### Pull Request Process

1. **Create branch**

```bash
git checkout -b feature/your-feature-name
```

2. **Make changes**

- Write clear commit messages
- Follow coding standards
- Add tests for new features
- Update documentation

3. **Test thoroughly**

```bash
npm run test
npm run lint
npm run build
```

4. **Submit PR**

- Clear title describing change
- Description of what & why
- Link related issues
- Screenshots (for UI changes)

5. **Code review**

- Address feedback promptly
- Keep discussion professional
- Be open to suggestions

6. **Merge**

- Maintainer will merge once approved
- Celebrate! 🎉

## Contribution Ideas

### Good First Issues

**Beginner-friendly**:

- Fix typos in docs
- Add missing comments
- Improve error messages
- Write unit tests
- Update README

**Label**: `good-first-issue` on GitHub

### Advanced Contributions

**For experienced devs**:

- New yield strategies
- ZK circuit optimization
- Advanced ZK proofs (private withdrawals)
- Cross-chain integrations
- Security improvements

**Label**: `advanced` on GitHub

## Bug Reports

### How to Report

**Good bug report includes**:

1. **Title**: Clear, descriptive

   - ✅ "Withdrawal fails with 'insufficient liquidity' error"
   - ❌ "It doesn't work"

2. **Description**: What happened vs. expected

   ```
   Expected: Withdraw 1 ETH successfully
   Actual: Transaction reverts with error
   ```

3. **Steps to reproduce**:

   ```
   1. Connect wallet
   2. Navigate to Dashboard
   3. Click "Withdraw"
   4. Enter 1 ETH
   5. Click "Confirm"
   6. Transaction fails
   ```

4. **Environment**:

   - Browser: Chrome 120
   - Wallet: MetaMask 11.5
   - Network: Mantle Sepolia
   - Transaction hash: 0x...

5. **Screenshots/Videos**: If applicable

### Security Issues

**Critical bugs**: Email security@veilfi.xyz

**Don't**:

- Post publicly on GitHub
- Discuss in Discord
- Tweet about it

**Do**:

- Report privately
- Give team time to fix (responsible disclosure)
- Qualify for bug bounty

## Feature Requests

### Submit Ideas

**Template**:

```markdown
## Feature Request

**Problem**: What problem does this solve?

**Solution**: How would this feature work?

**Alternatives**: What else did you consider?

**Additional context**: Mockups, examples, etc.
```

### Voting on Features

Community votes on Discord polls or governance (future)

## Recognition

### Contributor Tiers

**Tier 1** (1-5 merged PRs):

- Contributor role in Discord
- Listed in CONTRIBUTORS.md

**Tier 2** (6-20 merged PRs):

- Core Contributor role
- Early access to features
- Direct contact with team

**Tier 3** (20+ merged PRs):

- Maintainer status
- Code review powers
- Governance rights
- Revenue share (future)

### Hall of Fame

Top contributors featured on:

- Website
- Documentation
- Twitter/Discord
- Annual report

## Code of Conduct

All contributors must follow our [Code of Conduct](../community#code-of-conduct):

- Be respectful
- Be inclusive
- Be collaborative
- Be transparent
- Be privacy-conscious

**Violations**: Warnings → temporary ban → permanent ban

## License

By contributing, you agree:

- Your code is licensed under MIT
- You have rights to contribute
- No backdoors or malicious code
- Contribution is yours or properly attributed

## Questions?

**Before contributing**:

- Read existing docs
- Check open issues/PRs
- Ask in Discord `#development`

**During development**:

- Post progress updates
- Ask for help when stuck
- Communicate blockers

---

**Thank you for helping build Veilfi!** 🙏

Every contribution, no matter how small, makes a difference.

Ready to start? Check out [good-first-issue](https://github.com/veilfi/protocol/labels/good-first-issue) on GitHub!
