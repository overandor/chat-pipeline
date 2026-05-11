# QR-Funded Idea Pool Protocol v0

**Anchor identity:** `overandor` / Joseph Skrobynets  
**Repo:** `overandor/chat-pipeline`  
**Protocol family:** MEMBRA / Human Chain / Chat-to-Token Reward Protocol / Idea Monetization Layer  
**Purpose:** define the QR payment and smart-contract pool model where payments sent through a QR gateway fund an idea-specific reward pool, allowing the originator and participants to support the creation, proof, and monetization potential of that idea.

## Core thesis

A QR payment into an idea pool is not an investment promise by default.

It is a disclosed support allocation into a protocol-managed pool attached to a specific idea, chat, proof capsule, artifact, or token manifest.

```text
QR scan
  -> idea proof page
  -> support terms reviewed
  -> wallet or Stripe payment
  -> pool receives funds
  -> receipt is created
  -> reward/participation accounting updates
  -> MEMBRA routes pool toward proof, build, notary, bounty, licensing, or payout rules
```

## Direct product sentence

MEMBRA lets people donate into their own idea-creation potential by funding QR-linked idea pools, while MEMBRA provides the proof, notary, token, reward-decay, settlement, and monetization protocol layer around those pools.

## What the pool represents

The pool represents disclosed support for an idea lifecycle.

It can fund:

1. originator rewards;
2. contributor rewards;
3. notary review;
4. KYC/compliance review where required;
5. testnet/mainnet anchoring costs;
6. artifact creation;
7. UI/app prototyping;
8. bounty payouts;
9. licensing preparation;
10. public proof capsule distribution.

It should not be represented as:

1. guaranteed profit;
2. equity;
3. ownership of the creator;
4. OpenAI payment;
5. automatic legal debt;
6. investment return;
7. wallet-key access;
8. official fiat settlement before actual payment clears.

## Full loop

```text
Human speaks/types idea
  -> LLM scores letters/tokens
  -> LLM extracts artifact candidates
  -> chat proof capsule created
  -> chat token manifest created
  -> user chooses token supply
  -> QR page generated
  -> support pool created
  -> participants scan QR
  -> participants review terms
  -> participants sign wallet tx or pay Stripe
  -> funds enter pool
  -> originator share and participant share update by decay rule
  -> pool can pay rewards or fund build tasks
  -> receipts are hashed and anchored
  -> external settlements are recorded separately
```

## Pool types

### 1. Testnet Pool

Used for devnet simulation and UX testing.

```text
official_money_usd = 0.00
claimable_fiat = false
purpose = demo, proof, mechanics, public testing
```

### 2. Support Pool

Funded by voluntary support payments.

```text
official_money_usd = amount actually settled
claimable_fiat = depends on treasury/rules
purpose = support, creator rewards, build funding
```

### 3. Bounty Pool

Funded for specific tasks.

```text
payout requires task completion and verification
purpose = build, verify, mirror, notarize, code, design, distribute
```

### 4. License Pool

Funded by a buyer or licensee.

```text
payout depends on license acceptance and terms
purpose = artifact access, commercial rights, limited use
```

### 5. Sponsor Pool

Funded by sponsor or community.

```text
purpose = public proof capsule, campaign, creator support, protocol visibility
```

## Smart contract / program role

The on-chain program should do only what it can verify:

```text
create pool
record pool config
receive payment or record reference
emit receipt
track participation count
apply decay math
track claimable balances
allow withdrawal only according to rules
pause in emergencies
emit proof events
```

The program should not claim to evaluate idea quality by itself.

LLMs can appraise and classify, but payout rights must come from pool rules, signatures, receipts, and funded balances.

## QR gateway rule

The QR code must open context first.

```text
QR opens idea page.
User reads terms.
User sees pool balance, risks, and purpose.
User sees that support is not investment.
Wallet opens only after confirmation.
User signs intentionally.
Receipt is created.
```

QR must not trigger blind execution.

## Pool schema

