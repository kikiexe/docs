---
title: Quick Start
sidebar_position: 1
---

# Developer Quick Start

Get ZK-Yield running locally in **under 10 minutes**! This guide will help you set up, run, and deploy the entire stack.

## Prerequisites

Before starting, ensure you have:

- ✅ **Node.js 18+** - [Download](https://nodejs.org/)
- ✅ **Foundry** - For smart contracts ([Install](https://book.getfoundry.sh/getting-started/installation))
- ✅ **Circom** - For ZK circuits ([Install](https://docs.circom.io/getting-started/installation/))
- ✅ **Git** - Version control
- ✅ **MetaMask** - Web3 wallet

### Quick Setup

```bash
# Install Node.js (if not installed)
# Windows: Download from nodejs.org
# Mac: brew install node
# Linux: sudo apt install nodejs npm

# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Install Circom
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
git clone https://github.com/iden3/circom.git
cd circom
cargo build --release
cargo install --path circom
```

---

## Step 1: Clone Repository

```bash
git clone https://github.com/faldi21/ZK-Yield.git
cd ZK-Yield
```

Project structure:

```
ZK-Yield/
├── circuits/          # ZK circuits (Circom)
├── contracts/         # Smart contracts (Solidity)
├── frontend/          # Web app (Next.js)
└── docs/              # Documentation
```

---

## Step 2: Install Dependencies

### Install All Dependencies

```bash
# Root dependencies
npm install

# Frontend dependencies
cd frontend
npm install
cd ..

# Contract dependencies (handled by Foundry)
cd contracts
forge install
cd ..
```

---

## Step 3: Environment Configuration

### Create Environment Files

```bash
# Copy environment templates
cp .env.example .env
cp frontend/.env.example frontend/.env.local
```

### Configure `.env` (Root)

```bash
# Wallet Private Key (for contract deployment)
PRIVATE_KEY=your_private_key_here

# RPC URLs
MANTLE_SEPOLIA_RPC=https://rpc.sepolia.mantle.xyz
MANTLE_MAINNET_RPC=https://rpc.mantle.xyz

# Etherscan API (for verification)
ETHERSCAN_API_KEY=your_api_key_here
```

### Configure `frontend/.env.local`

```bash
# WalletConnect Project ID (get from https://cloud.walletconnect.com)
NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID=your_project_id_here

# Contract Addresses (update after deployment)
NEXT_PUBLIC_VAULT_ADDRESS=0x...
NEXT_PUBLIC_COMPLIANCE_ADDRESS=0x...

# Network
NEXT_PUBLIC_CHAIN_ID=5003
NEXT_PUBLIC_RPC_URL=https://rpc.sepolia.mantle.xyz
```

---

## Step 4: Build ZK Circuits

### Compile Circuits

```bash
cd circuits

# Build KYC verification circuit
cd kyc-verification
chmod +x build.sh
./build.sh

# Build balance proof circuit (if exists)
cd ../balance-proof
chmod +x build.sh
./build.sh

cd ../..
```

This generates:

- ✅ `circuit.wasm` - Circuit WebAssembly
- ✅ `circuit.zkey` - Proving key
- ✅ `verification_key.json` - Verification key
- ✅ `verifier.sol` - Solidity verifier contract

---

## Step 5: Deploy Smart Contracts

### Compile Contracts

```bash
cd contracts
forge build
```

### Deploy to Mantle Sepolia

```bash
# Deploy all contracts
forge script script/DeployMantle.s.sol \
  --rpc-url $MANTLE_SEPOLIA_RPC \
  --broadcast \
  --verify

# Save deployed addresses
# Contracts will be deployed in this order:
# 1. ComplianceManagerV2
# 2. MockAaveStrategy
# 3. MockLidoStrategy
# 4. MockUniswapStrategy
# 5. StrategyVaultV2_Multi
```

### Update Frontend Config

After deployment, copy contract addresses to `frontend/.env.local`:

```bash
NEXT_PUBLIC_VAULT_ADDRESS=0x... # From deployment output
NEXT_PUBLIC_COMPLIANCE_ADDRESS=0x... # From deployment output
```

---

## Step 6: Run Frontend

### Start Development Server

```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Expected Pages

- `/` - Landing page
- `/login` - Login & KYC flow
- `/dashboard` - User dashboard
- `/admin` - Admin panel (requires owner wallet)

---

## Step 7: Test the Flow

### User Flow

1. **Connect Wallet**

   - Click "Connect Wallet" button
   - Select MetaMask
   - Switch to Mantle Sepolia network

2. **Complete KYC**

   - Go to `/login`
   - Submit KYC information
   - Generate ZK proof (happens automatically)
   - Proof stored locally

3. **Deposit Funds**

   - Go to `/dashboard`
   - Enter deposit amount
   - Optionally use privacy mode (with balance proof)
   - Confirm transaction

4. **View Yields**

   - Dashboard shows your shares
   - Real-time yield tracking
   - Strategy allocation breakdown

5. **Withdraw**
   - Enter share amount to withdraw
   - Confirm withdrawal
   - Receive funds

### Admin Flow

1. **Connect Owner Wallet**

   - Use the wallet that deployed contracts
   - Go to `/admin`

2. **Allocate Funds**

   - Set percentages for each strategy
   - Submit allocation transaction

3. **Harvest Yields**
   - Click "Harvest All Yields"
   - Collect from all strategies
   - Compound into vault

---

## Step 8: Run Tests

### Smart Contract Tests

```bash
cd contracts

# Run all tests
forge test

# Run with verbosity
forge test -vvv

# Run specific test
forge test --match-test testDeposit

# Check coverage
forge coverage
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test

# Run with coverage
npm test -- --coverage
```

### ZK Circuit Tests

```bash
cd circuits

# Test KYC circuit
cd kyc-verification
npm test

# Test balance circuit
cd ../balance-proof
npm test
```

---

## Common Commands

### Development

```bash
# Start frontend dev server
cd frontend && npm run dev

# Watch contract changes
cd contracts && forge build --watch

# Rebuild circuits
cd circuits && ./build-all.sh
```

### Deployment

```bash
# Deploy to testnet
cd contracts && forge script script/DeployMantle.s.sol --rpc-url $MANTLE_SEPOLIA_RPC --broadcast

# Verify contracts
forge verify-contract <address> <contract> --chain mantle-sepolia

# Deploy frontend
cd frontend && vercel --prod
```

### Testing

```bash
# Test everything
npm run test:all

# Test contracts only
cd contracts && forge test

# Test circuits only
cd circuits && npm test
```

---

## Troubleshooting

### Issue: Circuit build fails

**Solution**:

```bash
# Check Circom installation
circom --version

# Reinstall if needed
cargo install --path circom --force
```

### Issue: Contract deployment fails

**Solution**:

```bash
# Check RPC connection
curl -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  https://rpc.sepolia.mantle.xyz

# Check wallet has funds
# Get testnet ETH from faucet
```

### Issue: Frontend can't connect to wallet

**Solution**:

```bash
# Check WalletConnect Project ID
echo $NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID

# Get new one from https://cloud.walletconnect.com
# Update .env.local
```

### Issue: ZK proof generation fails

**Solution**:

```bash
# Check .wasm and .zkey files exist
ls circuits/kyc-verification/*.wasm
ls circuits/kyc-verification/*.zkey

# Rebuild circuit
cd circuits/kyc-verification && ./build.sh
```

---

## Next Steps

Now that you're set up, explore:

- **[Architecture Overview](../protocol-design/architecture-overview/core-vault-layer)** - Understand the system
- **[ZK Circuits Deep Dive](../zk-circuits/introduction)** - Learn about privacy
- **[Smart Contracts](../smart-contracts/overview)** - Review contract code
- **[Testing Guide](./testing/smart-contract-tests)** - Write comprehensive tests
- **[Deployment Guide](./development/deploy-contracts)** - Deploy to mainnet

---

## Get Help

- 📖 **Documentation**: You're reading it!
- 💬 **Discord**: [Join our community](https://discord.gg/zk-yield)
- 🐛 **Issues**: [GitHub Issues](https://github.com/faldi21/ZK-Yield/issues)
- 📧 **Email**: support@zk-yield.com

---

**Happy Building! 🚀**

Ready to create privacy-preserving DeFi applications? Let's go!
