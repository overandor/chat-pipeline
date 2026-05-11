# QR Read Token Allocation Protocol v0

**Anchor identity:** `overandor` / Joseph Skrobynets  
**Repo:** `overandor/chat-pipeline`  
**Protocol family:** MEMBRA / Human Chain / QR-Funded Idea Pool / Chat-to-Token Reward Protocol  
**Purpose:** define how every verified QR read of a chat/proof capsule can create an immediate token allocation event while preserving consent, anti-sybil protections, pool boundaries, and the distinction between token allocation and official money.

## Core product sentence

Every verified QR read of a MEMBRA chat can trigger an immediate token allocation event tied to that chat’s pool, proof capsule, and public rules.

## Hard boundary

A QR read can immediately allocate protocol units, points, credits, claim receipts, or testnet tokens.

A QR read should not automatically transfer valuable mainnet tokens or fiat unless:

```text
1. the reader accepts terms;
2. the wallet is connected;
3. the pool is funded;
4. anti-sybil checks pass;
5. token supply exists;
6. the smart contract/program authorizes the allocation;
7. compliance/risk rules allow it;
8. the user signs if required.
```

## Safe allocation types

### 1. Instant Scan Credit

A non-transferable or internal accounting unit created immediately after a verified QR read.

```text
low risk
fast UX
not money
can later convert by rules
```

### 2. Claimable Token Receipt

A hashed receipt saying the wallet is eligible for a token allocation.

```text
medium risk
claim requires wallet signature
allocation visible
actual mint/transfer can be delayed
```

### 3. Testnet Token Allocation

Devnet/testnet token allocation for proof and UX testing.

```text
not official money
not mainnet value
safe for public demo
```

### 4. Mainnet Token Allocation

Real SPL token allocation on Solana mainnet.

```text
higher risk
requires live mint
requires wallet signature or program-authorized airdrop
requires supply and rules
requires legal/compliance review
```

### 5. Funded Reward Claim

Claim against an actual support pool balance.

```text
withdrawable only if pool is funded
subject to lockup, anti-fraud, refund/dispute window, and rules
```

## Immediate QR read flow

```text
1. User scans QR.
2. QR opens chat proof page, not blind wallet execution.
3. Page displays chat hash, pool status, token supply, risk terms, and reward curve.
4. Reader accepts terms.
5. Reader optionally connects wallet.
6. System checks uniqueness and anti-sybil rules.
7. System calculates allocation.
8. System emits scan allocation receipt.
9. Receipt is hashed.
10. Receipt is written to database and optionally GitHub/IPFS/onchain.
11. If claimable, reader signs claim transaction.
12. Program transfers/mints/records allocation according to pool rules.
```

## Allocation object

```json
{
  "schema": "membra.qr_read_allocation.v0",
  "allocation_id": "ALLOC-YYYYMMDD-HHMMSS-000001",
  "chat_id": "CHAT-YYYYMMDD-000001",
  "pool_id": "POOL-YYYYMMDD-000001",
  "qr_id": "QR-YYYYMMDD-000001",
  "reader_wallet": "<public_wallet_or_null>",
  "reader_fingerprint_hash": "<privacy_preserving_hash_optional>",
  "scan_index": 1,
  "allocation_type": "scan_credit|claim_receipt|testnet_token|mainnet_token|funded_reward_claim",
  "token_symbol": "MCHAT<short_id>",
  "token_supply_total": "<user_defined_supply>",
  "allocation_amount": "<amount>",
  "originator_share_percent_before": 50,
  "originator_share_percent_after": 49,
  "participant_share_percent_after": 51,
  "decay_rule_hash": "<sha256>",
  "terms_accepted": true,
  "anti_sybil_status": "passed|pending|failed",
  "claim_status": "not_claimable|claimable|claimed|expired|blocked",
  "official_money_usd": "0.00_until_funded_settlement",
  "created_at": "<iso_timestamp>",
  "allocation_sha256": "<sha256>"
}
```

## Token allocation formula

The chat creator chooses total token supply for the chat.

```text
total_supply = user_defined
creator_reserve = total_supply * creator_reserve_percent
participant_pool = total_supply * participant_pool_percent
scan_allocation_base = participant_pool / max_participants
```

Decay-adjusted allocation:

