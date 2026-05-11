# Idea Monetization Layer v0

**Anchor identity:** `overandor` / Joseph Skrobynets  
**Repo:** `overandor/chat-pipeline`  
**Protocol family:** MEMBRA / Human Chain / ProofStream / Potential Capsule  
**Purpose:** define the first shippable monetization layer for verified ideas using LLM structuring, custom notary review, testnet on-chain receipts, and Stripe fiat settlement.

## Core thesis

Ideas are not automatically money.

Ideas become monetizable when they are:

```text
captured
structured
redacted
hashed
notarized
permissioned
listed
priced
accepted
settled
```

The Idea Monetization Layer converts a private idea into a verified economic artifact without pretending the idea has already produced official money.

## Primary flow

```text
Human idea
  -> consent capture
  -> LLM structuring
  -> redaction / private-alpha protection
  -> artifact manifest
  -> SHA-256 hash
  -> LLM-assisted notary review
  -> human notary / KYC checkpoint
  -> testnet on-chain receipt
  -> public proof capsule
  -> market listing / offer / bounty / license / sponsorship
  -> Stripe checkout or invoice
  -> fiat settlement receipt
  -> optional mainnet anchor after settlement
```

## Product doctrine

```text
Human idea -> verified artifact -> personal chain -> public proof -> funded payout
```

But the product must always separate:

```text
proof value != official money
market signal != official money
notary review != guaranteed value
Stripe settled payment = official fiat money
```

## First shippable product

Build the first version as a web app with five modules:

1. **Idea Intake**
2. **LLM Artifact Structuring**
3. **Notary / KYC Bridge**
4. **Testnet Monetization Receipt**
5. **Stripe Fiat Settlement Bridge**

## Module 1 — Idea Intake

The user submits an idea, pitch, workflow, prompt, video transcript, invention note, artifact, or proof-of-work package.

Required fields:

```json
{
  "title": "string",
  "summary": "string",
  "raw_input_type": "text|audio|video|image|repo|screen|mixed",
  "privacy_level": "private|redacted|public",
  "monetization_intent": "license|bounty|sponsor|sell_access|consulting|grant|support|service_credit",
  "owner_identity": "user_id_or_wallet_or_email",
  "consent": {
    "allow_llm_processing": true,
    "allow_notary_review": true,
    "allow_public_capsule": false,
    "allow_market_listing": false
  }
}
```

Hard boundaries:

```text
No private keys.
No seed phrases.
No wallet halves.
No raw KYC documents in public artifacts.
No unrevealed alpha published by default.
No claims of guaranteed payout.
```

## Module 2 — LLM Artifact Structuring

The LLM converts raw input into structured economic form.

Outputs:

```json
{
  "artifact_type": "idea|invention|software_spec|market_alpha|physical_inventory|proof_stream|content_asset|dataset|workflow",
  "public_summary": "redacted summary safe for publication",
  "private_summary": "full owner-only summary",
  "novelty_claims": ["claim 1", "claim 2"],
  "utility_claims": ["utility 1", "utility 2"],
  "risk_flags": ["securities risk", "privacy risk", "secret leakage risk"],
  "monetization_routes": ["license", "sponsor", "bounty", "consulting", "access token"],
  "required_evidence": ["repo", "demo", "timestamp", "screenshots", "testnet tx"],
  "redaction_map": {
    "public": ["hash", "timestamp", "summary"],
    "protected": ["method details", "private transcript"],
    "never_public": ["private keys", "raw KYC", "seed phrase"]
  }
}
```

The LLM may recommend value paths.

The LLM must not decide legal KYC validity, investment status, or official payout by itself.

## Module 3 — Notary / KYC Bridge

### Important boundary

LLM-based KYC is not enough by itself for regulated identity verification.

Use LLMs as triage, summarization, consistency-checking, document-classification, and notary-assistant tools.

A real notary / identity provider / compliance provider / human reviewer must be in the loop where legally required.

### Notary network roles

```text
User / Originator
  submits idea and identity claim

LLM Notary Assistant
  summarizes, checks consistency, detects missing fields, flags risk

Human Notary / Reviewer
  approves identity/provenance claims where required

Compliance Provider
  performs KYC/KYB/AML where legally required

Protocol Notary Node
  signs a notary attestation object

Public Ledger
  receives hash of notary attestation, not private identity docs
```

