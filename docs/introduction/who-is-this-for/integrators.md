---
title: Integrators
sidebar_position: 3
---

# Integrators

Veilfi is designed to be **composable and integration-friendly** for developers, protocols, DAOs, and institutions building on top of privacy-preserving DeFi infrastructure.

## Key Benefits for Developers

### 1. Privacy Primitive for Your Protocol

Integrate Veilfi's privacy layer into your DeFi application:

**Example Use Cases**:

- **DAO Treasury Management**: Private yield earning for governance treasuries
- **Payroll Platforms**: Privacy-preserving salary distributions with yield
- **Savings Apps**: Consumer-facing products with private balances
- **Institutional Vaults**: Enterprise yield aggregation with compliance

### 2. ERC-4626 Compatibility

Veilfi implements the **ERC-4626 Tokenized Vault Standard**:

```solidity
interface IERC4626 {
    // Standard vault functions
    function deposit(uint256 assets, address receiver) external returns (uint256 shares);
    function withdraw(uint256 assets, address receiver, address owner) external returns (uint256 shares);
    function totalAssets() external view returns (uint256);
    function convertToShares(uint256 assets) external view returns (uint256);
    function convertToAssets(uint256 shares) external view returns (uint256);
}
```

**Benefit**: Drop-in replacement for existing vault integrations (Yearn, Beefy, etc.).

### 3. Programmable Privacy via Smart Contracts

Interact with Veilfi programmatically:

```solidity
// Your contract can deposit on behalf of users
contract MyDeFiApp {
    IVeilfiVault public veilfiVault;

    function depositToPrivateYield(uint256 amount) external {
        // Transfer user funds
        IERC20(ETH).transferFrom(msg.sender, address(this), amount);

        // Deposit to Veilfi with privacy
        veilfiVault.depositWithProof{value: amount}(
            proof.a,
            proof.b,
            proof.c,
            proof.publicSignals
        );

        // User earns yield privately
    }
}
```

### 4. ZK Proof Generation Tools

Use Veilfi's open-source ZK libraries:

```javascript
import { generateKYCProof, generateBalanceProof } from "@veilfi/zk-circuits";

// Generate proof client-side
const proof = await generateBalanceProof({
  balance: userBalance,
  minRequired: minimumDeposit,
});

// Submit to contract
await vaultContract.depositWithProof(
  proof.proof.a,
  proof.proof.b,
  proof.proof.c,
  proof.publicSignals
);
```

**Benefit**: Reusable privacy infrastructure for your own applications.

## Integration Opportunities

### Read-Only Integration (Low Effort)

**Query Veilfi Data for Analytics**:

```javascript
// Get total vault metrics
const tvl = await veilfiVault.totalAssets();
const sharePrice = await veilfiVault.convertToAssets(
  ethers.utils.parseEther("1")
);

// Display in your dashboard
console.log(`Veilfi TVL: ${ethers.utils.formatEther(tvl)} ETH`);
console.log(`Share Price: ${ethers.utils.formatEther(sharePrice)} ETH`);
```

**Use Cases**:

- DeFi aggregators (DeFiLlama, DeBank)
- Portfolio trackers (Zapper, Zerion)
- Yield comparison tools

### Programmatic Deposits (Medium Effort)

**Enable Users to Deposit via Your UI**:

```typescript
// Example: Savings app integration
async function depositUserSavings(amount: bigint) {
  // 1. Generate ZK proof (optional for privacy)
  const proof = await generateDepositProof({
    amount,
    userSecret: wallet.privateKey,
  });

  // 2. Deposit to Veilfi
  const tx = await veilfiVault.depositWithProof(
    proof.a,
    proof.b,
    proof.c,
    proof.publicSignals,
    { value: amount }
  );

  await tx.wait();

  // 3. User now earns yield via Veilfi
  return tx.hash;
}
```

**Use Cases**:

- Wallet apps (MetaMask Snap, Rabby)
- DeFi dashboards (Instadapp, Zapper)
- DAO tooling (Gnosis Safe app)