```text
originator_share_n = max(originator_floor, 50% - n * decay_per_scan)
participant_share_n = 100% - originator_share_n
reader_allocation_n = scan_allocation_base * scan_weight_n
```

Where:

```text
n = verified scan/support count
scan_weight_n = novelty multiplier, early-reader multiplier, support multiplier, or fixed 1.0
```

## Example default rule

```json
{
  "total_supply": "1000000",
  "creator_reserve_percent": 50,
  "participant_pool_percent": 50,
  "max_participants": 1000,
  "base_allocation_per_verified_qr_read": "500",
  "early_reader_multiplier_first_100": 2.0,
  "decay_per_scan_percent": 0.05,
  "originator_floor_percent": 10,
  "requires_wallet_connect": true,
  "requires_terms_acceptance": true,
  "requires_human_or_captcha_check": true,
  "claim_window_days": 30
}
```

## Pool funding interaction

Token allocation and payout must remain separate.

```text
token allocation = participation/accounting/proof unit
pool funding = actual support balance
claimable reward = rules-based claim against funded pool
official money = settled external payment or successfully withdrawn value
```

A QR read may allocate tokens immediately.

A QR read does not create official money unless a funded payment event exists.

## Anti-sybil requirements

Before valuable allocations, use some combination of:

```text
wallet signature
rate limit
one wallet per QR allocation rule
captcha or proof-of-human check
optional KYC/notary for high-value claims
device/session risk score
IP/rate abuse detection
minimum support payment for valuable claim
cooldown windows
blacklist/denylist
manual review for suspicious clusters
```

## Smart contract / Solana program responsibilities

The Solana program should support:

```text
create_chat_pool
create_qr_campaign
record_verified_scan
calculate_allocation
emit_allocation_receipt
claim_allocation
pause_campaign
close_campaign
withdraw_protocol_fee
withdraw_creator_share
withdraw_participant_reward
```

The program should not evaluate idea quality. LLM appraisal remains offchain and is referenced by hash.

## QR read receipt memo

```text
MEMBRA_QR_ALLOC_V0;chat=<chat_id>;pool=<pool_id>;qr=<qr_id>;scan=<n>;wallet=<reader_wallet>;alloc=<amount>;official_money_usd=0.00_until_settlement
```

## Database schema

```sql
CREATE TABLE qr_campaigns (
  id TEXT PRIMARY KEY,
  chat_id TEXT NOT NULL,
  pool_id TEXT NOT NULL,
  token_symbol TEXT NOT NULL,
  token_supply TEXT NOT NULL,
  max_participants INTEGER,
  decay_rule_json TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE qr_read_allocations (
  id TEXT PRIMARY KEY,
  qr_campaign_id TEXT NOT NULL,
  chat_id TEXT NOT NULL,
  pool_id TEXT NOT NULL,
  reader_wallet TEXT,
  reader_fingerprint_hash TEXT,
  scan_index INTEGER NOT NULL,
  allocation_type TEXT NOT NULL,
  allocation_amount TEXT NOT NULL,
  claim_status TEXT NOT NULL,
  anti_sybil_status TEXT NOT NULL,
  allocation_json TEXT NOT NULL,
  allocation_sha256 TEXT NOT NULL,
  created_at TEXT NOT NULL
);
```

## UI modules

### 1. QR Allocation Console

Shows:

```text
QR read count
verified readers
token supply
remaining participant pool
next reader allocation
originator share now
participant share now
anti-sybil status
claimability status
```

### 2. Reader Claim Page

Shows:

```text
chat proof capsule
allocation terms
wallet connect
allocation amount
claim button
risk disclosure
receipt hash
```

### 3. Creator Campaign Panel

Shows:

```text
chat token supply editor
creator reserve percent
participant pool percent
decay rule editor
max participants
minimum support amount
claim window
pause campaign button
```

## TikTok-safe explanation

```text
Every MEMBRA chat can get a QR code.
When someone scans it, the protocol can immediately allocate that chat’s participation tokens or claim receipts.
The creator chooses token supply and the reward curve.
The first rule can start at 50% creator logic and decay as verified participants scan, support, or build.
But the token is not profit, the scan is not money, and real payouts require a funded pool or settled payment.
```

## One-sentence truth

MEMBRA can allocate chat-specific participation tokens immediately per verified QR read, while keeping real payouts tied to funded pools, signed claims, anti-sybil checks, and external settlement.
