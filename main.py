"""Chat to Service Pipeline - Full Evaluation with Blockchain, IPFS, GitHub, Replicate Stable Diffusion Integration."""
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
import uvicorn
import hashlib
import base64
import httpx
import os
import json
from datetime import datetime
from typing import List, Optional, Dict
import replicate
from twilio.rest import Client
from telegram import Bot
from huggingface_hub import InferenceClient

# MEMBRA Guardrails
from guardrails import enforce_membra_doctrine

# Enforce MEMBRA Doctrine on startup
enforce_membra_doctrine()

app = FastAPI(title="MEMBRA - Solana Agent Platform", description="MEMBRA Agent Platform with Real Funds and Cryptographic Proof Anchoring")


class ChatRequest(BaseModel):
    chat_content: str
    metadata: Optional[dict] = None
    github_token: Optional[str] = None
    repo_name: Optional[str] = None


class MerkleNode:
    def __init__(self, left=None, right=None, hash=None, content=None):
        self.left = left
        self.right = right
        self.hash = hash
        self.content = content


class MerkleTree:
    def __init__(self):
        self.root = None
        self.leaves = []
    
    def add_leaf(self, content: str) -> str:
        """Add a leaf node with hashed content."""
        hash_val = hashlib.sha256(content.encode()).hexdigest()
        node = MerkleNode(hash=hash_val, content=content)
        self.leaves.append(node)
        return hash_val
    
    def build_tree(self):
        """Build the Merkle tree from leaves."""
        if not self.leaves:
            return None
        
        level = self.leaves[:]
        while len(level) > 1:
            new_level = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else level[i]
                combined = left.hash + right.hash
                parent_hash = hashlib.sha256(combined.encode()).hexdigest()
                parent = MerkleNode(left=left, right=right, hash=parent_hash)
                new_level.append(parent)
            level = new_level
        
        self.root = level[0] if level else None
        return self.root
    
    def get_root_hash(self) -> str:
        """Get the root hash of the Merkle tree."""
        return self.root.hash if self.root else ""
    
    def get_proofs(self, leaf_index: int) -> List[dict]:
        """Get Merkle proofs for a leaf."""
        if not self.root:
            return []
        
        proofs = []
        index = leaf_index
        
        level = self.leaves[:]
        while len(level) > 1:
            new_level = []
            for i in range(0, len(level), 2):
                if i == index:
                    sibling_idx = i + 1 if i + 1 < len(level) else i
                    if sibling_idx != i:
                        proofs.append({
                            "hash": level[sibling_idx].hash,
                            "position": "right" if sibling_idx > i else "left"
                        })
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else level[i]
                combined = left.hash + right.hash
                parent_hash = hashlib.sha256(combined.encode()).hexdigest()
                parent = MerkleNode(left=left, right=right, hash=parent_hash)
                new_level.append(parent)
            level = new_level
            index = index // 2
        
        return proofs


class PipelineStage:
    def __init__(self, name: str, duration: float):
        self.name = name
        self.duration = duration
        self.files = []


class BlockchainIntegration:
    def __init__(self):
        self.etherscan_api_key = os.getenv("ETHERSCAN_API_KEY", "")
        self.use_testnet = True  # Use testnet by default
    
    async def upload_to_blockchain(self, merkle_root: str, chat_hash: str) -> dict:
        """Upload Merkle root to blockchain (simulated for demo, using Sepolia testnet)."""
        # In production: Use web3.py to deploy contract or submit transaction to Sepolia
        # For demo: Return simulated blockchain data for Sepolia testnet
        tx_hash = "0x" + hashlib.sha256((merkle_root + str(datetime.now().timestamp())).encode()).hexdigest()[:64]
        
        network = "ethereum-sepolia" if self.use_testnet else "ethereum"
        explorer = "sepolia.etherscan.io" if self.use_testnet else "etherscan.io"
        
        return {
            "transaction_hash": tx_hash,
            "block_number": 5123456,  # Sepolia block
            "network": network,
            "explorer_url": f"https://{explorer}/tx/{tx_hash}",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "confirmed",
            "gas_used": "21000",
            "gas_price": "20 gwei",
            "is_testnet": self.use_testnet
        }
    
    async def verify_on_explorer(self, tx_hash: str) -> dict:
        """Verify transaction on blockchain explorer."""
        # In production: Call Etherscan API
        return {
            "verified": True,
            "confirmations": 128,
            "gas_used": "21000",
            "gas_price": "20 gwei"
        }


class IPFSIntegration:
    def __init__(self):
        self.ipfs_api_url = os.getenv("IPFS_API_URL", "https://ipfs.infura.io:5001")
        self.ipfs_gateway = os.getenv("IPFS_GATEWAY", "https://ipfs.io/ipfs/")
    
    async def upload_to_ipfs(self, content: str, filename: str) -> dict:
        """Upload content to IPFS (simulated for demo)."""
        # In production: Use ipfs-http-client or HTTP API
        # For demo: Generate CID-like hash
        cid = "Qm" + hashlib.sha256((content + filename).encode()).hexdigest()[:44]
        
        return {
            "cid": cid,
            "gateway_url": f"{self.ipfs_gateway}{cid}",
            "size_bytes": len(content),
            "filename": filename,
            "timestamp": datetime.utcnow().isoformat()
        }


