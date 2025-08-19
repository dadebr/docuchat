# DocuChat

A modern RAG (Retrieval-Augmented Generation) system with web interface built using LlamaIndex and Ollama. DocuChat enables you to create, manage, and chat with document knowledge bases through an intuitive web interface.

## 🚀 Project Overview

DocuChat is an intelligent document chat system that allows you to:
- **Upload and manage document collections** - Support for multiple file formats
- **Create searchable knowledge bases** - Advanced document indexing with LlamaIndex
- **Interactive chat interface** - Natural language conversations with your documents
- **Real-time document processing** - Instant indexing and retrieval
- **Modern web UI** - Clean, responsive interface built with modern web technologies

The system leverages the power of local LLMs through Ollama for privacy-focused document analysis and chat capabilities.

## 📋 Prerequisites

Before installing DocuChat, ensure you have the following installed:

### System Requirements
- **Python 3.8+** - Required for backend services
- **Node.js 16+** - Required for frontend development
- **Docker & Docker Compose** - For containerized deployment (recommended)
- **Git** - For cloning the repository

### LLM Requirements
- **Ollama** - Local LLM runtime (will be installed via Docker)
- **Compatible GPU** (recommended) - For faster inference
- **Minimum 8GB RAM** - 16GB+ recommended for better performance

## 🐳 Docker Installation (Recommended)

The easiest way to get DocuChat running is using Docker Compose:

### 1. Clone Repository
```bash
git clone https://github.com/dadebr/docuchat.git
cd docuchat
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env file with your configuration
```

### 3. Deploy with Docker Compose
```bash
docker-compose up -d
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Ollama API**: http://localhost:11434

## 🔧 Manual Installation

For development or custom deployments:

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your settings

# Start backend server
python main.py
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Ollama Setup
```bash
# Install Ollama (Linux/macOS)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a compatible model
ollama pull llama2  # or your preferred model

# Start Ollama service
ollama serve
```

## 📖 Usage Guide

### 1. Starting the Backend
The FastAPI backend handles document processing, indexing, and chat operations:

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000` with automatic documentation at `/docs`.

### 2. Starting the Frontend
The React frontend provides the user interface:

```bash
cd frontend
npm start
```

Access the web interface at `http://localhost:3000`.

### 3. Document Upload Process
1. **Navigate to Upload Section** - Click "Upload Documents" in the interface
2. **Select Files** - Choose your documents (PDF, TXT, DOCX supported)
3. **Create Knowledge Base** - Provide a name for your document collection
4. **Wait for Processing** - Documents will be indexed automatically
5. **Confirmation** - Receive notification when indexing is complete

### 4. Chat Interface
1. **Select Knowledge Base** - Choose from your available document collections
2. **Start Conversation** - Type your questions in natural language
3. **Receive Answers** - Get responses with source citations
4. **Follow-up Questions** - Continue the conversation contextually

## 🌟 Real-World Use Cases

### Legal Document Analysis
```
Use Case: Law firm analyzing contract collections
- Upload: Contract documents, legal precedents
- Query: "What are the standard termination clauses?"
- Benefit: Quick access to relevant legal language
```

### Research Paper Review
```
Use Case: Academic research across multiple papers
- Upload: Research papers, academic articles
- Query: "What methodologies were used in machine learning studies?"
- Benefit: Comprehensive literature review assistance
```

### Corporate Knowledge Management
```
Use Case: Company policy and procedure queries
- Upload: Employee handbooks, SOPs, training materials
- Query: "What is the process for requesting time off?"
- Benefit: Instant access to company information
```

### Technical Documentation
```
Use Case: Software development team documentation
- Upload: API docs, architecture guides, code documentation
- Query: "How do I implement authentication in the system?"
- Benefit: Faster developer onboarding and support
```

## 🛠️ Troubleshooting

### Common Issues

#### Backend Connection Issues
```bash
# Check if backend is running
curl http://localhost:8000/health

# Verify environment variables
cat backend/.env

# Check logs
docker-compose logs backend
```

#### Frontend Not Loading
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check for port conflicts
lsof -i :3000
```

#### Ollama Model Issues
```bash
# List available models
ollama list

# Pull required model
ollama pull llama2

# Test model
ollama run llama2 "Hello, world!"
```

#### Document Processing Failures
```bash
# Check supported file formats
# Ensure files are not corrupted
# Verify sufficient disk space
# Review backend logs for specific errors
```

### Performance Optimization

#### For Large Document Collections
- **Increase chunk size** in indexing configuration
- **Use GPU acceleration** for Ollama if available
- **Allocate more memory** to Docker containers
- **Consider SSD storage** for better I/O performance

#### For Slow Response Times
- **Optimize model selection** - smaller models for faster inference
- **Implement caching** for frequent queries
- **Use vector database** for large-scale deployments

### Error Code Reference

| Error Code | Description | Solution |
|------------|-------------|----------|
| CONN_001 | Backend connection failed | Check if backend service is running |
| PROC_002 | Document processing error | Verify file format and integrity |
| MODEL_003 | Ollama model not found | Pull required model with `ollama pull` |
| UPLOAD_004 | File upload size exceeded | Check file size limits in configuration |

## 🙏 Credits and Resources

### Core Technologies
- **[LlamaIndex](https://llamaindex.ai/)** - Document indexing and retrieval framework
- **[Ollama](https://ollama.ai/)** - Local LLM runtime and model management
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework for APIs
- **[React](https://reactjs.org/)** - Frontend user interface library

### Key Dependencies
- **Python Libraries**: `llama-index`, `fastapi`, `uvicorn`, `python-multipart`
- **JavaScript Libraries**: `react`, `axios`, `styled-components`
- **Infrastructure**: `docker`, `docker-compose`, `nginx`

### Learning Resources
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Ollama Model Library](https://ollama.ai/library)
- [RAG Implementation Guide](https://python.langchain.com/docs/use_cases/question_answering)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### Community and Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Join community discussions for help and ideas
- **Documentation**: Check the `/docs` endpoint for API documentation

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

### License
This project is open source. Please check the LICENSE file for details.

---

**Built with ❤️ for the open source community**

*For additional support, please open an issue on GitHub or check the documentation at the `/docs` API endpoint.*