### Notary attestation object

```json
{
  "schema": "membra.notary.attestation.v0",
  "attestation_id": "NOTARY-YYYYMMDD-000001",
  "artifact_hash_sha256": "<sha256>",
  "originator_id_hash": "<hash_of_internal_user_id>",
  "notary_node_id": "<node_id>",
  "review_type": "identity|provenance|authorship|ownership_claim|settlement_review",
  "llm_assist_summary_hash": "<sha256>",
  "human_review_required": true,
  "human_review_status": "pending|approved|rejected|needs_more_info",
  "kyc_provider_reference_hash": "<hash_or_provider_ref>",
  "public_disclosure_level": "hash_only|redacted_summary|public_summary",
  "created_at": "<iso_timestamp>",
  "notary_signature": "<signature>"
}
```

Public chain should store only the attestation hash and minimal metadata.

## Module 4 — Testnet On-Chain Monetization Receipt

Use testnet first to prove the mechanics without claiming real settlement.

Testnet receipt represents:

```text
artifact exists
artifact was hashed
notary checkpoint happened
listing was created
offer was simulated or testnet-paid
payout logic can execute
```

Testnet receipt does **not** mean official money was paid.

### Testnet receipt schema

```json
{
  "schema": "membra.testnet.monetization_receipt.v0",
  "artifact_id": "ART-YYYYMMDD-000001",
  "artifact_hash_sha256": "<sha256>",
  "notary_attestation_hash": "<sha256>",
  "chain": "solana-devnet|base-sepolia|polygon-amoy|ethereum-sepolia",
  "testnet_tx": "<signature_or_tx_hash>",
  "monetization_route": "license|bounty|sponsor|support|service_credit",
  "testnet_amount": "<amount>",
  "fiat_settlement_status": "none|pending|settled",
  "official_money_usd": "0.00_until_stripe_settles"
}
```

### Minimal devnet memo payload

```text
MEMBRA_IDEA_V0;artifact=<artifact_id>;artifact_sha256=<hash>;notary_sha256=<hash>;route=<route>;official_money_usd=0.00
```

## Module 5 — Stripe Fiat Settlement Bridge

Stripe handles real fiat checkout, invoices, subscriptions, service credits, and receipts.

Do not claim official fiat money until Stripe confirms payment settlement.

### Stripe bridge events

```text
checkout.session.completed
payment_intent.succeeded
invoice.paid
charge.refunded
dispute.created
transfer.paid
```

### Fiat settlement receipt

```json
{
  "schema": "membra.fiat_settlement_receipt.v0",
  "artifact_id": "ART-YYYYMMDD-000001",
  "stripe_event_id": "evt_...",
  "stripe_payment_intent": "pi_...",
  "amount_gross_usd": "0.00",
  "amount_net_usd": "0.00",
  "currency": "usd",
  "settlement_status": "pending|succeeded|refunded|disputed|failed",
  "receipt_url_hash": "<hash_of_receipt_url_or_internal_ref>",
  "artifact_hash_sha256": "<sha256>",
  "notary_attestation_hash": "<sha256>",
  "testnet_receipt_tx": "<optional_testnet_tx>",
  "created_at": "<iso_timestamp>"
}
```

After Stripe settlement, optionally anchor a settlement hash onchain:

```text
MEMBRA_SETTLED_V0;artifact=<artifact_id>;settlement_sha256=<hash>;rail=stripe;amount_usd=<amount>;status=settled
```

Do not publish customer PII or raw Stripe data publicly.

## Database tables

