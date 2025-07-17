# AI Agent for optimizing candidate evaluation

**Course Project for Dialogue Systems (DIALOGUE SYSTEMS) - University of Bonn**

This project was developed as part of the Dialogue Systems course at the University of Bonn, taught by **[Prof. Dr. Lucie Flek](https://scholar.google.de/citations?user=qZCZFp0AAAAJ&hl=en)** and **[Dr. Akbar Karimi](https://scholar.google.com/citations?user=_qroDmEAAAAJ&hl=en)**. For more information about the course, visit: [Dialogue Systems Course](https://www.b-it-center.de/caisa/teaching/dialogsys)

---

An intelligent AI agent built with [smolagents](https://github.com/huggingface/smolagents) that processes PDF resumes, extracts detailed candidate information, and ranks candidates for job positions using advanced AI analysis.

## 🚀 Key Features

### PDF Resume Processing
- **Complete Text Extraction**: Extract all text content from PDF resumes
- **Contact Information Extraction**: Automatically extract names, emails, phone numbers
- **Platform URL Detection**: Find GitHub, LinkedIn, Google Scholar profiles
- **Smart Summarization**: AI-powered resume summaries with key highlights
- **Skill Search**: Search across all PDFs for specific skills or technologies
- **Batch Processing**: Analyze entire directories of resumes at once

### Candidate Ranking & Analysis
- **Intelligent Candidate Ranking**: Multi-criteria evaluation algorithm
- **Skills Matching**: Required vs preferred skills analysis
- **Experience Assessment**: Years of experience vs job requirements
- **Education Scoring**: Degree level and field relevance evaluation
- **Role Relevance Analysis**: Previous roles matching job requirements
- **Detailed Explanations**: Comprehensive breakdown of ranking decisions

### Email Integration
- **Gmail API Integration**: Fetch recent emails for candidate communication
- **Email Processing**: Convert email attachments to searchable formats

### AI-Powered Interface
- **Natural Language Interaction**: Conversational queries and responses
- **Human-Readable Output**: All responses formatted for easy reading
- **Interactive Terminal**: Real-time processing with streaming outputs
- **Multiple Model Support**: HuggingFace API, LiteLLM, local models


## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Choose Your AI Model Setup

#### Option A: HuggingFace API (Recommended)
1. Get a free token from [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Create a `.env` file in the project root:
```bash
HF_TOKEN=your_token_here
```

#### Option B: Local Ollama
1. Install [Ollama](https://ollama.com/)
2. Pull the model: `ollama pull qwen2.5-coder:32b`
3. Start the server: `ollama serve`

#### Option C: Other API Providers
Set appropriate environment variables for OpenAI, Anthropic, or other LiteLLM-supported providers.

### 3. (Optional) Gmail Integration Setup
For email functionality:
1. Enable Gmail API in Google Cloud Console
2. Download `credentials.json` to project root
3. Run the app - it will guide you through OAuth flow

### 4. Run the System

```bash
python main.py
```

## 🎯 Usage Examples

### Interactive Mode Commands

**Resume Analysis:**
```
🔍 Your request: Show me all available resume files
🔍 Your request: Summarize all PDFs in the resumes directory  
🔍 Your request: Extract contact information from resumes/CV_Yihang_Chen.pdf
🔍 Your request: Find all resumes containing Python skills
🔍 Your request: Get GitHub and LinkedIn URLs from all resumes
```

**Candidate Ranking:**
```
🔍 Your request: Give me the 3 best fit candidates for job 1
🔍 Your request: Show me all available jobs
🔍 Your request: Rank all candidates for the Data Scientist position
🔍 Your request: Compare candidates for the backend developer role
```

**Advanced Queries:**
```
🔍 Your request: Which candidates have machine learning experience?
🔍 Your request: Summarize the background of Yihang Chen
🔍 Your request: Find candidates suitable for startup environments
```

### Command Line Mode
```bash
python main.py "Summarize all resumes and rank them for job 1"
python main.py "Extract all contact information from the resumes"
```

### Sample Output

```
🔍 Your request: Give me the 3 best fit candidates for job 1

🤖 Processing: Give me the 3 best fit candidates for job 1
----------------------------------------

📋 Response:
Job: Senior Data Scientist at TechCorp
Required Skills: Python, Machine Learning, Statistics, TensorFlow, Data Analysis

🏆 Top 3 Candidates:
==================================================

🏆 Rank #1: Yihang Chen
📧 Email: yihang.chen@example.com
⭐ Overall Match Score: 87.5% (Excellent Match)

📊 Detailed Evaluation:
🛠️ Skills Match: 92% - Found 4 out of 5 required skills, plus 2 preferred skills
💼 Experience: 85% - 6 years experience (exceeds 4 year requirement)
🎓 Education: 90% - PhD in Computer Science with AI specialization
🔗 Platform Links: GitHub: github.com/yihangchen, LinkedIn: linkedin.com/in/yihangchen

Key Highlights: Extensive machine learning background, published research in NLP, 
experience with TensorFlow and PyTorch, strong statistical analysis skills...
```

## 🚨 Troubleshooting

### Common Issues

1. **PDF Processing Errors**: Ensure PDFs are not password-protected or corrupted
2. **No model available**: Check HuggingFace token or Ollama installation
3. **Gmail API errors**: Verify credentials.json and complete OAuth flow
4. **Import errors**: Run `pip install -r requirements.txt`

### Error Messages


- `❌ Gmail API setup failed`: Check credentials.json and internet connection
- `❌ HuggingFace API setup failed`: Verify HF_TOKEN is valid



## 🙏 Acknowledgments

- Built with [smolagents](https://github.com/huggingface/smolagents) by HuggingFace
- PDF processing powered by [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
- Gmail integration via Google APIs
- AI models from HuggingFace, Ollama, and other providers 