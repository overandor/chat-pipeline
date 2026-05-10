-- MEMBRA Database Schema
-- The database is the source of truth.
-- Solana mainnet stores proof anchors, not the complete application database.

-- Agents table: stores agent profiles
CREATE TABLE IF NOT EXISTS agents (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  status TEXT NOT NULL,
  solana_pubkey TEXT NOT NULL,
  created_at TEXT NOT NULL
);

-- Agent wallets table: stores wallet information per cluster
CREATE TABLE IF NOT EXISTS agent_wallets (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  cluster TEXT NOT NULL,
  public_key TEXT NOT NULL,
  encrypted_secret TEXT,
  fee_payer BOOLEAN DEFAULT FALSE,
  created_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- Tasks table: stores task queue and job attempts
CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  source TEXT,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL,
  reward_usd REAL DEFAULT 0,
  created_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- Skill tests table: stores skill tests and scoring
CREATE TABLE IF NOT EXISTS skill_tests (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  skill_name TEXT NOT NULL,
  test_prompt TEXT NOT NULL,
  result_json TEXT,
  score REAL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- ProofBook entries table: stores proof hashes and mainnet anchors
CREATE TABLE IF NOT EXISTS proofbook_entries (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  task_id TEXT,
  proof_type TEXT NOT NULL,
  proof_json TEXT NOT NULL,
  proof_hash TEXT NOT NULL,
  solana_cluster TEXT DEFAULT 'mainnet-beta',
  solana_signature TEXT,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id),
  FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- Transactions table: stores all mainnet transaction signatures
CREATE TABLE IF NOT EXISTS transactions (
  id TEXT PRIMARY KEY,
  agent_id TEXT,
  signature TEXT NOT NULL,
  action_type TEXT NOT NULL,
  request_json TEXT,
  response_json TEXT,
  confirmed BOOLEAN DEFAULT FALSE,
  created_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- Graduation events table: stores graduation records
CREATE TABLE IF NOT EXISTS graduation_events (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  skill_score REAL,
  uptime_score REAL,
  proof_count INTEGER,
  profit_usd REAL,
  status TEXT NOT NULL,
  proofbook_hash TEXT,
  solana_signature TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agent_wallets_agent_id ON agent_wallets(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_wallets_cluster ON agent_wallets(cluster);
CREATE INDEX IF NOT EXISTS idx_tasks_agent_id ON tasks(agent_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_skill_tests_agent_id ON skill_tests(agent_id);
CREATE INDEX IF NOT EXISTS idx_skill_tests_status ON skill_tests(status);
CREATE INDEX IF NOT EXISTS idx_proofbook_entries_agent_id ON proofbook_entries(agent_id);
CREATE INDEX IF NOT EXISTS idx_proofbook_entries_task_id ON proofbook_entries(task_id);
CREATE INDEX IF NOT EXISTS idx_proofbook_entries_proof_hash ON proofbook_entries(proof_hash);
CREATE INDEX IF NOT EXISTS idx_proofbook_entries_solana_signature ON proofbook_entries(solana_signature);
CREATE INDEX IF NOT EXISTS idx_transactions_agent_id ON transactions(agent_id);
CREATE INDEX IF NOT EXISTS idx_transactions_signature ON transactions(signature);
CREATE INDEX IF NOT EXISTS idx_graduation_events_agent_id ON graduation_events(agent_id);
CREATE INDEX IF NOT EXISTS idx_graduation_events_status ON graduation_events(status);
