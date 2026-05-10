# Chat Pipeline

**Full Evaluation System with Blockchain, IPFS, GitHub Integration & Neomorphic Dashboard**

Transform raw chat logs into deployable services with complete provenance tracking including Merkle trees, blockchain anchoring, IPFS storage, GitHub repository creation, and comprehensive appraisal.

## What It Does

- **Merkle Provenance**: Hash chat content, generate Merkle tree, track artifacts with cryptographic proofs
- **Blockchain Integration**: Upload Merkle root to blockchain with transaction hash and explorer links
- **IPFS Storage**: Upload chat artifacts to IPFS with CID and gateway URLs
- **GitHub Integration**: Create repositories and files with chat appraisal data
- **Chat Appraisal**: Analyze chat complexity, value, and quality with USD estimation
- **Base64 Encoding**: Convert chat to base64 for storage and transmission
- **Neomorphic Dashboard**: Modern soft UI design with shadows and depth
- **Visual Pipeline**: Animated extract-transform-load pipeline showing files moving through stages
- **API Service**: RESTful endpoints for chat processing and file uploads
- **Chart Uploads**: Support for MD and ZIP file uploads
- **Real-time Metrics**: Display processing time, chunk count, estimated value

## Pipeline Stages

1. **Extract**: Parse and extract chat content, create Merkle tree
2. **Transform**: Apply transformations and base64 encoding
3. **Load**: Upload artifacts to IPFS
4. **Analyze**: Appraise chat value and compute metrics
5. **Deploy**: Upload to blockchain and optionally create GitHub repository

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Open browser
# http://localhost:8001
```

## Environment Variables (Optional)

```bash
# For blockchain integration
export ETHERSCAN_API_KEY="your_etherscan_key"

# For IPFS integration
export IPFS_API_URL="https://ipfs.infura.io:5001"
export IPFS_GATEWAY="https://ipfs.io/ipfs/"

# For art generation (choose one)
export REPLICATE_API_TOKEN="your_replicate_api_key"
# or
export OPENAI_API_KEY="your_openai_api_key"

# For Twilio-Telegram-LLM integration
export TWILIO_ACCOUNT_SID="your_twilio_account_sid"
export TWILIO_AUTH_TOKEN="your_twilio_auth_token"
export TWILIO_MESSAGING_SERVICE_SID="your_messaging_service_sid"
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export TELEGRAM_APPROVED_CHAT_ID="your_telegram_chat_id"
export HUGGINGFACE_API_KEY="your_huggingface_api_key"
export HUGGINGFACE_MODEL="meta-llama/Llama-2-7b-chat-hf"
export AUTO_REPLY="false"
export AUTO_REPLY_ALLOWLIST="+15551234567,+15557654321"
```

## API Endpoints

### `POST /api/process`
Process chat content through the full evaluation pipeline.

**Request:**
```json
{
  "chat_content": "Your chat content here...",
  "github_token": "ghp_xxxxx (optional)",
  "repo_name": "my-repo (optional)"
}
```

**Response:**
```json
{
  "chat_hash": "abc123...",
  "chat_base64": "base64encoded...",
  "merkle_root": "def456...",
  "chunk_count": 10,
  "timestamp": "2024-01-01T00:00:00",
  "size_bytes": 5000,
  "ipfs": {
    "cid": "Qm...",
    "gateway_url": "https://ipfs.io/ipfs/Qm...",
    "size_bytes": 5000,
    "filename": "chat.txt"
  },
  "blockchain": {
    "transaction_hash": "0x...",
    "block_number": 18234567,
    "network": "ethereum",
    "explorer_url": "https://etherscan.io/tx/0x...",
    "status": "confirmed"
  },
  "appraisal": {
    "word_count": 100,
    "char_count": 500,
    "complexity_score": 0.5,
    "value_score": 0.05,
    "estimated_value_usd": 2.5,
    "quality_rating": "C"
  },
  "github": {
    "repository": "https://github.com/user/repo",
    "file_url": "https://github.com/user/repo/blob/main/appraisal.json",
    "commit_sha": "abc123..."
  }
}
```

### `POST /api/upload`
Upload MD or ZIP files for processing.

**Request:** multipart/form-data with files

**Response:** Same as `/api/process`

### `GET /api/artifacts/{id}`
Retrieve artifacts by ID (demo placeholder).

## Integrations

### Merkle Provenance
- Chat is split into 1000-character chunks
- Each chunk is hashed with SHA-256
- Hashes are combined pairwise to build the tree
- Root hash provides cryptographic proof of content integrity
- Proofs can be generated for any chunk

### Blockchain Integration
- Merkle root is uploaded to blockchain
- Transaction hash generated and returned
- Block number and explorer URL provided
- Etherscan integration for verification
- Ethereum network (simulated in demo)

### Art Generation Integration
- Replicate API for Stable Diffusion XL (primary)
- OpenAI DALL-E as alternative
- Chat content converted to artistic prompts
- Base64 encoded image output
- Fallback description on API failure
- Requires REPLICATE_API_TOKEN or OPENAI_API_KEY environment variable
- Note: Replicate requires account credits; OpenAI requires valid API key

### IPFS Integration
- Chat content uploaded to IPFS
- Content Identifier (CID) generated
- Gateway URL for content retrieval
- Persistent decentralized storage
- Infura or local IPFS node support

### GitHub Integration
- Creates new repository with chat artifact
- Uploads appraisal.json with evaluation data
- Returns repository URL and file links
- Commit SHA for provenance
- Requires GitHub personal access token

### Chat Appraisal
- Word count and character count analysis
- Complexity score based on content length
- Value score for market estimation
- USD value estimation
- Quality rating (A/B/C tiers)

## Visual Features

- **Neomorphic Design**: Soft UI with shadows and depth
- **Animated Pipeline**: Files move through stages with smooth animations
- **Stage Indicators**: Visual progress through extract-transform-load
- **Real-time Metrics**: Size, chunks, time, estimated value displayed
- **Integration Cards**: Separate sections for each integration
- **Drag & Drop**: Upload files by dragging to upload zone
- **Responsive**: Works on desktop and mobile

## Use Cases

- **Chat-to-Service**: Transform AI chat logs into deployable microservices
- **Provenance Tracking**: Cryptographic proof of content origin with blockchain
- **Decentralized Storage**: IPFS for permanent artifact storage
- **Repository Management**: GitHub integration for version control
- **Value Appraisal**: Estimate chat content value for monetization
- **Pipeline Visualization**: Monitor data flow through processing stages
- **Batch Processing**: Upload multiple files for batch analysis
- **API Integration**: Programmatic access via REST endpoints

## Architecture

```
main.py (FastAPI dashboard)
├── MerkleTree (Provenance system)
├── BlockchainIntegration (Blockchain anchoring)
├── IPFSIntegration (Decentralized storage)
├── GitHubIntegration (Repository management)
├── ChatAppraiser (Value evaluation)
├── ChatPipeline (Orchestration engine)
├── PipelineStage (Stage management)
└── Neomorphic Dashboard (Frontend)
```

## Twilio-Telegram-LLM Integration

### Overview

The chat pipeline now includes a powerful SMS-to-LLM integration with human approval workflow:

1. **User texts your Twilio number**
2. **Hugging Face LLM generates a draft reply**
3. **Two modes of operation:**
   - **Auto-reply mode**: Allowlisted numbers get automatic LLM replies
   - **Human approval mode**: Drafts sent to Telegram for approval before sending

### Flow Diagram

```
Person texts Twilio number
        ↓