```json
{
  "schema": "membra.qr_funded_idea_pool.v0",
  "pool_id": "POOL-YYYYMMDD-HHMMSS-000001",
  "idea_id": "IDEA-YYYYMMDD-000001",
  "chat_id": "CHAT-YYYYMMDD-000001",
  "artifact_hash_sha256": "<sha256>",
  "token_manifest_hash_sha256": "<sha256>",
  "qr_page_url": "<url>",
  "chain": "solana-devnet|solana-mainnet-beta",
  "pool_address": "<program_or_treasury_address>",
  "payment_rails": ["solana_wallet", "stripe"],
  "official_money_usd": "0.00_until_settled_payment",
  "pool_purpose": "support|bounty|license|sponsor|testnet",
  "originator_share_initial_percent": 50,
  "participant_pool_percent": 50,
  "decay_rule": {
    "basis": "scan_count|support_count|epoch|time",
    "decay_per_event_percent": 1,
    "originator_floor_percent": 10
  },
  "risk_disclosures": {
    "not_equity": true,
    "not_profit_guarantee": true,
    "not_person_ownership": true,
    "support_not_investment": true
  }
}
```

## Payment receipt schema

```json
{
  "schema": "membra.idea_pool_payment_receipt.v0",
  "receipt_id": "RCPT-YYYYMMDD-000001",
  "pool_id": "POOL-YYYYMMDD-HHMMSS-000001",
  "payer_wallet_or_ref_hash": "<hash_or_public_wallet>",
  "rail": "solana|stripe|testnet",
  "amount": "<amount>",
  "currency_or_token": "SOL|USDC|USD|TEST",
  "tx_or_payment_ref": "<signature_or_stripe_event_hash>",
  "settlement_status": "testnet|pending|settled|failed|refunded|disputed",
  "receipt_sha256": "<sha256>",
  "created_at": "<iso_timestamp>"
}
```

## 50% reward / decay interpretation

The 50% rule is best framed as an initial allocation rule, not a profit promise.

```text
originator starts with 50% of reward logic
participant pool starts with 50%
as more verified participants scan/support/mirror/build, the originator share can decay toward a disclosed floor
participants receive shares according to public rules
only funded balances are withdrawable
```

### Example

```json
{
  "initial_originator_share_percent": 50,
  "participant_pool_percent": 50,
  "decay_per_verified_support_percent": 1,
  "originator_floor_percent": 10,
  "pool_balance_usd": 100,
  "claimable_rule": "claimable after settlement and anti-fraud window"
}
```

## Token supply per chat

Each chat can define token supply, but supply does not equal money.

```text
token supply = coordination / access / proof units
pool balance = funded value
claimable reward = rules-based withdrawal from funded balance
official money = settled payment
```

## MEMBRA fee model

Potential protocol fees can be disclosed as:

```text
platform_fee_percent = 5% to 15%
notary_fee = fixed or percentage
anchor_fee = pass-through chain/storage cost
creator_share = per pool rule
participant_share = per decay rule
refund_policy = explicit
```

All fees must be shown before support payment.

## UI modules

### 1. QR Idea Pool Page

Shows:

```text
idea title
public summary
artifact hash
pool purpose
pool balance
originator share
participant share
current decay step
support button
wallet connect
Stripe checkout
risk disclosures
GitHub/IPFS anchors
```

### 2. Pool Funding Console

Shows:

```text
rail: Solana / Stripe / testnet
payment status
settled amount
pending amount
refunded/disputed amount
claimable amount
```

### 3. Reward Decay Console

Shows:

```text
originator initial 50%
current originator share
participant pool share
verified participants
next decay event
floor share
```

### 4. Claim Console

Shows:

```text
claimable balance
lockup/anti-fraud timer
withdrawal wallet
receipt hash
claim transaction
```

## Legal/compliance warnings

Before mainnet or fiat launch, review:

```text
securities law
money transmission
consumer protection
tax
sanctions
advertising claims
data/privacy
refund/dispute obligations
KYC/AML if required
platform terms
```

## TikTok-safe description

```text
MEMBRA lets a chat become an idea pool.
The QR code opens the proof page.
Supporters review terms, then pay by wallet or Stripe.
That payment funds the pool around the idea.
The originator can start at 50% of the reward logic, and participation decays by public rules.
But support is not investment, token supply is not money, and withdrawals require real funded balances.
```

## One-sentence truth

MEMBRA turns QR payments into idea-specific support pools, then uses proof capsules, reward decay, token manifests, notary review, and settlement receipts to route funded value back to creators and participants without pretending unsupported novelty is withdrawable money.