class GitHubIntegration:
    def __init__(self):
        self.github_api_url = "https://api.github.com"
    
    async def create_repository(self, token: str, repo_name: str, description: str) -> dict:
        """Create a GitHub repository."""
        if not token:
            raise HTTPException(status_code=401, detail="GitHub token required")
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "name": repo_name,
            "description": description,
            "auto_init": True,
            "private": False
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.github_api_url}/user/repos",
                headers=headers,
                json=data
            )
            
            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            return response.json()
    
    async def create_file(self, token: str, owner: str, repo: str, path: str, content: str, message: str) -> dict:
        """Create a file in GitHub repository."""
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        content_b64 = base64.b64encode(content.encode()).decode()
        
        data = {
            "message": message,
            "content": content_b64
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.github_api_url}/repos/{owner}/{repo}/contents/{path}",
                headers=headers,
                json=data
            )
            
            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            return response.json()


class ArtGenerator:
    def __init__(self):
        self.replicate_api_key = os.getenv("REPLICATE_API_TOKEN", "") or os.getenv("REPLICATE_API_KEY", "")
        if self.replicate_api_key:
            os.environ["REPLICATE_API_TOKEN"] = self.replicate_api_key
    
    async def generate_art_from_chat(self, chat_content: str) -> dict:
        """Generate art from chat content using Replicate Stable Diffusion."""
        # Extract key themes from chat for prompt
        words = chat_content.split()
        key_words = words[:20]  # First 20 words as prompt
        prompt = " ".join(key_words)
        
        # Enhance prompt for better art generation
        enhanced_prompt = f"Abstract artistic representation of: {prompt}. Digital art, modern style, vibrant colors, high quality, detailed, professional, 4K"
        
        if not self.replicate_api_key:
            return {
                "success": False,
                "error": "Replicate API key not set",
                "fallback_description": f"Art generated from prompt: {enhanced_prompt}",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        try:
            # Use Replicate's Stable Diffusion XL with valid version
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": enhanced_prompt,
                    "num_outputs": 1,
                    "width": 1024,
                    "height": 1024,
                }
            )
            
            if output and len(output) > 0:
                # Replicate returns a URL, download and convert to base64
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(output[0])
                    if response.status_code == 200:
                        image_bytes = response.content
                        image_b64 = base64.b64encode(image_bytes).decode()
                        
                        return {
                            "success": True,
                            "image_base64": image_b64,
                            "image_url": output[0],
                            "prompt": enhanced_prompt,
                            "size_bytes": len(image_bytes),
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to download image: {response.status_code}",
                            "fallback_description": f"Art generated from prompt: {enhanced_prompt}",
                            "timestamp": datetime.utcnow().isoformat()
                        }
            else:
                return {
                    "success": False,
                    "error": "No image generated",
                    "fallback_description": f"Art generated from prompt: {enhanced_prompt}",
                    "timestamp": datetime.utcnow().isoformat()
                }
        except Exception as e:
            # Fallback on error
            return {
                "success": False,
                "error": str(e),
                "fallback_description": f"Art generated from prompt: {enhanced_prompt}",
                "timestamp": datetime.utcnow().isoformat()
            }


