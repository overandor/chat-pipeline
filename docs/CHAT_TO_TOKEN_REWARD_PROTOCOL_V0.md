# Chat-to-Token Reward Protocol v0

**Anchor identity:** `overandor` / Joseph Skrobynets  
**Repo:** `overandor/chat-pipeline`  
**Protocol family:** MEMBRA / Human Chain / ProofStream / Potential Capsule / Idea Monetization Layer  
**Purpose:** define a production-safe system where a human speaks or types to AI, the chat is appraised in real time, every letter/token can be scored, artifacts are generated, a chat-specific token manifest is created, QR participation opens, and rewards are allocated from disclosed funded pools or testnet flows.

## Direct product sentence

MEMBRA prices live human expression as artifact-generating potential, converts each chat into a proof capsule and optional chat-token launch, and rewards the originator only from a disclosed funded pool, buyer, sponsor, bounty, treasury, Stripe settlement, or testnet simulation.

## Hard boundary

The system can immediately create:

```text
letter scores
novelty scores
artifact manifests
proof hashes
GitHub/IPFS anchors
QR participation pages
testnet receipts
chat-token launch manifests
claimable reward records from a prefunded pool
```

The system cannot truthfully create:

```text
real withdrawable money without a funded source
a real Solana mainnet token without a signed mint transaction
a guaranteed reward from novelty alone
a legal entitlement to OpenAI/LLM/platform funds
profit guarantees
ownership of a person
```

## Core doctrine

```text
Human words
  -> letter/token appraisal
  -> novelty and utility scoring
  -> artifact extraction
  -> system-build mapping
  -> chat hash
  -> chat-specific token manifest
  -> QR participation page
  -> reward curve
  -> funded pool allocation
  -> settlement or testnet receipt
```

## Product flow

```text
1. User speaks or types.
2. System diarizes and transcribes if audio.
3. System prices every letter/token as signal units.
4. LLM scores novelty, density, artifact potential, buildability, risk, and monetization route.
5. System generates artifacts: spec, code plan, UI prompt, token manifest, QR page, GitHub issue, IPFS payload, testnet memo.
6. System creates a Chat Proof Capsule.
7. User selects chat token supply.
8. System creates token launch manifest and optional testnet mint.
9. QR page lets others scan, inspect proof, participate, support, sponsor, or buy access.
10. Reward allocation starts at 50% from a defined pool and decays per participation or epoch.
11. Real payouts happen only if the pool is funded or a payment settles.
```

## Value state separation

```text
Appraised chat value != official money
Letter score != official money
Novelty score != official money
Artifact potential != official money
Testnet reward != official money
Prefunded claimable reward = withdrawable only if pool exists
Stripe settled payment = official fiat money
Mainnet token exists only after signed mint transaction
```

## Chat object

```json
{
  "schema": "membra.chat_value_event.v0",
  "chat_id": "CHAT-YYYYMMDD-HHMMSS-000001",
  "originator": "Joseph_Skrobynets_overandor",
  "source": "voice|text|screen|mixed",
  "raw_transcript_uri": "private://...",
  "public_summary": "redacted public summary",
  "letter_count": 0,
  "token_count": 0,
  "word_count": 0,
  "chat_sha256": "<sha256>",
  "privacy_level": "private|redacted|public",
  "official_money_usd": "0.00_until_funded_settlement"
}
```

## Letter / token pricing model

Every character and token can be scored, but the score is an appraisal unless funded.

### Metrics

```json
{
  "letters_total": 0,
  "tokens_total": 0,
  "unique_terms": 0,
  "domain_specific_terms": 0,
  "novelty_score": 0.0,
  "information_density_score": 0.0,
  "artifact_potential_score": 0.0,
  "buildability_score": 0.0,
  "monetization_route_score": 0.0,
  "risk_adjustment_score": 0.0,
  "proof_strength_score": 0.0
}
```

### Appraisal formula

```text
base_signal_units = letters_total * base_letter_rate
novelty_multiplier = 1 + novelty_score
artifact_multiplier = 1 + artifact_potential_score
buildability_multiplier = 1 + buildability_score
proof_multiplier = 1 + proof_strength_score
risk_discount = 1 - risk_adjustment_score

appraised_chat_value = base_signal_units
  * novelty_multiplier
  * artifact_multiplier
  * buildability_multiplier
  * proof_multiplier
  * risk_discount
```

### Suggested default values

