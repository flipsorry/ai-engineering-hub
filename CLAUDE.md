# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

The AI Engineering Hub is a collection of AI/ML tutorials and examples focusing on:
- RAG (Retrieval-Augmented Generation) applications
- AI agents using CrewAI and AutoGen
- LLM integration examples (DeepSeek, Llama, OpenAI)
- MCP (Model Context Protocol) implementations
- Multi-modal AI applications (text, audio, video, images)

## Project Structure

This repository contains 60+ independent AI engineering projects, each in its own directory with:
- Individual README.md files with setup instructions
- Standalone applications (app.py, main.py, or notebook.ipynb)
- Project-specific dependencies (requirements.txt, pyproject.toml, or package.json)

Major categories include:
- **RAG Applications**: `agentic_rag/`, `fastest-rag-stack/`, `document-chat-rag/`, `multimodal-rag-assemblyai/`
- **AI Agents**: `Multi-Agent-deep-researcher-mcp-windows-linux/`, `financial-analyst-deepseek/`, `hotel-booking-crew/`
- **MCP Servers**: `mcp-agentic-rag/`, `llamaindex-mcp/`, `pixeltable-mcp/`, `cursor_linkup_mcp/`
- **UI Applications**: `deepseek-thinking-ui/`, `qwen3-thinking-ui/`, `gpt-oss-thinking-ui/`
- **Workflow Systems**: `book-writer-flow/`, `brand-monitoring/`, `content_planner_flow/`

## Common Development Commands

### Python Projects (most common)
```bash
# Install dependencies
pip install -r requirements.txt
# Or for uv projects
uv install

# Run Streamlit applications
streamlit run app.py
streamlit run app_deep_seek.py  # For DeepSeek variants
streamlit run app_local.py      # For local model variants

# Run Python applications
python app.py
python main.py
```

### Node.js Projects (Motia-based)
```bash
# Install dependencies
npm install

# Development
npm run dev
npm run dev:debug

# Build
npm run build

# Clean
npm run clean
```

### Docker-based Services
Many projects require external services:
```bash
# Qdrant vector database (common across RAG projects)
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant

# Milvus (alternative vector DB)
# Check project-specific README for docker-compose.yml
```

## Key Technologies and Patterns

### Common Dependencies
- **AI/ML**: `openai`, `crewai`, `crewai-tools`, `llama-index`, `transformers`
- **Vector Databases**: `qdrant-client`, `pymilvus`, `chromadb`
- **Web Frameworks**: `streamlit`, `fastapi`, `flask`
- **Document Processing**: `markitdown`, `dockling`, `pymupdf`
- **Audio/Video**: `assemblyai`, `whisper`, `opencv-python`

### MCP Server Pattern
MCP servers typically follow this structure:
- `server.py` - Main MCP server implementation
- `tools.py` - Tool definitions
- `pyproject.toml` - Dependencies with MCP

### CrewAI Pattern
CrewAI projects use:
- `config/` directory with `agents.yaml` and `tasks.yaml`
- `crew.py` - Main crew implementation
- `tools/custom_tool.py` - Custom tools

### RAG Application Pattern
- Document ingestion and chunking
- Vector database storage (Qdrant/Milvus)
- Embedding models (typically HuggingFace)
- LLM integration for generation
- Web interface via Streamlit

## Environment Variables

Common environment variables across projects:
- `OPENAI_API_KEY` - OpenAI API access
- `SAMBANOVA_API_KEY` - SambaNova inference
- `FIRECRAWL_API_KEY` - Web scraping
- `BRIGHDATA_USERNAME/PASSWORD` - Bright Data proxy
- `ASSEMBLYAI_API_KEY` - Audio processing

## Testing and Validation

Most projects include:
- Jupyter notebooks for experimentation (`.ipynb` files)
- Demo applications with sample data
- Video demonstrations (`.mp4` files)
- Individual project READMEs with setup instructions

Each project is self-contained - always check the specific project's README.md for detailed setup and usage instructions.