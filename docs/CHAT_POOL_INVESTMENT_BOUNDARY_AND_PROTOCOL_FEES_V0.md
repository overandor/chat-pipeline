# Chat Pool Investment Boundary and Protocol Fee Model v0

**Anchor identity:** `overandor` / Joseph Skrobynets  
**Repo:** `overandor/chat-pipeline`  
**Protocol family:** MEMBRA / Human Chain / QR-Funded Idea Pool / Chat-to-Token Reward Protocol  
**Purpose:** define the boundary between safe chat-specific support pools and high-risk investment-like claims, while describing a compliant protocol-fee model for MEMBRA revenue from deployed chats.

## Direct boundary

Treating each chat as a protocol people can support on Solana is feasible.

Treating each chat as an investment where buyers expect revenue from all future MEMBRA chats, or where buying MEMBRA gives ownership of MEMBRA and revenue flow from all chats, may create securities, investment-contract, fund, revenue-share, broker/dealer, crowdfunding, tax, and money-transmission issues.

Therefore, the production design must separate:

```text
chat-specific support pool
protocol usage fee
creator reward
participant reward
governance or ownership rights
company equity / revenue share
```

Do not collapse all of these into one public token without legal/compliance review.

## Regulatory warning

Under the Howey-style investment contract analysis, an arrangement can become a securities transaction when there is an investment of money in a common enterprise with a reasonable expectation of profits derived from the efforts of others.

MEMBRA must avoid marketing public chat tokens as passive profit claims or ownership of all future chat revenues unless structured and registered/exempted properly.

## Safe design principle

```text
Each chat can have a support pool.
Each support pool can have public rules.
Each pool can reward the creator and verified contributors from actual funded balances.
MEMBRA can charge protocol fees for software, notary, anchoring, routing, and settlement services.
MEMBRA ownership/revenue-share must be handled separately through proper legal structure.
```

## What is allowed in v0

### 1. Chat-specific support pool

A user creates a chat proof capsule. Supporters scan a QR code and contribute to that specific pool.

```text
supporter pays voluntarily
supporter receives receipt / access / badge / service credit / participation unit
creator receives allocation from funded balance
contributors may receive allocation from funded balance
MEMBRA receives disclosed protocol fee
```

### 2. Protocol fee

MEMBRA takes a disclosed fee for operating the infrastructure.

Fee examples:

```text
platform_fee = 5% to 15%
notary_fee = fixed or percentage
anchor_fee = pass-through chain/storage cost
Stripe_fee = pass-through payment processor fee
creator_payout = remaining balance per pool rules
contributor_payout = remaining balance per pool rules
```

### 3. Support/access utility token

A token can represent:

```text
access
support status
service credits
proof participation
notary credits
artifact participation
reputation/badge rights
```

It should not be marketed as:

```text
ownership of MEMBRA
ownership of all chats
claim on all future revenue
guaranteed profit
passive investment return
OpenAI/ChatGPT money
ownership of a human
```

## High-risk design that needs legal structure

The following needs counsel before launch:

```text
Buy MEMBRA token and receive revenue from all chats.
Buy chat token and profit from other people building the protocol.
Token holders own MEMBRA.
Protocol fee revenue automatically flows to public token holders.
Token supply entitles holders to dividends.
Public buyers receive equity-like rights.
```

This may require securities compliance, corporate governance, tax structuring, investor disclosures, transfer restrictions, and possibly registration or exemption.

## Recommended two-layer architecture

### Layer A — Public protocol utility layer

```text
chat support pools
creator rewards
contributor rewards
service credits
access passes
notary credits
QR receipts
Solana proof receipts
Stripe settlement receipts
```

This layer can be launched first with strict disclosures.

### Layer B — MEMBRA ownership / revenue layer

```text
company equity
membership interests
SAFEs
revenue share agreements
regulated investment product
private investor agreement
DAO governance with legal wrapper
```

This layer should not be casually launched as a public token without legal review.

## Chat pool schema

```json
{
  "schema": "membra.chat_pool.v0",
  "chat_id": "CHAT-YYYYMMDD-000001",
  "pool_id": "POOL-YYYYMMDD-000001",
  "creator_id": "Joseph_Skrobynets_overandor",
  "artifact_hash_sha256": "<sha256>",
  "qr_page_url": "<url>",
  "chain": "solana-devnet|solana-mainnet-beta",
  "payment_rails": ["solana", "stripe"],
  "pool_purpose": "support|access|bounty|license|sponsor|notary_credit",
  "not_investment": true,
  "no_profit_guarantee": true,
  "no_memra_ownership_rights": true,
  "official_money_usd": "0.00_until_settled_payment"
}
```

## Protocol fee receipt schema

```json
{
  "schema": "membra.protocol_fee_receipt.v0",
  "pool_id": "POOL-YYYYMMDD-000001",
  "payment_receipt_id": "RCPT-YYYYMMDD-000001",
  "gross_amount": "<amount>",
  "currency": "USD|SOL|USDC",
  "platform_fee_percent": 10,
  "platform_fee_amount": "<amount>",
  "creator_amount": "<amount>",
  "contributor_amount": "<amount>",
  "processor_fee_amount": "<amount>",
  "settlement_status": "pending|settled|refunded|disputed",
  "receipt_sha256": "<sha256>"
}
```

## Revenue model without securities language

MEMBRA may earn revenue from:

```text
SaaS subscriptions
platform fees
notary review credits
artifact publishing credits
GitHub/IPFS anchoring credits
QR gateway fees
Stripe checkout fees
marketplace listing fees
sponsor campaign fees
enterprise proof-stream licenses
API usage
```

Public users may receive:

```text
badges
access
service credits
creator payouts from their own pools
contributor payouts for verified work
bounty payments
license payments
support receipts
```

Do not call public users "owners of all MEMBRA revenue" unless legally structured.

## If MEMBRA wants real ownership token later

Required steps:

```text
1. Form legal entity or legal wrapper.
2. Define equity/revenue rights.
3. Determine jurisdiction.
4. Obtain securities counsel.
5. Determine registration/exemption path.
6. Create investor disclosures.
7. Implement KYC/AML where required.
8. Restrict transfers if required.
9. Separate treasury accounting.
10. Publish audited or reviewable fee/revenue records.
```

## UI language

Use:

```text
Support this chat pool
Fund this proof capsule
Buy access/service credits
Sponsor this artifact
Contribute to this bounty
Protocol fee
Creator payout
Contributor reward
Settlement receipt
```

Avoid:

```text
Invest in this chat for profit
Own MEMBRA by buying token
Receive revenue from all chats automatically
Guaranteed yield
Passive income from others' chats
Official ChatGPT payout
```

## TikTok-safe explanation

```text
Each MEMBRA chat can become a QR-funded idea pool.
People can support, sponsor, or fund tasks around that specific chat.
The pool pays the creator and contributors from real funded balances.
MEMBRA takes a disclosed protocol fee for the infrastructure.
MEMBRA ownership or revenue-share is a separate legal structure, not something we fake with a public token.
```

## One-sentence truth

MEMBRA can let people support and fund individual chats on Solana while MEMBRA earns disclosed protocol fees, but ownership of MEMBRA or revenue flow from all chats must be legally structured separately from public utility/support tokens.