### Advanced Integrations (High Effort)

**Build Composable Protocols on Veilfi**:

1. **Leveraged Privacy Vaults**:

   ```solidity
   // Take loan against Veilfi shares
   contract VeilfiLending {
       function borrowAgainstPrivateShares(uint256 shares) external {
           // Users can collateralize without revealing balance
       }
   }
   ```

2. **Privacy-Preserving Stablecoins**:

   ```solidity
   // Mint stablecoin backed by Veilfi yields
   contract PrivateStablecoin {
       function mintFromVeilfiYield(address user) external {
           // Collateral amount hidden via ZK proofs
       }
   }
   ```

3. **Anonymous Yield Derivatives**:
   ```solidity
   // Tokenize future Veilfi yields
   contract YieldTokenization {
       function mintYieldToken(uint256 shares) external {
           // Trade yields without exposing principal
       }
   }
   ```

## Integration Methods

### Method 1: Direct Contract Interaction

**Best For**: Maximum control, custom UX

```solidity
// Directly call Veilfi contracts
IVeilfiVault vault = IVeilfiVault(VEILFI_VAULT_ADDRESS);

function myDepositFunction(uint256 amount) external {
    vault.deposit{value: amount}();
}
```

**Pros**: Full flexibility, no dependencies  
**Cons**: More code to write

### Method 2: SDK Integration

**Best For**: Faster development, maintained by Veilfi team

```javascript
import { VeilfiSDK } from "@veilfi/sdk";

const veilfi = new VeilfiSDK({
  network: "mantle",
  wallet: userWallet,
});

// Simplified deposit
await veilfi.deposit({
  amount: ethers.utils.parseEther("10"),
  privacy: true, // Auto-generates ZK proof
});
```

**Pros**: Easy integration, automatic updates  
**Cons**: Dependency on Veilfi SDK

### Method 3: Widget Embedding

**Best For**: Non-technical integration, quick deployment

```html
<!-- Embed Veilfi deposit widget in your site -->
<iframe src="https://widget.veilfi.xyz/deposit" width="400" height="600">
</iframe>
```

**Pros**: Zero code required  
**Cons**: Limited customization

## API Reference

### Core Vault Functions

#### `deposit()`

```solidity
function deposit() external payable returns (uint256 shares)
```

Standard public deposit (amount visible on-chain).

#### `depositWithProof()`

```solidity
function depositWithProof(
    uint256[2] memory a,
    uint256[2][2] memory b,
    uint256[2] memory c,
    uint256[3] memory publicSignals
) external payable returns (uint256 shares)
```

Private deposit (amount hidden via ZK proof).

#### `withdraw()`

```solidity
function withdraw(uint256 sharesToBurn) external returns (uint256 assets)
```

Withdraw ETH/USDC by burning vault shares.

#### `totalAssets()`

```solidity
function totalAssets() external view returns (uint256)
```

Total vault TVL (public).

#### `balanceOf()`

```solidity
function balanceOf(address user) external view returns (uint256 shares)
```

User's share balance (public).

### ZK Proof Generation (Off-Chain)

#### `generateKYCProof()`

```javascript
async function generateKYCProof(params) {
  // params: { userId, kycHash, timestamp }
  // Returns: { proof, publicSignals }
}
```

#### `generateBalanceProof()`

```javascript
async function generateBalanceProof(params) {
  // params: { balance, minRequired }
  // Returns: { proof, publicSignals }
}
```

## Integration Best Practices

### 1. Gas Optimization

**Problem**: ZK proof verification costs ~300k gas (expensive).

**Solution**: Batch operations when possible.

```solidity
// ❌ Bad: Each user pays 300k gas
for (uint i = 0; i < users.length; i++) {
    vault.depositWithProof(...);  // Expensive!
}

// ✅ Good: Single batched transaction
vault.batchDepositWithProofs(proofs);  // Amortized gas
```

### 2. Proof Generation Performance

**Problem**: Generating ZK proofs takes ~10 seconds on mobile.

