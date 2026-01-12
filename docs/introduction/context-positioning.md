---
sidebar_position: 1
title: Context & Positioning
---

# Context & Positioning

## The Problem: The Transparency Paradox

DeFi allows anyone to earn yield (Aave, Lido), but it forces **Radical Transparency**. 
* Every deposit is public.
* Every wallet balance is visible.
* Once your address is known, your entire financial net worth is exposed.

For privacy-conscious users and institutions, **using DeFi means losing privacy.**

## Enter Veilfi

**Veilfi** is a privacy-preserving yield aggregator built on Mantle. 

We allow users to:
1.  **Deposit funds** into a shared anonymity set.
2.  **Earn yield** from battle-tested protocols (Aave, Lido, Uniswap).
3.  **Withdraw privately** using Zero-Knowledge Proofs.

### Why Veilfi? (The Hackathon "Alpha")

Unlike Tornado Cash (which yields 0% and has high regulatory risk), Veilfi is **Compliance-Friendly** and **Capital Efficient**.

| Feature | Tornado Cash | Aave/Lido | **Veilfi** |
| :--- | :---: | :---: | :---: |
| **Privacy** | ✅ | ❌ | ✅ |
| **Earns Yield** | ❌ | ✅ | ✅ |
| **KYC Option** | ❌ | ❌ | ✅ |

### How It Works (Simplified)
We use a **Multi-Strategy Vault** coupled with **Circom ZK Circuits**. Users prove they own a share of the vault without revealing *which* deposit was theirs.

> **Veilfi = Privacy of a Mixer + Yield of a DeFi Protocol.**