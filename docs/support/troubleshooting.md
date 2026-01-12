---
title: Troubleshooting
sidebar_position: 2
---

# Troubleshooting

Common issues and how to fix them.

## Connection Issues

### Wallet won't connect

**Solutions**:

1. **Refresh page** (Ctrl+R / Cmd+R)
2. **Check wallet extension** is installed and unlocked
3. **Try different wallet** (MetaMask, Coinbase Wallet, etc.)
4. **Clear browser cache** and cookies
5. **Disable ad blockers** (can interfere with Web3)

### Wrong network error

**Problem**: "Please switch to Mantle Sepolia"

**Fix**:

```
1. Open wallet
2. Click network dropdown
3. Add Mantle Sepolia manually:
   - Network Name: Mantle Sepolia Testnet
   - RPC URL: https://rpc.sepolia.mantle.xyz
   - Chain ID: 5003
   - Currency: MNT
   - Explorer: https://explorer.sepolia.mantle.xyz
4. Switch to Mantle Sepolia
```

## Transaction Issues

### Transaction failed

**Common causes & fixes**:

**1. Insufficient gas**

```
Error: "insufficient funds for gas"
Fix: Get more MNT from faucet
```

**2. Gas price too low**

```
Error: "transaction underpriced"
Fix: Increase gas price in wallet settings
```

**3. Nonce error**

```
Error: "nonce too low"
Fix: Reset account in MetaMask (Settings → Advanced → Reset Account)
```

**4. Transaction reverted**

```
Error: "execution reverted"
Possible causes:
- Amount below minimum (0.01 ETH)
- Insufficient vault liquidity
- Contract paused (emergency)

Fix: Check error details on Explorer
```

### Transaction stuck/pending

**Solutions**:

1. **Wait** (may take 1-2 minutes)
2. **Speed up** (wallet option to increase gas)
3. **Cancel** (send 0 ETH to yourself with same nonce)
4. **Check Explorer** for actual status

## Deposit Issues

### Deposit not showing

**Checklist**:

1. ✅ Transaction confirmed? (check Explorer)
2. ✅ On correct network? (Mantle Sepolia)
3. ✅ Correct contract address?
4. ✅ Wait 30 seconds, refresh page

**If still not showing**:

- Clear cache and reconnect wallet
- Check transaction on Explorer for errors

### "Minimum deposit" error

**Problem**: Amount below 0.01 ETH

**Fix**: Deposit at least 0.01 ETH

### "Maximum exceeded" error

**Problem**: Single transaction limit exceeded

**Fix**: Split into multiple deposits (e.g., 2× 500 ETH instead of 1× 1000 ETH)

## Withdrawal Issues

### Cannot withdraw

**Possible causes**:

**1. Insufficient balance**

```
Fix: Check your actual balance (may have already withdrawn)
```

**2. Daily limit reached**

```
Error: "Daily withdrawal limit exceeded"
Fix: Wait 24 hours or withdraw smaller amount
```

**3. Vault liquidity**

```
Error: "Insufficient vault liquidity"
Fix: Wait 1-2 hours for strategy rebalancing
```

### Withdrawal amount lower than expected

**Explanation**: 0.1% withdrawal fee

**Example**:

```
Withdraw: 100 ETH
Fee: 0.1 ETH
Received: 99.9 ETH
```

## ZK Proof Issues

### Proof generation failed

**Solutions**:

**1. Out of memory**

```
Error: "JavaScript heap out of memory"
Fix:
- Close other tabs
- Use desktop browser (not mobile)
- Try standard deposit (skip ZK proof)
```

**2. Circuit files not loading**

```
Error: "Failed to fetch .wasm"
Fix:
- Check internet connection
- Hard refresh (Ctrl+Shift+R)
- Clear browser cache
```

**3. Proof generation timeout**

```
Error: "Timeout after 60s"
Fix:
- Wait and retry
- Use faster device
- Use standard deposit
```

### Proof verification failed

**Causes**:

- Proof corrupted during generation
- Wrong circuit version
- Browser compatibility issue

**Fix**: Regenerate proof or use standard deposit

## Display Issues

### Numbers not updating

**Fix**:

1. Refresh page
2. Disconnect and reconnect wallet
3. Clear browser cache

### Charts not showing

**Fix**:

1. Enable JavaScript
2. Disable privacy extensions (uBlock Origin, etc.)
3. Try different browser

### Wrong balance displayed

**Possible causes**:

- Multiple wallets connected (check active address)
- Cached data (refresh page)
- Wrong network (switch to Mantle Sepolia)

## Network Issues

### RPC errors

**Problem**: "Error connecting to RPC"

**Solutions**:

**Option 1: Use backup RPC**

```
Try different RPC in wallet settings:
- https://rpc.sepolia.mantle.xyz (primary)
- Add alternative if available
```

**Option 2: Wait and retry**

```
RPC may be temporarily down
Check Mantle status page
```

### Slow loading

**Optimizations**:

- Use wired internet (not WiFi)
- Disable VPN temporarily
- Try different RPC endpoint
- Use MetaMask instead of wallet browser

## Browser Compatibility

### Recommended browsers

✅ **Chrome** - Best compatibility  
✅ **Brave** - Good privacy + compatibility  
✅ **Firefox** - Good  
⚠️ **Safari** - May have issues with Web Workers  
❌ **Mobile browsers** - Limited ZK proof support

### If using Safari

**Issues**: ZK proof generation may fail

**Fix**:

1. Enable WebAssembly in settings
2. Allow cross-origin requests
3. Or use Chrome/Brave instead

## Advanced Issues

### Contract interaction failed

**Debug steps**:

1. **Check Explorer**

```
Copy transaction hash
View on https://explorer.sepolia.mantle.xyz
Check error message
```

2. **Check contract state**

```
Is contract paused? (emergency stop)
Is function callable?
Are parameters correct?
```

3. **Verify ABI**

```
Make sure using latest ABI
Check contract is verified on Explorer
```

### Gas estimation failed

**Causes**:

- Transaction would revert
- Contract state changed
- Insufficient balance

**Fix**:

- Check transaction parameters
- Verify sufficient balance
- Try manual gas limit (e.g., 500,000)

## Getting Help

If issue persists:

1. **Check [FAQ](/docs/support/faq)** first
2. **Search [Community](/docs/support/community)** for similar issues
3. **Ask in Discord** with:
   - Transaction hash (if applicable)
   - Error message
   - Browser & wallet used
   - Steps to reproduce

---

**Emergency**: If you believe there's a critical bug, report to security@veilfi.xyz