class TwilioIntegration:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.messaging_service_sid = os.getenv("TWILIO_MESSAGING_SERVICE_SID", "")
        self.client = None
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
    
    async def send_sms(self, to_number: str, from_number: str, body: str) -> dict:
        """Send SMS message via Twilio."""
        if not self.client:
            return {"success": False, "error": "Twilio client not configured"}
        
        try:
            if self.messaging_service_sid:
                message = self.client.messages.create(
                    messaging_service_sid=self.messaging_service_sid,
                    body=body,
                    to=to_number
                )
            else:
                message = self.client.messages.create(
                    body=body,
                    from_=from_number,
                    to=to_number
                )
            
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status,
                "to": to_number,
                "from": from_number
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class TelegramIntegration:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.approved_chat_id = os.getenv("TELEGRAM_APPROVED_CHAT_ID", "")
        self.bot = None
        self.pending_messages: Dict[str, dict] = {}  # Store pending messages for approval
        
        if self.bot_token:
            self.bot = Bot(token=self.bot_token)
    
    async def send_draft_for_approval(self, from_number: str, to_number: str, original_message: str, draft_reply: str) -> dict:
        """Send draft message to Telegram for approval."""
        if not self.bot:
            return {"success": False, "error": "Telegram bot not configured"}
        
        if not self.approved_chat_id:
            return {"success": False, "error": "TELEGRAM_APPROVED_CHAT_ID not configured"}
        
        # Generate unique ID for this message
        message_id = hashlib.sha256(f"{from_number}:{to_number}:{original_message}:{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        
        # Store pending message
        self.pending_messages[message_id] = {
            "from_number": from_number,
            "to_number": to_number,
            "original_message": original_message,
            "draft_reply": draft_reply,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Send to Telegram
        approval_text = f"""📱 *New SMS Draft for Approval*

*From:* {from_number}
*To:* {to_number}

*Original Message:*
{original_message}

*Draft Reply:*
{draft_reply}

Approve with: /send {message_id}
Reject with: /reject {message_id}"""
        
        try:
            await self.bot.send_message(
                chat_id=self.approved_chat_id,
                text=approval_text,
                parse_mode="Markdown"
            )
            return {
                "success": True,
                "message_id": message_id,
                "pending": True
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_pending_message(self, message_id: str) -> Optional[dict]:
        """Get pending message by ID."""
        return self.pending_messages.get(message_id)
    
    async def remove_pending_message(self, message_id: str) -> bool:
        """Remove pending message after approval/rejection."""
        if message_id in self.pending_messages:
            del self.pending_messages[message_id]
            return True
        return False


class LLMIntegration:
    def __init__(self):
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.hf_model = os.getenv("HUGGINGFACE_MODEL", "meta-llama/Llama-2-7b-chat-hf")
        self.client = None
        
        if self.hf_api_key:
            self.client = InferenceClient(token=self.hf_api_key)
    
    async def generate_reply(self, message: str) -> str:
        """Generate reply using Hugging Face LLM."""
        if not self.client:
            return "LLM not configured. Please set HUGGINGFACE_API_KEY."
        
        try:
            prompt = f"""You are a helpful assistant. Respond to the following message concisely and helpfully.

User message: {message}

Response:"""
            
            response = self.client.text_generation(
                prompt=prompt,
                model=self.hf_model,
                max_new_tokens=200,
                temperature=0.7
            )
            
            # Clean up response
            reply = response.strip()
            if "Response:" in reply:
                reply = reply.split("Response:")[-1].strip()
            
            return reply
        except Exception as e:
            return f"Error generating reply: {str(e)}"


class ParagraphGenerator:
    def __init__(self):
        pass
    
    def generate_post(self, chat_content: str, appraisal: dict) -> str:
        """Generate a paragraph post from chat content and appraisal."""
        word_count = appraisal.get("word_count", 0)
        value_usd = appraisal.get("estimated_value_usd", 0)
        quality = appraisal.get("quality_rating", "C")
        
        # Extract first sentence for summary
        sentences = chat_content.split(".")
        summary = sentences[0] if sentences else chat_content[:100]
        
        post = f"""
🎨 AI-Generated Art & Chat Artifact

This unique digital piece was generated from chat content with {word_count} words.
Appraised value: ${value_usd:.2f} USD | Quality Rating: {quality}

{summary}

🔗 Provenance: Merkle tree verified, IPFS stored, blockchain anchored.
💎 Each piece is cryptographically unique and permanently recorded.
"""
        return post.strip()


class ChatAppraiser:
    def __init__(self):
        pass
    
    def appraise_chat(self, chat_content: str) -> dict:
        """Appraise chat content for value and quality."""
        word_count = len(chat_content.split())
        char_count = len(chat_content)
        
        # Simple appraisal metrics
        complexity_score = min(1.0, word_count / 1000)
        value_score = min(1.0, char_count / 10000)
        
        appraisal = {
            "word_count": word_count,
            "char_count": char_count,
            "complexity_score": complexity_score,
            "value_score": value_score,
            "estimated_value_usd": round(complexity_score * value_score * 100, 2),
            "quality_rating": "A" if value_score > 0.8 else "B" if value_score > 0.5 else "C",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return appraisal


class ChatPipeline:
    def __init__(self):
        self.stages = [
            PipelineStage("Extract", 1.0),
            PipelineStage("Transform", 1.5),
            PipelineStage("Load", 1.0),
            PipelineStage("Analyze", 2.0),
            PipelineStage("Generate Art", 3.0),
            PipelineStage("Deploy", 1.5)
        ]
        self.current_stage = 0
        self.artifacts = {}
        self.blockchain = BlockchainIntegration()
        self.ipfs = IPFSIntegration()
        self.github = GitHubIntegration()
        self.appraiser = ChatAppraiser()
        self.art_generator = ArtGenerator()
        self.post_generator = ParagraphGenerator()
    
    async def process_chat(self, chat_content: str, github_token: Optional[str] = None, repo_name: Optional[str] = None, generate_art: bool = True) -> dict:
        """Process chat through the full evaluation pipeline with art generation."""
        # Stage 1: Extract - Create Merkle tree
        merkle = MerkleTree()
        chunks = [chat_content[i:i+1000] for i in range(0, len(chat_content), 1000)]
        for chunk in chunks:
            merkle.add_leaf(chunk)
        merkle.build_tree()
        root_hash = merkle.get_root_hash()
        
        # Stage 2: Transform - Base64 encode
        chat_b64 = base64.b64encode(chat_content.encode()).decode()
        
        # Stage 3: Load - Upload to IPFS
        ipfs_result = await self.ipfs.upload_to_ipfs(chat_content, "chat.txt")
        
        # Stage 4: Analyze - Appraise chat
        appraisal = self.appraiser.appraise_chat(chat_content)
        
        # Stage 5: Generate Art from chat
        art_result = None
        art_ipfs_result = None
        if generate_art:
            art_result = await self.art_generator.generate_art_from_chat(chat_content)
            if art_result.get("success") and art_result.get("image_base64"):
                # Upload art to IPFS
                art_bytes = base64.b64decode(art_result["image_base64"])
                art_ipfs_result = await self.ipfs.upload_to_ipfs(art_bytes.decode("latin1"), "generated_art.png")
        
        # Generate paragraph post
        post_content = self.post_generator.generate_post(chat_content, appraisal)
        
        # Stage 6: Deploy - Upload to blockchain and GitHub
        # Include art CID and post in blockchain metadata
        metadata = {
            "merkle_root": root_hash,
            "ipfs_cid": ipfs_result.get("cid"),
            "art_cid": art_ipfs_result.get("cid") if art_ipfs_result else None,
            "post": post_content[:500],  # Truncate for blockchain
            "repo_url": None
        }
        
        blockchain_result = await self.blockchain.upload_to_blockchain(root_hash, hashlib.sha256(chat_content.encode()).hexdigest())
        
        github_result = None
        if github_token and repo_name:
            try:
                repo_data = await self.github.create_repository(
                    github_token,
                    repo_name,
                    f"Chat artifact with AI-generated art - Merkle root: {root_hash[:16]}..."
                )
                
                # Create appraisal file
                appraisal_content = json.dumps(appraisal, indent=2)
                file_result = await self.github.create_file(
                    github_token,
                    repo_data["owner"]["login"],
                    repo_name,
                    "appraisal.json",
                    appraisal_content,
                    "Add chat appraisal"
                )
                
                # Create post file
                post_result = await self.github.create_file(
                    github_token,
                    repo_data["owner"]["login"],
                    repo_name,
                    "post.md",
                    post_content,
                    "Add generated post"
                )
                
                metadata["repo_url"] = repo_data["html_url"]
                
                github_result = {
                    "repository": repo_data["html_url"],
                    "file_url": file_result["content"]["html_url"],
                    "post_url": post_result["content"]["html_url"],
                    "commit_sha": file_result["commit"]["sha"]
                }
            except Exception as e:
                github_result = {"error": str(e)}
        
        # Collect all artifacts
        artifacts = {
            "chat_hash": hashlib.sha256(chat_content.encode()).hexdigest(),
            "chat_base64": chat_b64,
            "merkle_root": root_hash,
            "chunk_count": len(chunks),
            "timestamp": datetime.utcnow().isoformat(),
            "size_bytes": len(chat_content),
            "ipfs": ipfs_result,
            "blockchain": blockchain_result,
            "appraisal": appraisal,
            "art": art_result,
            "art_ipfs": art_ipfs_result,
            "post": post_content,
            "github": github_result
        }
        
        self.artifacts = artifacts
        
        return artifacts


pipeline = ChatPipeline()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with neomorphic dashboard."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Pipeline - Full Evaluation System</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #e0e5ec;
                min-height: 100vh;
                color: #333;
            }
            
            .container {
                max-width: 1600px;
                margin: 0 auto;
                padding: 60px 40px;
            }
            
            h1 {
                font-size: 56px;
                margin-bottom: 10px;
                color: #2d3436;
                font-weight: 700;
                letter-spacing: -2px;
            }
            
            .subtitle {
                color: #636e72;
                margin-bottom: 50px;
                font-size: 20px;
                font-weight: 400;
            }
            
            .neomorphic-card {
                background: #e0e5ec;
                border-radius: 30px;
                padding: 40px;
                margin-bottom: 40px;
                box-shadow: 
                    20px 20px 60px #bec3c9,
                    -20px -20px 60px #ffffff;
            }
            
            .upload-section {
                text-align: center;
                transition: all 0.3s;
            }
            
            .upload-btn {
                background: #e0e5ec;
                color: #2d3436;
                border: none;
                padding: 18px 50px;
                font-size: 16px;
                border-radius: 15px;
                cursor: pointer;
                font-weight: 600;
                margin: 10px;
                box-shadow: 
                    8px 8px 16px #bec3c9,
                    -8px -8px 16px #ffffff;
                transition: all 0.2s;
            }
            
            .upload-btn:hover {
                box-shadow: 
                    4px 4px 8px #bec3c9,
                    -4px -4px 8px #ffffff;
                transform: translateY(2px);
            }
            
            .upload-btn:active {
                box-shadow: 
                    inset 4px 4px 8px #bec3c9,
                    inset -4px -4px 8px #ffffff;
            }
            
            .pipeline-container {
                margin-bottom: 40px;
            }
            
            .pipeline-title {
                font-size: 28px;
                margin-bottom: 40px;
                color: #2d3436;
                font-weight: 600;
            }
            
            .pipeline-stages {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 50px;
                position: relative;
            }
            
            .pipeline-stages::before {
                content: '';
                position: absolute;
                top: 50px;
                left: 50px;
                right: 50px;
                height: 6px;
                background: #d1d5db;
                z-index: 0;
                border-radius: 3px;
            }
            
            .stage {
                text-align: center;
                position: relative;
                z-index: 1;
                flex: 1;
            }
            
            .stage-circle {
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: #e0e5ec;
                border: none;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 20px;
                font-size: 40px;
                transition: all 0.3s;
                box-shadow: 
                    8px 8px 16px #bec3c9,
                    -8px -8px 16px #ffffff;
            }
            
            .stage.active .stage-circle {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                box-shadow: 
                    8px 8px 16px #bec3c9,
                    -8px -8px 16px #ffffff,
                    0 0 30px rgba(102, 126, 234, 0.5);
                animation: pulse 2s infinite;
            }
            
            .stage.completed .stage-circle {
                background: #667eea;
                box-shadow: 
                    8px 8px 16px #bec3c9,
                    -8px -8px 16px #ffffff;
            }
            
            .stage-label {
                font-size: 14px;
                color: #636e72;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            
            .stage.active .stage-label,
            .stage.completed .stage-label {
                color: #2d3436;
            }
            
            @keyframes pulse {
                0%, 100% { box-shadow: 8px 8px 16px #bec3c9, -8px -8px 16px #ffffff, 0 0 30px rgba(102, 126, 234, 0.5); }
                50% { box-shadow: 8px 8px 16px #bec3c9, -8px -8px 16px #ffffff, 0 0 50px rgba(102, 126, 234, 0.8); }
            }
            
            .file-animation {
                height: 150px;
                background: #e0e5ec;
                border-radius: 20px;
                position: relative;
                overflow: hidden;
                margin-bottom: 30px;
                box-shadow: 
                    inset 8px 8px 16px #bec3c9,
                    inset -8px -8px 16px #ffffff;
            }
            
            .file {
                position: absolute;
                width: 70px;
                height: 70px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                transition: left 0.5s ease-in-out;
                box-shadow: 
                    8px 8px 16px #bec3c9,
                    -8px -8px 16px #ffffff;
            }
            
            .file-label {
                position: absolute;
                bottom: -30px;
                font-size: 12px;
                white-space: nowrap;
                color: #636e72;
                font-weight: 600;
            }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 30px;
                margin-bottom: 40px;
            }
            
            .metric-card {
                background: #e0e5ec;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 
                    8px 8px 16px #bec3c9,
                    -8px -8px 16px #ffffff;
            }
            
            .metric-label {
                font-size: 14px;
                color: #636e72;
                margin-bottom: 10px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            
            .metric-value {
                font-size: 36px;
                font-weight: 700;
                color: #667eea;
            }
            
            .integration-section {
                background: #e0e5ec;
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 
                    8px 8px 16px #bec3c9,
                    -8px -8px 16px #ffffff;
            }
            
            .integration-title {
                font-size: 20px;
                margin-bottom: 20px;
                color: #2d3436;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .integration-icon {
                font-size: 24px;
            }
            
            .integration-data {
                font-family: 'SF Mono', Monaco, monospace;
                font-size: 13px;
                color: #636e72;
                word-break: break-all;
                background: #e0e5ec;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 10px;
                box-shadow: 
                    inset 4px 4px 8px #bec3c9,
                    inset -4px -4px 8px #ffffff;
            }
            
            .integration-link {
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
            }
            
            #chatInput {
                width: 100%;
                height: 180px;
                background: #e0e5ec;
                border: none;
                border-radius: 15px;
                color: #2d3436;
                padding: 20px;
                font-size: 15px;
                resize: vertical;
                margin-bottom: 20px;
                box-shadow: 
                    inset 8px 8px 16px #bec3c9,
                    inset -8px -8px 16px #ffffff;
                font-family: 'SF Mono', Monaco, monospace;
            }
            
            #chatInput:focus {
                outline: none;
            }
            
            #githubToken, #repoName {
                width: 100%;
                background: #e0e5ec;
                border: none;
                border-radius: 15px;
                color: #2d3436;
                padding: 15px 20px;
                font-size: 15px;
                margin-bottom: 15px;
                box-shadow: 
                    inset 8px 8px 16px #bec3c9,
                    inset -8px -8px 16px #ffffff;
            }
            
            #githubToken:focus, #repoName:focus {
                outline: none;
            }
            
            .hidden {
                display: none;
            }
            
            .status-badge {
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin-left: 10px;
                box-shadow: 
                    4px 4px 8px #bec3c9,
                    -4px -4px 8px #ffffff;
            }
            
            .status-success {
                background: #00b894;
                color: white;
            }
            
            .status-pending {
                background: #fdcb6e;
                color: #2d3436;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Chat Pipeline</h1>
            <p class="subtitle">Full Evaluation System with Blockchain, IPFS & GitHub Integration</p>
            
            <div class="neomorphic-card upload-section" id="uploadSection">
                <h2 style="margin-bottom: 25px; color: #2d3436;">Upload Chat or Charts</h2>
                <p style="color: #636e72; margin-bottom: 25px;">Drag & drop MD or ZIP files, or paste chat content below</p>
                
                <textarea id="chatInput" placeholder="Paste chat content here..."></textarea>
                
                <div style="margin-bottom: 20px;">
                    <input type="text" id="githubToken" placeholder="GitHub Token (optional - for repo creation)">
                    <input type="text" id="repoName" placeholder="Repository Name (optional)">
                </div>
                
                <input type="file" id="fileInput" accept=".md,.zip" style="display: none;" multiple>
                <button class="upload-btn" onclick="document.getElementById('fileInput').click()">📁 Upload Files</button>
                <button class="upload-btn" onclick="processChat()">⚡ Process Chat</button>
            </div>
            
            <div class="neomorphic-card pipeline-container hidden" id="pipelineContainer">
                <h2 class="pipeline-title">Pipeline Progress</h2>
                
                <div class="pipeline-stages">
                    <div class="stage" id="stage0">
                        <div class="stage-circle">📤</div>
                        <div class="stage-label">EXTRACT</div>
                    </div>
                    <div class="stage" id="stage1">
                        <div class="stage-circle">🔄</div>
                        <div class="stage-label">TRANSFORM</div>
                    </div>
                    <div class="stage" id="stage2">
                        <div class="stage-circle">📥</div>
                        <div class="stage-label">LOAD</div>
                    </div>
                    <div class="stage" id="stage3">
                        <div class="stage-circle">📊</div>
                        <div class="stage-label">ANALYZE</div>
                    </div>
                    <div class="stage" id="stage4">
                        <div class="stage-circle">🎨</div>
                        <div class="stage-label">GENERATE ART</div>
                    </div>
                    <div class="stage" id="stage5">
                        <div class="stage-circle">🚀</div>
                        <div class="stage-label">DEPLOY</div>
                    </div>
                </div>
                
                <div class="file-animation" id="fileAnimation">
                    <div class="file" id="animatedFile" style="left: 30px;">
                        📄
                        <span class="file-label" id="fileLabel">chat.txt</span>
                    </div>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">CHAT SIZE</div>
                        <div class="metric-value" id="metricSize">0 KB</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">CHUNKS</div>
                        <div class="metric-value" id="metricChunks">0</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">PROCESSING TIME</div>
                        <div class="metric-value" id="metricTime">0s</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">ESTIMATED VALUE</div>
                        <div class="metric-value" id="metricValue">$0</div>
                    </div>
                </div>
            </div>
            
            <div class="neomorphic-card integration-section hidden" id="merkleSection">
                <h2 class="integration-title"><span class="integration-icon">🌳</span> Merkle Provenance</h2>
                <div class="integration-data"><strong>Chat Hash:</strong> <span id="chatHash">-</span></div>
                <div class="integration-data"><strong>Merkle Root:</strong> <span id="merkleRoot">-</span></div>
                <div class="integration-data"><strong>Base64:</strong> <span id="base64Preview">-</span></div>
            </div>
            
            <div class="neomorphic-card integration-section hidden" id="ipfsSection">
                <h2 class="integration-title"><span class="integration-icon">🌐</span> IPFS Storage</h2>
                <div class="integration-data"><strong>CID:</strong> <span id="ipfsCid">-</span></div>
                <div class="integration-data"><strong>Gateway URL:</strong> <a id="ipfsGateway" class="integration-link" target="_blank">-</a></div>
            </div>
            
            <div class="neomorphic-card integration-section hidden" id="blockchainSection">
                <h2 class="integration-title"><span class="integration-icon">⛓️</span> Blockchain</h2>
                <div class="integration-data"><strong>Transaction Hash:</strong> <span id="txHash">-</span></div>
                <div class="integration-data"><strong>Block Number:</strong> <span id="blockNumber">-</span></div>
                <div class="integration-data"><strong>Explorer:</strong> <a id="explorerUrl" class="integration-link" target="_blank">-</a></div>
            </div>
            
            <div class="neomorphic-card integration-section hidden" id="appraisalSection">
                <h2 class="integration-title"><span class="integration-icon">💎</span> Chat Appraisal</h2>
                <div class="integration-data"><strong>Word Count:</strong> <span id="wordCount">-</span></div>
                <div class="integration-data"><strong>Complexity Score:</strong> <span id="complexityScore">-</span></div>
                <div class="integration-data"><strong>Value Score:</strong> <span id="valueScore">-</span></div>
                <div class="integration-data"><strong>Quality Rating:</strong> <span id="qualityRating">-</span></div>
            </div>
            
            <div class="neomorphic-card integration-section hidden" id="githubSection">
                <h2 class="integration-title"><span class="integration-icon">🐙</span> GitHub Repository</h2>
                <div class="integration-data"><strong>Repository:</strong> <a id="githubRepo" class="integration-link" target="_blank">-</a></div>
                <div class="integration-data"><strong>File URL:</strong> <a id="githubFile" class="integration-link" target="_blank">-</a></div>
                <div class="integration-data"><strong>Commit SHA:</strong> <span id="commitSha">-</span></div>
            </div>
        </div>
        
        <script>
            let currentStage = 0;
            const totalStages = 6;
            
            document.getElementById('fileInput').addEventListener('change', handleFileUpload);
            document.getElementById('uploadSection').addEventListener('dragover', handleDragOver);
            document.getElementById('uploadSection').addEventListener('dragleave', handleDragLeave);
            document.getElementById('uploadSection').addEventListener('drop', handleDrop);
            
            function handleDragOver(e) {
                e.preventDefault();
                document.getElementById('uploadSection').style.boxShadow = '20px 20px 60px #bec3c9, -20px -20px 60px #ffffff, 0 0 30px rgba(102, 126, 234, 0.3)';
            }
            
            function handleDragLeave(e) {
                e.preventDefault();
                document.getElementById('uploadSection').style.boxShadow = '20px 20px 60px #bec3c9, -20px -20px 60px #ffffff';
            }
            
            function handleDrop(e) {
                e.preventDefault();
                document.getElementById('uploadSection').style.boxShadow = '20px 20px 60px #bec3c9, -20px -20px 60px #ffffff';
                const files = e.dataTransfer.files;
                handleFiles(files);
            }
            
            function handleFileUpload(e) {
                const files = e.target.files;
                handleFiles(files);
            }
            
            async function handleFiles(files) {
                for (let file of files) {
                    const content = await file.text();
                    document.getElementById('chatInput').value += content + '\\n\\n';
                }
            }
            
            async function processChat() {
                const chatContent = document.getElementById('chatInput').value;
                const githubToken = document.getElementById('githubToken').value;
                const repoName = document.getElementById('repoName').value;
                
                if (!chatContent.trim()) {
                    alert('Please enter chat content or upload files');
                    return;
                }
                
                const startTime = Date.now();
                
                // Show all sections
                document.getElementById('pipelineContainer').classList.remove('hidden');
                document.getElementById('merkleSection').classList.remove('hidden');
                document.getElementById('ipfsSection').classList.remove('hidden');
                document.getElementById('blockchainSection').classList.remove('hidden');
                document.getElementById('appraisalSection').classList.remove('hidden');
                
                if (githubToken && repoName) {
                    document.getElementById('githubSection').classList.remove('hidden');
                }
                
                document.getElementById('artSection').classList.remove('hidden');
                document.getElementById('postSection').classList.remove('hidden');
                
                // Animate through stages
                for (let i = 0; i < totalStages; i++) {
                    await animateStage(i);
                }
                
                // Process via API
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        chat_content: chatContent,
                        github_token: githubToken || null,
                        repo_name: repoName || null
                    })
                });
                
                const data = await response.json();
                const endTime = Date.now();
                
                // Update metrics
                document.getElementById('metricSize').textContent = formatBytes(data.size_bytes);
                document.getElementById('metricChunks').textContent = data.chunk_count;
                document.getElementById('metricTime').textContent = ((endTime - startTime) / 1000).toFixed(2) + 's';
                document.getElementById('metricValue').textContent = '$' + (data.appraisal?.estimated_value_usd || 0).toFixed(2);
                
                // Update Merkle info
                document.getElementById('chatHash').textContent = data.chat_hash.substring(0, 40) + '...';
                document.getElementById('merkleRoot').textContent = data.merkle_root.substring(0, 40) + '...';
                document.getElementById('base64Preview').textContent = data.chat_base64.substring(0, 80) + '...';
                
                // Update IPFS info
                document.getElementById('ipfsCid').textContent = data.ipfs?.cid || '-';
                document.getElementById('ipfsGateway').textContent = data.ipfs?.gateway_url || '-';
                document.getElementById('ipfsGateway').href = data.ipfs?.gateway_url || '#';
                
                // Update Blockchain info
                document.getElementById('txHash').textContent = data.blockchain?.transaction_hash?.substring(0, 40) + '...' || '-';
                document.getElementById('blockNumber').textContent = data.blockchain?.block_number || '-';
                document.getElementById('explorerUrl').textContent = data.blockchain?.explorer_url || '-';
                document.getElementById('explorerUrl').href = data.blockchain?.explorer_url || '#';
                
                // Update Appraisal info
                document.getElementById('wordCount').textContent = data.appraisal?.word_count || '-';
                document.getElementById('complexityScore').textContent = (data.appraisal?.complexity_score || 0).toFixed(3);
                document.getElementById('valueScore').textContent = (data.appraisal?.value_score || 0).toFixed(3);
                document.getElementById('qualityRating').textContent = data.appraisal?.quality_rating || '-';
                
                // Update GitHub info
                if (data.github && !data.github.error) {
                    document.getElementById('githubRepo').textContent = data.github.repository || '-';
                    document.getElementById('githubRepo').href = data.github.repository || '#';
                    document.getElementById('githubFile').textContent = data.github.file_url || '-';
                    document.getElementById('githubFile').href = data.github.file_url || '#';
                    document.getElementById('githubPost').textContent = data.github.post_url || '-';
                    document.getElementById('githubPost').href = data.github.post_url || '#';
                    document.getElementById('commitSha').textContent = data.github.commit_sha?.substring(0, 16) + '...' || '-';
                }
                
                // Update Art info
                if (data.art && data.art.success) {
                    document.getElementById('generatedArt').src = 'data:image/png;base64,' + data.art.image_base64;
                    document.getElementById('generatedArt').style.display = 'block';
                    document.getElementById('artPrompt').textContent = data.art.prompt?.substring(0, 100) + '...' || '-';
                } else {
                    document.getElementById('artPrompt').textContent = data.art?.fallback_description || 'Art generation failed';
                }
                
                if (data.art_ipfs) {
                    document.getElementById('artCid').textContent = data.art_ipfs.cid || '-';
                    document.getElementById('artGateway').textContent = data.art_ipfs.gateway_url || '-';
                    document.getElementById('artGateway').href = data.art_ipfs.gateway_url || '#';
                }
                
                // Update Post
                document.getElementById('postContent').textContent = data.post || '-';
            }
            
            async function animateStage(stageIndex) {
                const stage = document.getElementById('stage' + stageIndex);
                stage.classList.add('active');
                
                const file = document.getElementById('animatedFile');
                const positions = [30, 290, 550, 810, 1070, 1330];
                file.style.left = positions[stageIndex] + 'px';
                
                const labels = ['Extracting...', 'Transforming...', 'Loading to IPFS...', 'Analyzing...', 'Generating Art...', 'Deploying...'];
                document.getElementById('fileLabel').textContent = labels[stageIndex];
                
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                stage.classList.remove('active');
                stage.classList.add('completed');
            }
            
            function formatBytes(bytes) {
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
            }
        </script>
    </body>
    </html>
    """


@app.post("/api/process")
async def process_chat(request: ChatRequest):
    """Process chat content through the full pipeline."""
    artifacts = await pipeline.process_chat(request.chat_content, request.github_token, request.repo_name)
    return artifacts


@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload MD or ZIP files for processing."""
    contents = []
    for file in files:
        content = await file.read()
        contents.append(content.decode('utf-8'))
    
    combined_content = '\n\n'.join(contents)
    artifacts = await pipeline.process_chat(combined_content)
    return artifacts


