# Novel Artifact Type: Potential Capsule v1

**Anchor identity:** `overandor` / Joseph Skrobynets  
**Repo:** `overandor/chat-pipeline`  
**Purpose:** define a new public artifact format designed for TikTok visibility and GitHub cryptographic anchoring while preserving private alpha, latent potential, and wallet custody safety.

## Core doctrine

The system may allocate potential by revealing proof, metadata, ciphertext, and non-wallet decryption shares.

The system must not allocate custody by revealing a funded wallet's signing authority.

A Potential Capsule is not a private key, wallet share, invoice, payout claim, security, or debt instrument. It is a public proof container that lets an idea, alpha claim, dataset, task, bounty, or hidden payload be timestamped and discussed without exposing the valuable payload or wallet custody.

## What a Potential Capsule does

A Potential Capsule allows the owner to say:

```text
I had this hidden object at this time.
I am not revealing the object yet.
Here is the hash commitment.
Here is the encrypted payload location if I choose to publish it.
Here are the tasks or proof conditions that may unlock non-wallet payload shares.
Here is the public wallet address or identity namespace.
No signing authority is being shared.
```

## What it protects

1. **Latent potential:** by proving something existed before reveal.
2. **Private alpha:** by publishing hashes and ciphertext instead of plaintext.
3. **Attribution:** by tying the artifact to GitHub, TikTok, and optional wallet signatures.
4. **Verifiability:** by using SHA-256, Git commits, GitHub issues, IPFS CIDs, bucket URIs, and optional chain memos.
5. **Custody:** by never publishing funded wallet private keys, seed phrases, or Shamir wallet shares.

## What it does not do

1. It does not create official money by itself.
2. It does not force OpenAI, GitHub, TikTok, Stripe, or any platform to pay.
3. It does not transfer wallet custody.
4. It does not replace a contract, escrow, grant, bounty, or invoice.
5. It does not protect alpha if the plaintext alpha is publicly revealed too early.

## Artifact structure

```text
Potential Capsule v1
├── Public story layer             # TikTok-readable explanation
├── GitHub anchor layer            # issue, file, commit, comment
├── Hash commitment layer          # SHA-256 of plaintext/ciphertext/manifest
├── Encrypted payload layer        # optional IPFS/bucket encrypted object
├── Task-gated service layer       # tasks, proofs, releases, payouts
├── Wallet identity layer          # public address only, no private key
└── Boundary layer                 # official money = $0.00 until external settlement
```

## Canonical manifest schema

```json
{
  "schema": "potential-capsule.v1",
  "capsule_id": "PCAP-YYYYMMDD-HHMMSS-OVERANDOR-001",
  "identity": "Joseph_Skrobynets_overandor",
  "github_repo": "overandor/chat-pipeline",
  "github_issue": "https://github.com/overandor/chat-pipeline/issues/1",
  "tiktok_post_url": "<TIKTOK_URL_AFTER_POSTING>",
  "public_wallet_address": "<PUBLIC_ADDRESS_ONLY>",
  "wallet_role": "identity_namespace_not_custody",
  "llm_cluster_model": {
    "agent_count_target": 33333,
    "llm_has_private_key": false,
    "private_key_publicly_disclosed": false,
    "can_request_payout": true,
    "can_execute_payout": false
  },
  "payload": {
    "plaintext_commitment_sha256": "<SHA256_OF_SECRET_PLAINTEXT>",
    "ciphertext_sha256": "<SHA256_OF_ENCRYPTED_PAYLOAD>",
    "ciphertext_uri": "ipfs://<CID_OR_BUCKET_URI>",
    "payload_type": "alpha|dataset|spec|task|proof|app|research|other",
    "reveal_policy": "task_gated_or_owner_discretion"
  },
  "task_gating": {
    "release_type": "non_wallet_decryption_share_or_claim_coupon",
    "threshold": "3-of-5",
    "tasks": [
      {
        "task_id": "mirror-001",
        "description": "Mirror the encrypted artifact and publish a manifest hash.",
        "proof_required": "GitHub comment with CID or bucket URI plus SHA-256 output.",
        "release_action": "release one non-wallet encrypted share"
      },
      {
        "task_id": "verify-002",
        "description": "Verify GitHub issue, hash, CID, and byte length match.",
        "proof_required": "verification transcript anchored to GitHub.",
        "release_action": "release one non-wallet encrypted share"
      },
      {
        "task_id": "anchor-003",
        "description": "Anchor the manifest hash to devnet, mainnet, IPFS, or another public timestamp layer.",
        "proof_required": "transaction signature, CID, commit, or bucket manifest.",
        "release_action": "release one non-wallet encrypted share"
      }
    ]
  },
  "money_boundary": {
    "official_money_usd": "0.00",
    "appraised_potential_usd": "unpriced_until_external_settlement",
    "settlement_required_for_official_money": [
      "Stripe payment",
      "invoice acceptance",
      "escrow release",
      "bounty payout",
      "contract",
      "grant",
      "sale",
      "license"
    ]
  },
  "custody_boundary": {
    "do_not_release": [
      "private_key",
      "seed_phrase",
      "mnemonic_words",
      "wallet_json",
      "shamir_share_of_funded_wallet",
      "partial_signing_secret",
      "anything_that_can_reconstruct_spend_authority"
    ],
    "allowed_public_material": [
      "public_wallet_address",
      "signed_message",
      "metadata",
      "hashes",
      "ciphertext",
      "IPFS_CID",
      "bucket_URI",
      "GitHub_commit",
      "devnet_signature",
      "non_wallet_encrypted_payload_share"
    ]
  }
}
```