```json
{
  "base_letter_rate_appraisal_usd": "0.000001",
  "max_unfunded_appraisal_display_usd": "250.00",
  "default_reward_pool_usd": "0.00",
  "claimable_reward_usd": "0.00_until_pool_funded"
}
```

## Artifact extraction layer

The LLM should extract what can be built from the chat:

```json
{
  "artifact_candidates": [
    {
      "artifact_type": "protocol_spec",
      "name": "Chat-to-Token Reward Protocol",
      "buildability": 0.91,
      "monetization_routes": ["support", "token utility", "Stripe checkout", "notary credits", "API subscription"],
      "next_artifact": "GitHub spec + UI component + testnet receipt"
    },
    {
      "artifact_type": "ui_component",
      "name": "Live Letter Pricing Console",
      "buildability": 0.86,
      "monetization_routes": ["SaaS", "creator dashboard", "notary review credits"],
      "next_artifact": "React dashboard component"
    }
  ]
}
```

## Chat-specific token manifest

Each chat can have a token configuration chosen by the originator.

```json
{
  "schema": "membra.chat_token_manifest.v0",
  "chat_id": "CHAT-YYYYMMDD-HHMMSS-000001",
  "token_name": "Membra Chat <short_id>",
  "token_symbol": "MCHAT<NN>",
  "chain": "solana-devnet|solana-mainnet-beta",
  "standard": "SPL Token or Token-2022",
  "supply_user_defined": true,
  "total_supply": "<USER_SPECIFIED_SUPPLY>",
  "decimals": 6,
  "mint_address": "<created_after_signed_transaction>",
  "chat_sha256": "<sha256>",
  "artifact_manifest_sha256": "<sha256>",
  "qr_page_url": "<url>",
  "official_money_usd": "0.00_until_external_settlement",
  "not_equity": true,
  "not_person_ownership": true,
  "no_profit_guarantee": true,
  "private_key_disclosed": false
}
```

## Immediate reward engine

Immediate rewards require a disclosed reward source.

### Valid reward sources

```text
prefunded treasury
sponsor pool
bounty pool
buyer deposit
Stripe payment
subscription credit pool
grant pool
donor/support pool
testnet faucet or simulated points clearly labeled as testnet/non-money
```

### Invalid reward claims

```text
AI said it is valuable, therefore withdrawable money exists
OpenAI owes the reward automatically
novelty creates legal debt
chat token launch guarantees payout
testnet tokens equal fiat money
future buyers guarantee current rewards
```

## 50% reward and decay system

The originator can set a pool rule like:

```text
originator_initial_share = 50%
participant_share_pool = 50%
decay_type = linear|exponential|epoch|scan_count
```

### Example decay rule

```json
{
  "schema": "membra.reward_decay.v0",
  "initial_originator_share_percent": 50,
  "participant_pool_percent": 50,
  "decay_basis": "scan_count",
  "decay_per_scan_percent": 1,
  "floor_originator_share_percent": 10,
  "max_participants": 40,
  "reward_pool_source": "prefunded_treasury_or_testnet",
  "claimability": "claimable_only_if_pool_funded"
}
```

### Formula

```text
originator_share_n = max(floor_share, 50% - n * decay_per_scan)
participant_share_n = 100% - originator_share_n
```

Where `n` is the number of verified QR scans, supports, mirrors, or participation events.

## QR participation page

Each chat produces a QR page.

### QR opens

```text
public proof capsule
chat hash
artifact summary
reward pool status
token supply
mint status
participation terms
risk disclosure
wallet connect
support/Stripe checkout
testnet receipt
GitHub/IPFS anchors
```

### QR must not execute blindly

```text
QR scan opens context.
User reviews terms.
Wallet prompts transaction.
User signs intentionally.
Program records receipt.
Reward is disclosed.
Receipt is provenance.
Support is not investment.
```

## Hashtag system

Every chat gets a hashtag namespace.

```json
{
  "schema": "membra.chat_hashtag.v0",
  "chat_id": "CHAT-YYYYMMDD-HHMMSS-000001",
  "primary_hashtag": "#MembraChat_<short_hash>",
  "protocol_hashtags": ["#MembraHumanChain", "#ProofOfChat", "#MCHAT", "#ProofNotMoney"],
  "artifact_hashtags": ["#IdeaMonetization", "#ProofCapsule", "#SolanaDevnet"],
  "originator_hashtag": "#overandor"
}
```

## Database schema