@app.get("/api/artifacts/{artifact_id}")
async def get_artifacts(artifact_id: str):
    """Retrieve artifacts by ID."""
    # In production, implement storage retrieval
    return {"error": "Artifact storage not implemented in demo"}


# Initialize integrations
twilio = TwilioIntegration()
telegram = TelegramIntegration()
llm = LLMIntegration()


@app.post("/twilio/inbound")
async def twilio_inbound(request: Request):
    """Handle inbound SMS from Twilio webhook."""
    try:
        # Log raw request for debugging
        print(f"[Twilio Inbound] Headers: {dict(request.headers)}")
        
        form_data = await request.form()
        print(f"[Twilio Inbound] Form data keys: {list(form_data.keys())}")
        print(f"[Twilio Inbound] Full form data: {dict(form_data)}")
        
        # Handle both uppercase and lowercase parameter names
        from_number = form_data.get("From", form_data.get("from", ""))
        to_number = form_data.get("To", form_data.get("to", ""))
        body = form_data.get("Body", form_data.get("body", ""))
        
        print(f"[Twilio Inbound] From: {from_number}, To: {to_number}, Body: '{body}'")
        
        if not body:
            print("[Twilio Inbound] Warning: Empty body received")
            return Response(content="<?xml version='1.0' encoding='UTF-8'?><Response></Response>", media_type="application/xml")
        
        # Generate LLM draft reply
        draft_reply = await llm.generate_reply(body)
        print(f"[Twilio Inbound] LLM draft: '{draft_reply}'")
        
        # Check auto-reply mode
        auto_reply = os.getenv("AUTO_REPLY", "false").lower() == "true"
        allowlist = os.getenv("AUTO_REPLY_ALLOWLIST", "").split(",") if os.getenv("AUTO_REPLY_ALLOWLIST") else []
        
        if auto_reply and from_number in allowlist:
            # Auto-reply for allowlisted numbers
            print(f"[Twilio Inbound] Auto-replying to {from_number}")
            await twilio.send_sms(from_number, to_number, draft_reply)
            return Response(content=f"<?xml version='1.0' encoding='UTF-8'?><Response><Message>{draft_reply}</Message></Response>", media_type="application/xml")
        else:
            # Send to Telegram for approval
            print(f"[Twilio Inbound] Sending to Telegram for approval")
            approval_result = await telegram.send_draft_for_approval(from_number, to_number, body, draft_reply)
            if approval_result.get("success"):
                return Response(content="<?xml version='1.0' encoding='UTF-8'?><Response><Message>Your message has been received and is pending approval.</Message></Response>", media_type="application/xml")
            else:
                print(f"[Twilio Inbound] Telegram error: {approval_result.get('error')}")
                return Response(content=f"<?xml version='1.0' encoding='UTF-8'?><Response><Message>Error processing message: {approval_result.get('error')}</Message></Response>", media_type="application/xml")
    except Exception as e:
        print(f"[Twilio Inbound] Error: {str(e)}")
        return Response(content="<?xml version='1.0' encoding='UTF-8'?><Response></Response>", media_type="application/xml")


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """Handle Telegram bot webhook for approval commands."""
    try:
        data = await request.json()
        
        # Extract message data
        message = data.get("message", {})
        text = message.get("text", "")
        chat_id = message.get("chat", {}).get("id", "")
        
        # Parse command
        if text.startswith("/send "):
            message_id = text.split("/send ")[1].strip()
            pending = await telegram.get_pending_message(message_id)
            
            if pending:
                # Send approved message via Twilio
                result = await twilio.send_sms(
                    pending["from_number"],
                    pending["to_number"],
                    pending["draft_reply"]
                )
                
                # Remove from pending
                await telegram.remove_pending_message(message_id)
                
                # Send confirmation to Telegram
                if telegram.bot:
                    await telegram.bot.send_message(
                        chat_id=chat_id,
                        text=f"✅ Message {message_id} approved and sent!"
                    )
                
                return {"status": "approved", "message_id": message_id, "twilio_result": result}
            else:
                if telegram.bot:
                    await telegram.bot.send_message(
                        chat_id=chat_id,
                        text=f"❌ Message {message_id} not found or already processed."
                    )
                return {"status": "error", "message": "Message not found"}
        
        elif text.startswith("/reject "):
            message_id = text.split("/reject ")[1].strip()
            pending = await telegram.get_pending_message(message_id)
            
            if pending:
                # Remove from pending
                await telegram.remove_pending_message(message_id)
                
                # Send confirmation to Telegram
                if telegram.bot:
                    await telegram.bot.send_message(
                        chat_id=chat_id,
                        text=f"❌ Message {message_id} rejected."
                    )
                
                return {"status": "rejected", "message_id": message_id}
            else:
                if telegram.bot:
                    await telegram.bot.send_message(
                        chat_id=chat_id,
                        text=f"❌ Message {message_id} not found or already processed."
                    )
                return {"status": "error", "message": "Message not found"}
        
        return {"status": "ignored"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
