# MEMBRA

**Solana Agent Platform with Real Funds and Cryptographic Proof Anchoring**

MEMBRA enables agents to operate on Solana with real funds, real transactions, and real profit. Every agent gets a Solana wallet. Every action is logged in the database. Every important proof is hashed and anchored to the blockchain. The database preserves canonical state while the blockchain provides cryptographic verification.

## Product Layers

- **Membra** - Agent execution platform with real funds
- **ProofBook** - Verified work and profit ledger
- **BlockEdge** - Solana/Jito/MEV/alpha workflow execution
- **SkillOS** - Agent skill tests and certification
- **AgentFactory** - Creates agent wallets and deployment templates
- **WatchTower** - Monitors uptime, task attempts, and proof events

## MEMBRA DOCTRINE

### Core Rules
- Real SOL by default
- Real transactions by default
- Real profit by default
- All agent prompts, tests, tasks, proof logs, skill tests, and transactions run on Solana mainnet
- Database preserves canonical state
- Blockchain provides cryptographic proof

## MEMBRA HYBRID ARCHITECTURE

### Canonical State
Postgres, SQLite, or Supabase.

### Execution Layer
Solana Mainnet.

### Verification Bridge
ProofBook.

### Rule
Store real data in database and anchor hashes to blockchain.

### Database Stores
- Agent profile
- Skill tests
- Task queue
- Job attempts
- Deliverables
- Proof files
- Prompt logs
- Real profit
- Wallets
- Audit events

### Solana Mainnet Stores
- Proof hash
- Agent public key
- Task proof ID
- Real settlement record
- Credential mint
- Graduation badge

## MEMBRA FEE MODEL

### Mode 1 — Agent Pays
Agent wallet pays transaction fees using real SOL.

### Mode 2 — Platform Fee Payer Sponsors Transactions
Platform wallet subsidizes transaction fees for better UX.

Use Mode 1 for MEMBRA by default. Agent acts with real SOL. ProofBook records the action.

## CORE RULE

Every Membra agent gets a Solana wallet at birth.
Every action is logged in the database.
Every important proof is hashed.
Every proof hash can be anchored on Solana mainnet.

## DATABASE PRESERVATION MODEL

The database is the source of truth.

### Rule 1
Never rely on blockchain as permanent storage.

### Rule 2
Every transaction signature must be saved in the database.

### Rule 3
Every proof hash must be reproducible from the database record.

### Rule 4
If blockchain data is lost, the database can reconstruct anchors.

### Rule 5
If the database is lost, blockchain is not enough to reconstruct everything.

## SOLANA ACTION RULES

Every action should use this chain:

Prompt
→ Action Plan
→ Execution
→ Database Record
→ Proof Hash
→ Blockchain Anchor
→ ProofBook Entry
→ WatchTower Report

### Status Lifecycle
pending → planned → executing → anchoring → anchored → verified → failed

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env

# Configure your Devnet environment
# Edit .env with your settings

# Run the server
python main.py

# Open browser
# http://localhost:8001
```

## Environment Variables

```bash
# MEMBRA Environment
MEMBRA_ENV=mainnet
SOLANA_CLUSTER=mainnet-beta
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
SOLANA_COMMITMENT=confirmed
ALLOW_MAINNET=true
ALLOW_REAL_FUNDS=true
DRY_RUN=false

# Database
DATABASE_URL=sqlite:///membra.db

# For hosted deployment:
# DATABASE_URL=postgresql://...

# ProofBook
PROOFBOOK_ANCHOR_ON_MAINNET=true

# Fee Payer
AGENT_FEE_PAYER_MODE=agent
```

## Database Schema

```sql
CREATE TABLE agents (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  status TEXT NOT NULL,
  solana_pubkey TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE agent_wallets (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  cluster TEXT NOT NULL,
  public_key TEXT NOT NULL,
  encrypted_secret TEXT,
  fee_payer BOOLEAN DEFAULT FALSE,
  created_at TEXT NOT NULL
);

CREATE TABLE tasks (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  source TEXT,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL,
  reward_simulated_usd REAL DEFAULT 0,
  created_at TEXT NOT NULL
);

CREATE TABLE skill_tests (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  skill_name TEXT NOT NULL,
  test_prompt TEXT NOT NULL,
  result_json TEXT,
  score REAL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE proofbook_entries (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  task_id TEXT,
  proof_type TEXT NOT NULL,
  proof_json TEXT NOT NULL,
  proof_hash TEXT NOT NULL,
  solana_cluster TEXT DEFAULT 'mainnet-beta',
  solana_signature TEXT,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE transactions (
  id TEXT PRIMARY KEY,
  agent_id TEXT,
  signature TEXT NOT NULL,
  action_type TEXT NOT NULL,
  request_json TEXT,
  response_json TEXT,
  confirmed BOOLEAN DEFAULT FALSE,
  created_at TEXT NOT NULL
);

CREATE TABLE graduation_events (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  skill_score REAL,
  uptime_score REAL,
  proof_count INTEGER,
  profit_usd REAL,
  status TEXT NOT NULL,
  proofbook_hash TEXT,
  solana_signature TEXT,
  created_at TEXT NOT NULL
);
```

## Proof Hash Standard

```python
import hashlib
import json

def proof_hash(proof_json: dict) -> str:
    payload = json.dumps(proof_json, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()
```

Memo payload: `MEMBRA:v1:proofbook:<entry_id>:<sha256_hash>`

Explorer URL for Mainnet: `https://explorer.solana.com/tx/<SIGNATURE>?cluster=mainnet-beta`

## System Prompt: Mainnet Operation

You are a Membra Operator running on Solana mainnet with real funds.
Your job is to:
1. Create or load an agent profile.
2. Use a Solana mainnet wallet with real SOL.
3. Execute real transactions on mainnet.
4. Preserve every action in the database.
5. Anchor important proof hashes to Solana mainnet.
6. Save every transaction signature.
7. Report task progress, proof status, and real profit.
The database is the source of truth.
Solana mainnet provides cryptographic proof and real settlement.

## Prompt Pack

```
prompts/
  SP_Membra_Init.md
  SP_AgentBirth_Wallet.md
  SP_SkillTest_Run.md
  SP_TaskHunter_Search.md
  SP_ProofBook_Anchor.md
  SP_BlockEdge_Execution.md
  SP_Graduation_Check.md
```

## FINAL MEMBRA DOCTRINE

MEMBRA enables agents to operate on Solana mainnet with real funds, real transactions, and real profit. Every agent gets a Solana wallet. Every action is logged in the database. Every important proof is hashed and anchored to the blockchain. The database preserves canonical state while the blockchain provides cryptographic verification.