Twilio webhook → /twilio/inbound
        ↓
Hugging Face LLM drafts reply
        ↓
┌───────────────────────┬───────────────────────┐
│  AUTO_REPLY=true      │  AUTO_REPLY=false     │
│  + in allowlist       │  (default)             │
├───────────────────────┼───────────────────────┤
│ Auto-send via Twilio  │ Send to Telegram       │
│                       │ for approval           │
│                       │                       │
│                       │ /send <id> → Approve  │
│                       │ /reject <id> → Reject │
│                       │                       │
│                       │ Approved → Send via    │
│                       │ Twilio                │
└───────────────────────┴───────────────────────┘
```

### Setup

1. **Configure Twilio**:
   - Set your Twilio number's webhook URL to: `https://YOUR_DEPLOYED_DOMAIN/twilio/inbound`
   - Get your Account SID, Auth Token, and Messaging Service SID from Twilio console

2. **Configure Telegram**:
   - Create a bot via @BotFather
   - Get your bot token
   - Start a chat with your bot and get the chat ID (use @userinfobot to find your ID)
   - Set your bot's webhook URL to: `https://YOUR_DEPLOYED_DOMAIN/telegram/webhook`

3. **Configure Hugging Face**:
   - Get an API token from https://huggingface.co/settings/tokens
   - Choose a model (default: meta-llama/Llama-2-7b-chat-hf)

4. **Set environment variables** (see .env.example)

### Usage

**Auto-reply mode**:
```bash
export AUTO_REPLY=true
export AUTO_REPLY_ALLOWLIST="+15551234567,+15557654321"
```
Allowlisted numbers get automatic LLM replies.

**Human approval mode** (default):
```bash
export AUTO_REPLY=false
```
All messages require Telegram approval:
- `/send <message_id>` - Approve and send
- `/reject <message_id>` - Reject the draft

### Webhook Endpoints

- `POST /twilio/inbound` - Receives SMS from Twilio
- `POST /telegram/webhook` - Handles Telegram approval commands

## Future Expansions

- Real blockchain deployment (web3.py integration)
- Real IPFS node connection (ipfs-http-client)
- Persistent artifact storage (database)
- Merkle proof verification endpoint
- Advanced pipeline stages (ML inference, NLP)
- Real-time WebSocket updates
- Multi-user workspaces
- Pipeline orchestration (DAG support)
- Service deployment automation
- NFT minting from chat artifacts
- Tokenization of appraised content
- Alternative art generation APIs (Stability AI, Replicate)
- Real-time art generation with progress indicators
- Multi-language support for LLM integration
- SMS conversation history and context tracking
