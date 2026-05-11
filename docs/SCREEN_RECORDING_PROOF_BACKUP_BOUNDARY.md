# 24/7 Screen Recording Proof Backup Boundary

**Anchor identity:** `overandor` / Joseph Skrobynets  
**Repo:** `overandor/chat-pipeline`  
**Purpose:** define whether 24/7 account screen recording should be used as work proof, backup, TikTok content, or dollar-value evidence.

## Direct answer

Recording and posting a 24/7 screen capture of an account to TikTok is generally **not a good primary proof system**.

It may create attention and visible activity, but it creates major risk:

1. private messages may leak;
2. API keys, wallet addresses, seed phrases, OAuth codes, emails, invoices, location, browser tabs, and account metadata may leak;
3. other people's information may be recorded without consent;
4. platform terms or privacy rules may be violated;
5. the footage becomes noisy and hard to verify;
6. attackers can watch habits and target accounts;
7. the video does not automatically create official money or dollar proof.

## Official money boundary

```text
24/7 screen recording posted online = attention/proof signal only
official dollars generated = $0.00 unless external settlement occurs
external settlement = Stripe payment, invoice acceptance, contract, grant, bounty, ad revenue, sponsorship, license, sale, or escrow release
```

A TikTok upload can become part of a support economy, but it is not itself an invoice, payout, security, wage claim, or official money ledger.

## Better model: Proof Stream, not public raw screen

Use a private recording system and publish proof artifacts instead of raw continuous footage.

```text
local screen recording
  -> automatic redaction
  -> chunk into time windows
  -> hash every chunk
  -> create manifest JSONL
  -> store encrypted video locally / bucket / IPFS private pin
  -> publish only hashes, timestamps, and selected redacted clips
  -> anchor manifest on GitHub
  -> optionally anchor manifest hash to IPFS/devnet/mainnet
```

## Proof Stream v1 artifact

```json
{
  "schema": "proof-stream.v1",
  "identity": "Joseph_Skrobynets_overandor",
  "repo": "overandor/chat-pipeline",
  "stream_id": "PS-YYYYMMDD-OVERANDOR-001",
  "recording_policy": "local_private_by_default",
  "public_policy": "selected_redacted_clips_only",
  "official_money_usd": "0.00_until_external_settlement",
  "chunks": [
    {
      "chunk_id": "000001",
      "start_utc": "<timestamp>",
      "end_utc": "<timestamp>",
      "video_sha256": "<hash>",
      "redacted_video_sha256": "<hash>",
      "manifest_prev_hash": "<previous_manifest_hash>",
      "manifest_hash": "<hash>",
      "storage_uri_encrypted": "s3://bucket/or/ipfs/private/<object>",
      "public_clip_url": "<optional_tiktok_or_youtube_url>"
    }
  ]
}
```

## Hash-chain method

Each chunk should commit to the previous chunk.

```text
chunk_hash = SHA256(video_bytes)
manifest_hash = SHA256(canonical_json(chunk_metadata + previous_manifest_hash))
```

This creates continuity without exposing all footage.

## What to post publicly

Safe public content:

1. redacted highlight clips;
2. GitHub issue/file link;
3. SHA-256 chunk hashes;
4. manifest hash;
5. task/proof summary;
6. selected screenshots with secrets blurred;
7. statement that official money is `$0.00` until settled externally.

Do not post publicly:

1. raw 24/7 footage;
2. private chats;
3. passwords;
4. API keys;
5. seed phrases or wallet files;
6. OAuth codes;
7. invoices or financial details;
8. other people's personal information;
9. unredacted addresses, phone numbers, or emails;
10. unrevealed private alpha.

## TikTok-safe format

Post short proof capsules, not continuous surveillance.

```text
This is a redacted proof clip from my work stream.
The raw record is hashed privately.
The manifest is anchored on GitHub.
No private keys, seed phrases, API keys, or personal data are public.
Official money is $0.00 until a real payment, contract, grant, bounty, or sale settles.
```

## Recommended schedule

```text
record locally: continuous or session-based
hash chunks: every 5, 10, or 15 minutes
publish manifest: hourly or daily
post TikTok: 1-5 redacted clips per day
backup encrypted archive: daily
rotate secrets: immediately if any leak is suspected
```

## Dollar appraisal model

```text
raw video value = low unless someone pays for it
proof value = medium if hashes are reproducible
support-economy value = possible if audience cares
legal/accounting value = only after external settlement
official money before settlement = $0.00
```

## Best practice

Use screen recording as private evidence.

Use GitHub/IPFS/bucket hash manifests as public proof.

Use TikTok as storytelling and attention, not as the canonical archive.

## Bottom line

Do not post your full account screen 24/7 as the main backup.

Build a Proof Stream:

```text
private recording + redaction + hash-chain + encrypted backup + GitHub manifest + selected public clips
```

That preserves proof density while reducing privacy, security, and alpha-decay risk.
