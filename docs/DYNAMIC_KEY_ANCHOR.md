# Dynamic Key Anchor — Public-Only Safe Design

**Status:** design/specification only  
**Anchor identity:** `overandor` / Joseph Skrobynets  
**Purpose:** create a reproducible public wallet/key anchor without leaking private-key material online.

## Hard rule

Never post any private key, seed phrase, wallet JSON, partial private key, Shamir share, mnemonic word, or signing secret online.

A split key is still secret material. Posting half of a key on TikTok, GitHub, X, Telegram, Discord, or any other public platform is unsafe and can permanently compromise the wallet, especially if the other half is later photographed, leaked, guessed, weakly generated, or recovered from device backups.

## Safe version of the idea

The first public layer should contain only:

1. Public wallet address.
2. Public key, if the chain exposes one.
3. SHA-256 hash of the complete secret share package.
4. SHA-256 hash commitments for each offline share.
5. Public metadata: timestamp, repo URL, issue URL, chain, cluster, and anchor purpose.
6. Optional signed message from the wallet proving control.

The offline layer should contain:

1. The mnemonic or private key, generated locally.
2. Shamir secret shares or another threshold-secret scheme.
3. Encrypted backups stored offline.
4. Recovery instructions printed on paper or stored in an offline password manager.

## Recommended architecture

```text
Local machine / hardware wallet
    -> generate wallet locally
    -> export public address only
    -> create secret-share package offline
    -> hash each share offline
    -> publish only hash commitments
    -> optionally sign a public message
    -> anchor public address + hashes on GitHub/IPFS/devnet/mainnet
```

## Public anchor payload template

```text
DYNAMIC_KEY_ANCHOR:v1
identity=Joseph_Skrobynets_overandor
wallet_chain=<solana|ethereum|bitcoin|other>
wallet_cluster=<devnet|mainnet|testnet>
public_address=<PUBLIC_ADDRESS_ONLY>
public_key=<PUBLIC_KEY_IF_AVAILABLE>
secret_package_sha256=<SHA256_OF_FULL_OFFLINE_SECRET_PACKAGE>
share_1_commitment_sha256=<SHA256_OF_OFFLINE_SHARE_1>
share_2_commitment_sha256=<SHA256_OF_OFFLINE_SHARE_2>
threshold=<M_OF_N>
github_repo=overandor/chat-pipeline
github_issue=https://github.com/overandor/chat-pipeline/issues/1
prior_discussion_sha256=123d6b7d949c63962b5f382efd8e73bb9fa7cf6d42db033d4e0c634ed691dc28
official_money_usd=0.00
```

## Solana local wallet creation

Run locally only:

```bash
solana config set --url devnet
solana-keygen new --outfile ./dynamic-anchor-devnet.json
solana address -k ./dynamic-anchor-devnet.json
```

The output of `solana address` is public. The JSON file is private and must not be posted.

Optional proof-of-control signature:

```bash
solana-keygen pubkey ./dynamic-anchor-devnet.json
solana sign-offchain-message -k ./dynamic-anchor-devnet.json \
  "DYNAMIC_KEY_ANCHOR:v1:overandor:123d6b7d949c63962b5f382efd8e73bb9fa7cf6d42db033d4e0c634ed691dc28"
```

## Ethereum local wallet creation

Run locally only with Foundry:

```bash
cast wallet new
```

Publish only the address. Do not post the private key.

Optional proof-of-control signature:

```bash
cast wallet sign --private-key <PRIVATE_KEY_LOCAL_ONLY> \
  "DYNAMIC_KEY_ANCHOR:v1:overandor:123d6b7d949c63962b5f382efd8e73bb9fa7cf6d42db033d4e0c634ed691dc28"
```

## Secret splitting guidance

Use a real threshold scheme, not manual string splitting.

Recommended: Shamir Secret Sharing with threshold `2-of-3` or `3-of-5`.

Public platforms should receive only commitments:

```bash
sha256sum share-1.txt
sha256sum share-2.txt
sha256sum share-3.txt
```

Post the hashes, not the shares.

## TikTok-safe post text

```text
Dynamic Key Anchor v1
Public wallet only: <PUBLIC_ADDRESS>
GitHub anchor: https://github.com/overandor/chat-pipeline/issues/1
Discussion SHA-256: 123d6b7d949c63962b5f382efd8e73bb9fa7cf6d42db033d4e0c634ed691dc28
Secret shares are offline. No private keys posted.
Official money: $0.00. Proof layer only.
```

## Boundary statement

This document is not a wallet, private key, seed phrase, financial instrument, invoice, payout claim, or legal claim. It is a public-only proof architecture for anchoring identity, hashes, and future wallet-control proofs while keeping all secret material offline.
