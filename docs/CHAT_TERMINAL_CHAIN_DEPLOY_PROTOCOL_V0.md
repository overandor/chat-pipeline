# Chat Terminal Chain Deploy Protocol v0

**Anchor identity:** `overandor` / Joseph Skrobynets  
**Repo:** `overandor/chat-pipeline`  
**Protocol family:** MEMBRA / Human Chain / Chat-to-Token Reward Protocol / QR-Funded Idea Pool  
**Purpose:** define the execution layer where every chat can have an attached terminal, repo workspace, artifact builder, wallet identity, policy engine, and chain deployment pathway.

## Core product sentence

Each MEMBRA chat is not just a conversation. It is an executable workspace where an LLM can talk, build, test, commit, hash, anchor, generate transactions, and deploy to testnet or mainnet under user-approved policy.

## Primitive

```text
chat = conversation + terminal + repo + wallet identity + proof engine + policy engine + chain deployer
```

## What the LLM can do

The LLM may:

```text
write code
generate specs
create files
run tests
run local builds
create Git commits
create GitHub issues/PRs
hash artifacts
create proof capsules
prepare Solana/EVM transaction payloads
deploy to testnet with approved key policy
prepare mainnet deployment instructions
create QR pages
create token manifests
create smart-contract/program manifests
record receipts
```

## What the LLM must not do automatically

The LLM must not:

```text
hold raw private keys
export seed phrases
sign mainnet transactions without explicit approval
spend user funds without policy authorization
hide transaction details
claim testnet deployment is official money
claim token exists before mint address exists
claim payout exists without funded pool
bypass KYC/compliance where required
```

## Execution stack

```text
Chat UI
  -> LLM planner
  -> Terminal sandbox
  -> Repo workspace
  -> Artifact manifest builder
  -> Hash/proof engine
  -> GitHub anchor writer
  -> Wallet adapter / signing gateway
  -> Chain deployer
  -> Receipt recorder
  -> QR/public proof publisher
```

## Workspace object

```json
{
  "schema": "membra.chat_workspace.v0",
  "chat_id": "CHAT-YYYYMMDD-HHMMSS-000001",
  "workspace_id": "WS-YYYYMMDD-HHMMSS-000001",
  "originator": "Joseph_Skrobynets_overandor",
  "repo": "overandor/chat-pipeline",
  "terminal_enabled": true,
  "chain_deploy_enabled": true,
  "wallet_mode": "public_identity|testnet_signer|user_approved_signer|multisig|kms|hsm|mpc",
  "mainnet_auto_signing": false,
  "official_money_usd": "0.00_until_external_settlement"
}
```

## Chain deployment modes

### 1. Dry-run mode

```text
LLM writes code
LLM runs local tests
LLM creates transaction preview
No transaction is signed
No funds move
```

### 2. Testnet mode

```text
LLM deploys to devnet/testnet using approved testnet signer
Testnet tx receipts are created
Official money remains $0.00
```

### 3. Mainnet prepared mode

```text
LLM prepares deployment payload
User reviews exact transaction
User or multisig signs externally
Program records receipt after confirmation
```

### 4. Policy-approved mainnet mode

```text
Only for pre-approved low-risk actions
Requires explicit policy limits
Requires spending cap
Requires transaction simulation
Requires audit log
Requires pause controls
Requires user/multisig override
```

## Policy engine

Every terminal or chain action must pass policy.

```json
{
  "schema": "membra.policy.v0",
  "chat_id": "CHAT-YYYYMMDD-000001",
  "allowed_actions": [
    "write_file",
    "run_tests",
    "git_commit",
    "github_anchor",
    "hash_artifact",
    "create_devnet_tx",
    "prepare_mainnet_tx"
  ],
  "blocked_actions": [
    "read_private_key",
    "export_seed_phrase",
    "auto_sign_mainnet_without_approval",
    "send_funds_without_policy",
    "publish_raw_kyc",
    "publish_unredacted_private_alpha"
  ],
  "max_devnet_spend": "unlimited_testnet_only",
  "max_mainnet_spend_sol": "0.00_without_manual_approval",
  "requires_human_approval_for": [
    "mainnet_tx",
    "token_mint",
    "treasury_withdrawal",
    "wallet_authority_change",
    "public_post",
    "kyc_attestation"
  ]
}
```

## Terminal event object