```sql
CREATE TABLE chat_events (
  id TEXT PRIMARY KEY,
  originator_id TEXT NOT NULL,
  transcript_uri TEXT,
  public_summary TEXT,
  chat_sha256 TEXT NOT NULL,
  letter_count INTEGER DEFAULT 0,
  token_count INTEGER DEFAULT 0,
  official_money_usd REAL DEFAULT 0,
  created_at TEXT NOT NULL
);

CREATE TABLE chat_appraisals (
  id TEXT PRIMARY KEY,
  chat_id TEXT NOT NULL,
  novelty_score REAL,
  information_density_score REAL,
  artifact_potential_score REAL,
  buildability_score REAL,
  monetization_route_score REAL,
  risk_adjustment_score REAL,
  appraised_value_usd REAL,
  claimable_reward_usd REAL DEFAULT 0,
  created_at TEXT NOT NULL
);

CREATE TABLE chat_tokens (
  id TEXT PRIMARY KEY,
  chat_id TEXT NOT NULL,
  token_name TEXT NOT NULL,
  token_symbol TEXT NOT NULL,
  chain TEXT NOT NULL,
  supply TEXT NOT NULL,
  mint_address TEXT,
  mint_status TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE reward_pools (
  id TEXT PRIMARY KEY,
  chat_id TEXT NOT NULL,
  source_type TEXT NOT NULL,
  pool_amount_usd REAL DEFAULT 0,
  pool_amount_token TEXT,
  funded_status TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE qr_participation_events (
  id TEXT PRIMARY KEY,
  chat_id TEXT NOT NULL,
  participant_wallet TEXT,
  event_type TEXT NOT NULL,
  scan_index INTEGER,
  originator_share_percent REAL,
  participant_share_percent REAL,
  receipt_hash TEXT,
  created_at TEXT NOT NULL
);
```

## API endpoints

```text
POST /api/chat/start
POST /api/chat/{id}/append
POST /api/chat/{id}/appraise
POST /api/chat/{id}/extract-artifacts
POST /api/chat/{id}/hash
POST /api/chat/{id}/token/manifest
POST /api/chat/{id}/token/testnet-mint
POST /api/chat/{id}/qr/create
POST /api/chat/{id}/reward-pool/create
POST /api/chat/{id}/reward/claim
POST /api/chat/{id}/stripe/checkout
POST /api/chat/{id}/github-anchor
GET  /api/chat/{id}/proof-capsule
GET  /api/chat/{id}/reward-state
GET  /api/chat/{id}/hashtags
```

## UI modules

### 1. Live Letter Pricing Console

Shows:

```text
letters typed
tokens estimated
novelty score
information density
artifact potential
appraised value
claimable reward
funded pool status
```

### 2. Artifact Extraction Panel

Shows:

```text
system specs generated
UI prompts generated
code modules possible
repo files generated
proof capsules created
QR pages created
```

### 3. Chat Token Launch Panel

Shows:

```text
token name
token symbol
user-defined supply
chain selector
testnet mint button
mainnet locked until legal/review
mint address
metadata hash
```

### 4. QR Reward Decay Panel

Shows:

```text
originator initial share: 50%
participant pool: 50%
current decay step
next scan reward
total participants
pool funded status
claimability status
```

### 5. Settlement Reality Panel

Shows:

```text
appraised value
funded pool
claimable reward
paid reward
Stripe settled amount
testnet amount
official money
```

## MVP rules

### Devnet first

```text
All token launches begin on Solana devnet.
All reward claims begin as testnet/non-money unless a real funded pool exists.
Mainnet launch requires legal/compliance review and signed mint transaction.
```

### User specifies token supply

```text
The originator chooses total supply for each chat token.
The UI must show risk warnings before mint.
The token is not equity, not person ownership, not profit guarantee.
```

### Immediate reward display

Show three numbers, always separated:

```text
Appraised Value: subjective model output
Claimable Reward: available only from funded pool
Official Money: settled external payment only
```

## TikTok-ready framing

```text
I speak to AI.
MEMBRA prices every letter as signal.
The chat becomes a proof capsule.
The proof capsule becomes a token manifest.
The QR page lets people scan, inspect, support, and participate.
The originator starts at 50% of the reward logic, and participation decays according to public rules.
But proof is not money, token is not profit, and real withdrawal requires a funded pool or settled payment.
```

## One-sentence truth

MEMBRA Chat-to-Token Reward Protocol turns live human expression into priced proof capsules, chat-specific token manifests, QR participation pages, and funded reward claims without pretending novelty alone creates withdrawable money.