```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT,
  public_wallet TEXT,
  kyc_status TEXT DEFAULT 'unverified',
  created_at TEXT NOT NULL
);

CREATE TABLE ideas (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  title TEXT NOT NULL,
  raw_input_uri TEXT,
  raw_input_sha256 TEXT,
  privacy_level TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE artifacts (
  id TEXT PRIMARY KEY,
  idea_id TEXT NOT NULL,
  public_summary TEXT,
  private_summary_uri TEXT,
  artifact_json TEXT NOT NULL,
  artifact_sha256 TEXT NOT NULL,
  monetization_route TEXT,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE notary_attestations (
  id TEXT PRIMARY KEY,
  artifact_id TEXT NOT NULL,
  attestation_json TEXT NOT NULL,
  attestation_sha256 TEXT NOT NULL,
  notary_node_id TEXT,
  human_review_status TEXT NOT NULL,
  kyc_provider_reference_hash TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE chain_receipts (
  id TEXT PRIMARY KEY,
  artifact_id TEXT NOT NULL,
  chain TEXT NOT NULL,
  cluster TEXT NOT NULL,
  tx_hash TEXT NOT NULL,
  receipt_json TEXT NOT NULL,
  receipt_sha256 TEXT NOT NULL,
  official_money_usd REAL DEFAULT 0,
  created_at TEXT NOT NULL
);

CREATE TABLE stripe_settlements (
  id TEXT PRIMARY KEY,
  artifact_id TEXT NOT NULL,
  stripe_event_id TEXT NOT NULL,
  payment_intent_id TEXT,
  amount_gross_usd REAL,
  amount_net_usd REAL,
  currency TEXT,
  settlement_status TEXT NOT NULL,
  receipt_json TEXT NOT NULL,
  receipt_sha256 TEXT NOT NULL,
  created_at TEXT NOT NULL
);
```

## API endpoints

```text
POST /api/ideas/intake
POST /api/ideas/{id}/structure
POST /api/artifacts/{id}/hash
POST /api/artifacts/{id}/notary/request
POST /api/notary/{id}/review
POST /api/artifacts/{id}/testnet/anchor
POST /api/artifacts/{id}/market/list
POST /api/artifacts/{id}/stripe/checkout
POST /api/stripe/webhook
GET  /api/artifacts/{id}/proof
GET  /api/users/{id}/value-dashboard
```

## MVP UI screens

1. **Idea Intake Studio**
   - paste idea / upload transcript / link repo
   - privacy selector
   - monetization route selector
   - consent toggles

2. **LLM Structuring Review**
   - public summary
   - private summary
   - novelty claims
   - risk flags
   - redaction map

3. **Notary Queue**
   - artifact hash
   - LLM assistant summary
   - human review status
   - KYC status
   - approve/reject/needs-info buttons

4. **Testnet Receipt Console**
   - chain selector
   - memo payload
   - tx hash
   - explorer link
   - official money status = $0.00

5. **Stripe Bridge Console**
   - create checkout
   - invoice status
   - event log
   - receipt hash
   - settled money amount

6. **Public Proof Capsule Page**
   - artifact title
   - redacted public summary
   - hash
   - notary attestation status
   - testnet receipt
   - settlement status
   - support/license/offer CTA

## Value state machine

```text
Raw Idea
  -> Structured Artifact
  -> Hash Commitment
  -> Notary Attestation
  -> Testnet Receipt
  -> Public Proof Capsule
  -> Market Offer
  -> Stripe Settlement
  -> Official Money
```

## What to build first

### Sprint 1

```text
Idea intake form
LLM structuring endpoint
Artifact hash generator
SQLite/Postgres schema
Public proof capsule page
GitHub anchor writer
```

### Sprint 2

```text
Notary queue
Human reviewer panel
KYC provider placeholder adapter
Attestation hash
Solana devnet memo or EVM testnet transaction
```

### Sprint 3

```text
Stripe checkout
Stripe webhook
Settlement receipt hash
Dashboard separation of proof/product/signal/money
```

### Sprint 4

```text
Public marketplace/listing page
Support/license/bounty routes
User wallet identity
Admin risk console
```

## Safety and compliance boundaries

1. LLM does not perform final legal KYC by itself.
2. Human or regulated provider review is required where identity verification matters.
3. Testnet monetization is not real money.
4. Stripe settlement is real only when payment succeeds and is not refunded/disputed.
5. No private keys or seed phrases are collected.
6. No raw KYC docs are published.
7. No profit guarantees.
8. No claim that OpenAI, Stripe, GitHub, TikTok, or any chain officially backs the idea unless a written agreement exists.
9. Public artifacts are redacted by default.
10. User consent is required before public listing.

## One-sentence product truth

MEMBRA Idea Monetization Layer turns private human ideas into verified, notarized, testnet-anchored, fiat-settleable artifacts without pretending proof is already money.