**Solution**: Use Web Workers to avoid blocking UI.

```javascript
// In web worker
import { generateProof } from "@veilfi/zk-circuits";

self.addEventListener("message", async (event) => {
  const proof = await generateProof(event.data);
  self.postMessage(proof); // Send back to main thread
});
```

### 3. Error Handling

**Common Errors**:

| Error                | Cause                        | Solution                    |
| -------------------- | ---------------------------- | --------------------------- |
| `InvalidProof`       | Proof verification failed    | Regenerate proof            |
| `InsufficientShares` | Withdrawal > balance         | Check user balance first    |
| `KYCNotVerified`     | User not KYC'd (if required) | Prompt KYC flow             |
| `SlippageTooHigh`    | Share price moved            | Increase slippage tolerance |

**Example Error Handler**:

```javascript
try {
  await vault.depositWithProof(...);
} catch (error) {
  if (error.message.includes('InvalidProof')) {
    // Regenerate proof and retry
    const newProof = await generateProof(params);
    await vault.depositWithProof(newProof);
  } else {
    throw error;
  }
}
```

### 4. Privacy Considerations for Integrators

**Do**:

- ✅ Generate ZK proofs client-side (never server-side)
- ✅ Use HTTPS for all API calls
- ✅ Recommend VPNs to end users
- ✅ Avoid logging sensitive parameters

**Don't**:

- ❌ Log user deposit amounts
- ❌ Store ZK proof secrets
- ❌ Expose user balances in analytics
- ❌ Link user identities to vault addresses

## Support for Integrators

### Technical Documentation

- **GitHub**: [github.com/veilfi/contracts](https://github.com/veilfi)
- **SDK Docs**: [docs.veilfi.xyz/sdk](https://docs.veilfi.xyz)
- **API Reference**: [docs.veilfi.xyz/api](https://docs.veilfi.xyz)

### Developer Resources

- **Discord**: [discord.gg/veilfi](https://discord.gg) - #dev-support channel
- **Example Integrations**: See `examples/` in GitHub repo
- **Video Tutorials**: YouTube integration guides

### Partnership Opportunities

Interested in deep integration? Contact us:

- **Email**: partnerships@veilfi.xyz
- **Telegram**: @veilfi_dev
- **Grant Program**: Apply for integration grants

## Example Integrations

### Example 1: Gnosis Safe App

```typescript
// Gnosis Safe app for private yield
import { SafeAppProvider } from "@gnosis.pm/safe-apps-sdk";
import { VeilfiSDK } from "@veilfi/sdk";

const safeApp = new SafeAppProvider();
const veilfi = new VeilfiSDK({ wallet: safeApp });

// DAO deposits treasury privately
await veilfi.deposit({
  amount: ethers.utils.parseEther("1000000"),
  privacy: true,
});
```

### Example 2: DeFi Aggregator Widget

```jsx
// React component for yield comparison
function YieldComparator() {
  const [veilfiAPY, setVeilfiAPY] = useState(0);

  useEffect(() => {
    // Fetch Veilfi yield
    const apy = await veilfi.getAPY();
    setVeilfiAPY(apy);
  }, []);

  return (
    <div>
      <h3>Best Yields:</h3>
      <ul>
        <li>Aave: 5% APY</li>
        <li>Veilfi: {veilfiAPY}% APY (Private!)</li>
      </ul>
    </div>
  );
}
```

### Example 3: Institutional API

```python
# Python backend for institutional deposits
from veilfi import VeilfiClient

client = VeilfiClient(
    rpc_url="https://rpc.mantle.xyz",
    private_key=INSTITUTION_KEY
)

# Institutional treasury deposit
tx_hash = client.deposit_private(
    amount=1_000_000 * 10**18,  # 1M ETH
    kyc_proof=institution_kyc_proof
)

print(f"Private deposit: {tx_hash}")
```

---

**Ready to integrate?** Check out the [Integration Guide](../../integration-guide/overview) for detailed instructions.

**Need custom features?** Email partnerships@veilfi.xyz for enterprise solutions.
