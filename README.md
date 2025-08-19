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
- **Git** - For cloning the repository

### LLM Requirements

- **Ollama** - Local LLM runtime (installed locally)
- **Compatible GPU** (recommended) - For faster inference
- **Minimum 8GB RAM** - 16GB+ recommended for better performance

## 🔧 Installation Guide

Follow these steps to set up DocuChat on your local machine:

### 1. Clone Repository

```bash
git clone https://github.com/dadebr/docuchat.git
cd docuchat
```

### 2. Install Ollama

**Linux/macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:** Download and install from [ollama.ai](https://ollama.ai/download/windows)

### 3. Pull a Language Model

```bash
ollama pull llama2  # or your preferred model
```

### 4. Start Ollama Service

```bash
ollama serve
```

Keep this terminal open. Ollama will run on http://localhost:11434

### 5. Configure Environment

```bash
cp .env.example .env
# Edit .env file if needed - default values should work for local setup
```

### 6. Backend Setup

**Open a new terminal for the backend:**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp ../.env .env

# Start backend server
python main.py
```

The API will be available at http://localhost:8000 with automatic documentation at /docs.

### 7. Frontend Setup

**Open another new terminal for the frontend:**

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The web interface will be available at http://localhost:3000.

### 8. Alternative Frontend Setup (using npx)

If you prefer not to install dependencies globally:

```bash
cd frontend
npx create-react-app . --template typescript
npm start
```

## 🪟 Windows Local Installation

### Prerequisites

- **Python for Windows** - Download from [python.org](https://www.python.org/downloads/windows/)
  - ⚠️ **Important**: During installation, check "Add Python to PATH"
- **Node.js** - Download from [nodejs.org](https://nodejs.org/)
- **Ollama for Windows** - Download from [ollama.ai/download/windows](https://ollama.ai/download/windows)
- **Git** (optional) - Download from [git-scm.com](https://git-scm.com/download/win)

### Step-by-Step Installation

1. **Clone or Download Repository**
   ```cmd
   git clone https://github.com/dadebr/docuchat.git
   cd docuchat
   ```
   Or download as ZIP and extract to a folder.

2. **Copy Environment File**
   ```cmd
   copy .env.example .env
   ```

3. **Backend Setup (Command Prompt)**
   ```cmd
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   copy ..\..env .env
   ```

4. **Frontend Setup (New Command Prompt)**
   ```cmd
   cd frontend
   npm install
   ```

5. **Install and Configure Ollama**
   - Run the Ollama installer
   - Open Command Prompt and run:
   ```cmd
   ollama pull llama2
   ```

### Running the Application (3 Terminals)

**Terminal 1 - Ollama Service:**
```cmd
ollama serve
```

**Terminal 2 - Backend Service:**
```cmd
cd backend
venv\Scripts\activate
python main.py
```

**Terminal 3 - Frontend Service:**
```cmd
cd frontend
npm start
```

### Troubleshooting Windows Issues

#### Virtual Environment Activation
If `venv\Scripts\activate` doesn't work, try:
```cmd
venv\Scripts\activate.bat
```

#### PowerShell Execution Policy
If using PowerShell, you may need to run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### pip and Build Tools
If you encounter build errors during `pip install`:
- Install Visual Studio Build Tools
- Or use: `pip install --upgrade setuptools wheel`

#### File Copying
If `copy` command fails, manually copy `.env.example` to `.env` and `backend/.env` using File Explorer.

## 🚀 Quick Start

Once all services are running:

1. Access the web interface at http://localhost:3000
2. Upload documents using the upload interface
3. Create knowledge bases by organizing your documents
4. Start chatting with your documents using natural language

## 📖 Usage Guide

### Starting the System

You need to run three services:

1. **Ollama Service (Terminal 1):**
   ```bash
   ollama serve
   ```

2. **Backend Service (Terminal 2):**
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python main.py
   ```

3. **Frontend Service (Terminal 3):**
   ```bash
   cd frontend
   npm start
   ```

### Document Upload Process

1. **Navigate to Upload Section** - Click "Upload Documents" in the interface
2. **Select Files** - Choose your documents (PDF, TXT, DOCX supported)
3. **Create Knowledge Base** - Provide a name for your document collection
4. **Wait for Processing** - Documents will be indexed automatically
5. **Confirmation** - Receive notification when indexing is complete

### Chat Interface

1. **Select Knowledge Base** - Choose from your available document collections
2. **Start Conversation** - Type your questions in natural language
3. **Receive Answers** - Get responses with source citations
4. **Follow-up Questions** - Continue the conversation contextually

## 🛠️ Troubleshooting

### Common Issues

#### Backend Connection Issues

```bash
# Check if backend is running
curl http://localhost:8000/health

# Verify environment variables
cat backend/.env

# Check backend logs in the terminal running python main.py
```

#### Frontend Not Loading

```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check for port conflicts
# Linux/macOS:
lsof -i :3000
# Windows:
netstat -ano | findstr :3000
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

- • Check supported file formats (PDF, TXT, DOCX)
- • Ensure files are not corrupted
- • Verify sufficient disk space
- • Review backend logs for specific errors

### Performance Optimization

#### For Large Document Collections

- • Increase chunk size in indexing configuration
- • Use GPU acceleration for Ollama if available
- • Consider SSD storage for better I/O performance

#### For Slow Response Times

- • Optimize model selection - smaller models for faster inference
- • Implement caching for frequent queries
- • Use vector database for large-scale deployments

## 🌟 Real-World Use Cases

### Legal Document Analysis

Use Case: Law firm analyzing contract collections

- • Upload: Contract documents, legal precedents
- • Query: "What are the standard termination clauses?"
- • Benefit: Quick access to relevant legal language

### Research Paper Review

Use Case: Academic research across multiple papers

- • Upload: Research papers, academic articles
- • Query: "What methodologies were used in machine learning studies?"
- • Benefit: Comprehensive literature review assistance

### Corporate Knowledge Management

Use Case: Company policy and procedure queries

- • Upload: Employee handbooks, SOPs, training materials
- • Query: "What is the process for requesting time off?"
- • Benefit: Instant access to company information

### Technical Documentation

Use Case: Software development team documentation

- • Upload: API docs, architecture guides, code documentation
- • Query: "How do I implement authentication in the system?"
- • Benefit: Faster developer onboarding and support

## 🙏 Credits and Resources

### Core Technologies

- • **[LlamaIndex](https://llamaindex.ai/)** - Document indexing and retrieval framework
- • **[Ollama](https://ollama.ai/)** - Local LLM runtime and model management
- • **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework for APIs
- • **[React](https://reactjs.org/)** - Frontend user interface library

### Key Dependencies

- • Python Libraries: llama-index, fastapi, uvicorn, python-multipart
- • JavaScript Libraries: react, axios, styled-components

### Learning Resources

- • **[LlamaIndex Documentation](https://docs.llamaindex.ai/)**
- • **[Ollama Model Library](https://ollama.ai/library)**
- • **[RAG Implementation Guide](https://python.langchain.com/docs/use_cases/question_answering)**
- • **[FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)**

### Community and Support

- • GitHub Issues: Report bugs and request features
- • Discussions: Join community discussions for help and ideas
- • Documentation: Check the /docs endpoint for API documentation

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

### License

This project is open source. Please check the LICENSE file for details.

Built with ❤️ for the open source community

For additional support, please open an issue on GitHub or check the documentation at the /docs API endpoint.
