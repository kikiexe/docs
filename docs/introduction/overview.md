---
sidebar_position: 1
title: Overview
---

# Overview

## What is Veilfi?

Veilfi is a decentralized leverage trading protocol that enables users to access **5x leverage** with **20% collateral** through a community-funded liquidity pool. The protocol operates on the **Lisk blockchain** and integrates with **Velodrome AMM** for trading execution.

---

## 1-Minute Protocol Flow

### Problem -> Solution -> Flow

**Problem:** Traditional DeFi requires 150-200% collateral for 2-3x leverage -> **Capital inefficient**

**Veilfi's Solution:** 20% borrower margin + 80% pool funding = **5x leverage**

**How It Works:**

1.  **Borrower** deposits 20% collateral ($20k) -> Wants $100k position
2.  **Pool** allocates 80% funding ($80k) -> Total: $100k
3.  Combined capital sent to **RestrictedWallet** -> Chain-enforced trading
4.  **Borrower** trades via **Velodrome** -> Position grows/declines
5.  **Liquidation:** Time-based (30 day term) ✅ MVP | Price-based 🔄 Planned
6.  **Loss Allocation:** Margin absorbs first -> Pool protected
