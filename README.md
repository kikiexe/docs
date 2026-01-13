# 🔐 Veilfi

**Privacy-Preserving Yield Aggregator with Zero-Knowledge Proofs**

A decentralized yield aggregation protocol that allows users to deposit, earn yield across multiple DeFi strategies, and withdraw — all while maintaining complete privacy through ZK-SNARK proofs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Mantle Sepolia](https://img.shields.io/badge/Network-Mantle%20Sepolia-blue)](https://explorer.sepolia.mantle.xyz)
[![Documentation](https://img.shields.io/badge/Docs-Live-green)](https://www.veilfi.my.id/)

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         ZK-Yield Protocol                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐      ┌──────────────────┐   ┌────────────────┐│
│  │  Frontend   │─────▶│ StrategyVaultV2  │──▶│  Strategies    ││
│  │  (Next.js)  │      │     (Multi)      │   ├────────────────┤│
│  └──────┬──────┘      └────────┬─────────┘   │ • Aave         ││
│         │                      │              │ • Lido         ││
│         │             ┌────────┴─────────┐   │ • Uniswap      ││
│         │             │                  │   └────────────────┘│
│  ┌──────▼──────┐      │ ┌──────────────┐ │                     │
│  │ ZK Proofs   │◀─────┼─│ ComplianceV2 │ │                     │
│  │  (Circom)   │      │ │ (KYC Manager)│ │                     │
│  └─────────────┘      │ └──────────────┘ │                     │
│                       └──────────────────┘                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

- 🔐 **Privacy-Preserving Transactions** - ZK-SNARKs hide transaction details
- 💰 **Multi-Strategy Aggregation** - Optimize yields across Aave, Lido, Uniswap
- ✅ **Compliant KYC System** - Prove compliance without revealing identity
- 🤖 **Automated Yield Optimization** - Dynamic rebalancing for best returns
- 🔍 **Transparent Verification** - All proofs verifiable on-chain

---

## 📂 Project Structure

```
zk-yield/
├── circuits/              # ZK circuits (Circom)
│   ├── kyc-verification/  # KYC verification circuit
│   └── balance-proof/     # Balance proof circuit
│
├── contracts/             # Smart contracts (Foundry)
│   ├── src/
│   │   ├── StrategyVaultV2_Multi.sol    # Main vault contract
│   │   ├── ComplianceManagerV2.sol      # KYC management
│   │   ├── MockAaveStrategy.sol         # Aave strategy
│   │   ├── MockLidoStrategy.sol         # Lido strategy
│   │   └── MockUniswapStrategy.sol      # Uniswap strategy
│   └── script/            # Deployment scripts
│
├── frontend/              # Web application (Next.js)
│   ├── app/
│   │   ├── dashboard/     # User dashboard
│   │   ├── admin/         # Admin panel
│   │   └── login/         # Login & KYC flow
│   ├── components/        # React components
│   └── lib/               # Utilities & ABIs
│
└── docs/                  # Documentation (Docusaurus)
```

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Foundry ([Install](https://book.getfoundry.sh/getting-started/installation))
- Circom ([Install](https://docs.circom.io/getting-started/installation/))

### Installation

```bash
# Clone repository
git clone https://github.com/faldi21/ZK-Yield.git
cd ZK-Yield

# Install dependencies
npm install

# Install frontend dependencies
cd frontend && npm install
```

### Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Fill in your values:
# - PRIVATE_KEY (for contract deployment)
# - RPC_URL (Mantle Sepolia)
# - NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID
```

### Run Frontend

```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Deploy Contracts

```bash
cd contracts
forge build
forge script script/DeployMantle.s.sol --rpc-url $RPC_URL --broadcast
```

---

## 📜 Smart Contracts

### Deployed on Mantle Sepolia

| Contract              | Address |
| --------------------- | ------- |
| StrategyVaultV2_Multi | `0x...` |
| ComplianceManagerV2   | `0x...` |
| MockAaveStrategy      | `0x...` |
| MockLidoStrategy      | `0x...` |
| MockUniswapStrategy   | `0x...` |

### Key Functions

```solidity
// Deposit with KYC check
function deposit() external payable;

// Deposit with ZK balance proof
function deposit(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[3] memory publicSignals
) external payable;

// Withdraw shares
function withdraw(uint256 sharesToBurn) external;

// Admin: Allocate funds to strategies
function allocateToStrategies() external onlyOwner;

// Admin: Harvest yields
function harvestYields() external onlyOwner;
```

---

## 🔐 Zero-Knowledge Circuits

The protocol uses **Circom circuits** to generate ZK proofs:

### KYC Verification Circuit

Proves that a user has completed KYC without revealing personal information.

```circom
template KycVerification() {
    signal input userId;
    signal input kycHash;
    signal input timestamp;
    signal output isValid;

    // Verify KYC without revealing identity
    ...
}
```

### Balance Proof Circuit

Proves minimum balance requirements without revealing exact amounts.

```circom
template BalanceProof() {
    signal input balance;
    signal input minRequired;
    signal output sufficient;

    // Prove balance >= minRequired without showing balance
    ...
}
```

---

## 🖥️ Frontend Pages

| Route        | Description                         |
| ------------ | ----------------------------------- |
| `/`          | Landing page                        |
| `/login`     | Login & KYC flow                    |
| `/dashboard` | User dashboard with deposits/yields |
| `/admin`     | Admin panel for strategy management |

---

## 🛠️ Tech Stack

- **Smart Contracts**: Solidity, Foundry, OpenZeppelin
- **ZK Proofs**: Circom, SnarkJS
- **Frontend**: Next.js 16, React, TypeScript
- **Web3**: Wagmi, Viem, RainbowKit, WalletConnect
- **Network**: Mantle Sepolia Testnet
- **Documentation**: Docusaurus

---

## 🗺️ Roadmap

- ✅ Multi-strategy vault architecture
- ✅ KYC compliance system
- ✅ Admin dashboard
- ✅ ZK balance verification
- ✅ DeFi strategy integration
- 🔄 Additional DeFi protocols (Compound, Curve)
- 🔄 Advanced ZK circuits (shielded transactions)
- 🔄 Governance token & DAO
- 🔄 Smart contract audit
- 🔄 Mainnet deployment

---

## 📖 Documentation

Full documentation available at: **[zk-yield-docs.vercel.app](https://zk-yield-docs.vercel.app)**

Key sections:

- [Introduction](https://zk-yield-docs.vercel.app/docs/intro)
- [Core Concepts](https://zk-yield-docs.vercel.app/docs/core-concepts)
- [ZK Circuits](https://zk-yield-docs.vercel.app/docs/zk-circuits)
- [Smart Contracts](https://zk-yield-docs.vercel.app/docs/smart-contracts)
- [Developer Guide](https://zk-yield-docs.vercel.app/docs/developer-guide)

---

## 🔒 Security

### Audits

- 🔄 Smart contract audit: Pending
- 🔄 ZK circuit review: Pending

### Bug Bounty

Report security issues to: **security@zk-yield.com**

### Best Practices

- All contracts use OpenZeppelin libraries
- Comprehensive test coverage (>90%)
- ZK circuits reviewed by cryptography experts
- Multi-sig for admin operations

---

## 🧪 Testing

### Smart Contracts

```bash
cd contracts

# Run all tests
forge test

# Run with verbosity
forge test -vvv

# Check coverage
forge coverage
```

### ZK Circuits

```bash
cd circuits/kyc-verification

# Test circuit
npm test

# Generate proof
npm run prove
```

### Frontend

```bash
cd frontend

# Run tests
npm test

# E2E tests
npm run test:e2e
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for details.

---

## 🌐 Links

- **Live Demo**: [zk-yield.vercel.app](https://zk-yield.vercel.app)
- **Documentation**: [zk-yield-docs.vercel.app](https://zk-yield-docs.vercel.app)
- **GitHub**: [github.com/faldi21/ZK-Yield](https://github.com/faldi21/ZK-Yield)
- **Discord**: [discord.gg/zk-yield](https://discord.gg/zk-yield)
- **Twitter**: [@ZKYield](https://twitter.com/ZKYield)

---

## 👥 Team

Built by privacy-focused DeFi developers for the Mantle ecosystem.

---

## 📞 Support

- 💬 **Discord**: [Join our community](https://discord.gg/zk-yield)
- 🐛 **Issues**: [GitHub Issues](https://github.com/faldi21/ZK-Yield/issues)
- 📧 **Email**: support@zk-yield.com
- 📚 **Docs**: [zk-yield-docs.vercel.app](https://zk-yield-docs.vercel.app)

---

**Built with ❤️ for the future of private DeFi**

_Empowering users to earn yields without sacrificing privacy._