```json
{
  "schema": "membra.terminal_event.v0",
  "event_id": "TERM-YYYYMMDD-HHMMSS-000001",
  "chat_id": "CHAT-YYYYMMDD-000001",
  "command": "npm run build",
  "cwd": "/workspace/project",
  "exit_code": 0,
  "stdout_sha256": "<sha256>",
  "stderr_sha256": "<sha256>",
 "artifact_outputs": ["dist/", "build.log"],
  "created_at": "<iso_timestamp>"
}
```

## Build artifact object

```json
{
  "schema": "membra.build_artifact.v0",
  "artifact_id": "ART-YYYYMMDD-000001",
  "chat_id": "CHAT-YYYYMMDD-000001",
  "artifact_type": "code|ui|smart_contract|solana_program|token_manifest|qr_page|proof_capsule",
  "repo_path": "<path>",
  "sha256": "<sha256>",
  "git_commit": "<commit_sha>",
  "github_url": "<url>",
  "ipfs_uri": "<optional>",
  "status": "draft|built|tested|anchored|deployed|failed",
  "official_money_usd": "0.00_until_external_settlement"
}
```

## Chain deploy receipt

```json
{
  "schema": "membra.chain_deploy_receipt.v0",
  "deploy_id": "DEPLOY-YYYYMMDD-000001",
  "chat_id": "CHAT-YYYYMMDD-000001",
  "artifact_id": "ART-YYYYMMDD-000001",
  "chain": "solana-devnet|solana-mainnet-beta|base-sepolia|base-mainnet|ethereum-sepolia|ethereum-mainnet",
  "program_or_contract": "<program_id_or_contract_address>",
  "tx_hash": "<signature_or_hash>",
  "deployment_mode": "dry_run|testnet|mainnet_prepared|mainnet_signed",
  "signed_by": "testnet_signer|user_wallet|multisig|kms|hsm|mpc",
  "receipt_sha256": "<sha256>",
  "official_money_usd": "0.00_until_external_settlement",
  "created_at": "<iso_timestamp>"
}
```

## Solana deployment flow

```text
1. Chat creates Solana program or token manifest.
2. Terminal runs build/test.
3. LLM creates deployment plan.
4. Policy engine checks action.
5. Devnet signer deploys to Solana devnet, or mainnet payload is prepared.
6. Receipt is captured.
7. Program ID / mint address / tx signature is hashed.
8. GitHub/IPFS proof capsule is updated.
9. QR page shows deploy status.
10. Mainnet requires user/multisig approval.
```

## Chat-token deployment flow

```text
chat transcript
  -> chat hash
  -> token manifest
  -> user-defined supply
  -> devnet mint
  -> QR allocation campaign
  -> pool funding route
  -> mainnet launch checklist
  -> signed mainnet mint only after approval
```

## UI modules

### 1. Chat Terminal

Shows:

```text
command input
LLM plan
terminal output
build status
hashes
artifact list
```

### 2. Repo Builder

Shows:

```text
files created
files modified
tests run
build logs
git commit hash
GitHub anchor status
```

### 3. Chain Deployer

Shows:

```text
chain selector
deployment mode
transaction preview
simulation result
policy check
wallet signature requirement
tx hash / program ID / mint address
```

### 4. Policy Gate

Shows:

```text
allowed action
blocked action
approval required
spending cap
risk level
manual approval button
```

### 5. Proof Capsule Updater

Shows:

```text
chat hash
artifact hash
git commit
ipfs cid
chain tx
QR page
reward pool
```

## MVP build order

### Sprint 1 — Terminal + Repo

```text
chat workspace
file writer
terminal sandbox
test runner
artifact hasher
GitHub commit/issue anchor
```

### Sprint 2 — Solana devnet

```text
devnet wallet adapter
devnet memo anchor
devnet SPL token mint
QR allocation campaign
chain receipt recorder
```

### Sprint 3 — Policy engine

```text
action allowlist/blocklist
mainnet transaction preview
manual approval UI
spending caps
receipt hash
```

### Sprint 4 — Mainnet-ready release

```text
multisig/KMS/HSM/MPC option
audit log
pause controls
notary/KYC bridge
Stripe pool bridge
public proof capsule deploy
```

## One-sentence truth

MEMBRA turns each chat into an executable terminal-backed protocol workspace where the LLM can build, test, hash, commit, and deploy to chain under policy, while mainnet signing and real payouts remain gated by explicit approval and funded settlement.