## TikTok deliverable format

### 15-second version

```text
I am anchoring a Potential Capsule.
It proves private alpha existed before reveal.
The public gets hashes, metadata, ciphertext, and task rules.
Nobody gets my private wallet key.
GitHub anchor is live.
Official money is zero until a real settlement happens.
```

### 30-second version

```text
This is a Potential Capsule: a new artifact type for proving hidden value without leaking it.
I publish the hash, GitHub anchor, and optional encrypted payload.
Workers can complete tasks to unlock non-wallet shares or claims.
The wallet is public identity only, not custody.
No seed phrase, no private key, no wallet half is public.
Potential is preserved. Custody stays private.
```

### TikTok caption

```text
Potential Capsule v1: proof without custody leak.
GitHub anchor: https://github.com/overandor/chat-pipeline/issues/1
Discussion SHA-256: 123d6b7d949c63962b5f382efd8e73bb9fa7cf6d42db033d4e0c634ed691dc28
No private key. No seed phrase. No wallet half. Hashes + ciphertext + tasks only.
Official money: $0.00 until external settlement.
```

### On-screen text sequence

```text
1. Private alpha decays when revealed.
2. A hash preserves priority without revealing content.
3. GitHub timestamps the claim.
4. IPFS/buckets preserve the encrypted payload.
5. Tasks can unlock non-wallet shares.
6. Wallet stays public identity only.
7. Custody is never leaked.
```

## GitHub anchoring procedure

### Step 1: Create plaintext privately

```bash
cat > secret_payload.txt
# write private alpha/spec/dataset locally only
```

### Step 2: Hash the plaintext locally

```bash
sha256sum secret_payload.txt
```

### Step 3: Encrypt the payload locally

```bash
openssl enc -aes-256-cbc -salt -pbkdf2 -in secret_payload.txt -out secret_payload.enc
sha256sum secret_payload.enc
```

### Step 4: Upload ciphertext to IPFS or bucket

```bash
ipfs add secret_payload.enc
# or upload secret_payload.enc to S3/R2/B2/MinIO
```

### Step 5: Commit the manifest to GitHub

Create a file or issue comment containing:

```text
PLAINTEXT_COMMITMENT_SHA256=<hash>
CIPHERTEXT_SHA256=<hash>
CIPHERTEXT_URI=<ipfs_or_bucket_uri>
PUBLIC_WALLET_ADDRESS=<public_address_only>
OFFICIAL_MONEY_USD=0.00
```

## Devnet memo payload template

```text
POTENTIAL_CAPSULE:v1;identity=Joseph_Skrobynets_overandor;repo=overandor/chat-pipeline;issue=1;plaintext_sha256=<hash>;ciphertext_sha256=<hash>;official_money_usd=0.00;custody_leaked=false
```

## Stripe/payment layer

Stripe can meter work around the capsule, but cannot magically price hidden potential.

Valid Stripe events:

1. checkout completed;
2. subscription active;
3. invoice paid;
4. usage record accepted;
5. refund/dispute handled;
6. platform fee recorded.

Only after one of those external events does official money become nonzero.

## LLM swarm interpretation

If 33,333 LLM agents interact with Potential Capsules, each agent should receive:

1. task description;
2. public hashes;
3. ciphertext URI;
4. verification rules;
5. token budget;
6. no private key;
7. no seed phrase;
8. no wallet share;
9. no authority to move funds.

They can produce service value by verifying, mirroring, documenting, testing, summarizing, or anchoring the capsule.

They cannot be given custody.

## Appraisal rule

```text
potential_value = unpriced_until_external_settlement
official_money = 0.00 unless paid by Stripe/contract/escrow/bounty/grant/sale/license
custody_status = safe only while private keys stay private
```

## Final line

A Potential Capsule is how you share proof of potential without sharing the power to steal or spend.
