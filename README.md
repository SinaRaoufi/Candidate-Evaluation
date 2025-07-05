# AI Candidate Ranking Agent

An intelligent AI agent built with [smolagents](https://github.com/huggingface/smolagents) that ranks candidates for job descriptions based on multiple criteria including skills, experience, education, and role relevance.

## 🚀 Features

- **Smart Candidate Ranking**: Evaluates candidates using a comprehensive scoring algorithm
- **Multiple Evaluation Criteria**: 
  - Skills matching (required vs preferred)
  - Experience level assessment
  - Education qualification scoring
  - Role relevance analysis
- **Interactive Terminal Interface**: Natural language interaction with the agent
- **Multiple Model Support**: HuggingFace Inference API, LiteLLM, and local Transformers
- **Detailed Explanations**: Provides breakdown of why candidates are ranked as they are
- **Flexible Queries**: Support for various types of requests and questions

## 📋 What the Agent Can Do

The agent can handle requests like:
- "Give me the 3 best fit candidates for job 1"
- "Show me all available jobs"
- "Find candidates with Python skills"
- "Who are the top 5 candidates for the Senior Data Scientist role?"
- "Get details for job 2"
- "Compare candidates Alice and Bob for the backend developer position"

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Choose Your Model Setup

#### Option A: HuggingFace API (Recommended)
1. Get a free token from [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Create a `.env` file in the project root:
```bash
HF_TOKEN=your_token_here
```

#### Option B: Local Ollama
1. Install [Ollama](https://ollama.com/)
2. Pull a model: `ollama pull llama3.2`
3. Start the server: `ollama serve`

#### Option C: Other API Providers
You can also use OpenAI, Anthropic, or other providers supported by LiteLLM. Set the appropriate environment variables in your `.env` file.

### 3. Run the Agent

```bash
python main.py
```

## 🎯 Usage Examples

### Interactive Mode
```bash
python main.py
```

Then interact with the agent:
```
🔍 Your request: Give me the 3 best fit candidates for job 1

🤖 Processing: Give me the 3 best fit candidates for job 1
----------------------------------------

📋 Response:
Job: Senior Data Scientist at TechCorp
Required Skills: Python, Machine Learning, Statistics, TensorFlow, Data Analysis
Minimum Experience: 4 years

Top 3 Candidates:
==================================================

Rank #1: Alice Johnson
Email: alice.johnson@email.com
Overall Score: 0.89/1.00

Score Breakdown:
• Skills Match: 0.94/1.00 (5/5 required, 1/5 preferred)
• Experience: 0.90/1.00 (5 years vs 4 required)
• Education: 0.90/1.00 (MS Computer Science)
• Role Relevance: 0.80/1.00 (2 matching roles)

Key Skills: Python, Machine Learning, Data Science, SQL, TensorFlow
Previous Roles: Data Scientist, ML Engineer
Summary: Experienced data scientist with 5 years of experience in machine learning and data analysis...
```

### Command Line Mode
```bash
python main.py "Show me all available jobs"
python main.py "Find candidates with Python skills"
```

## 🏗️ Architecture

### Components

1. **`main.py`**: Entry point and agent orchestration
2. **`candidate_ranking_tool.py`**: Core ranking logic and smolagents tools
3. **`candidate_data.py`**: Sample data (candidates and job descriptions)
4. **`requirements.txt`**: Python dependencies

### Ranking Algorithm

The system uses a weighted scoring algorithm:

- **Skills Match (40%)**: Required skills vs preferred skills
- **Experience (25%)**: Years of experience vs minimum requirements
- **Education (20%)**: Degree level and field relevance
- **Role Relevance (15%)**: Previous roles matching job title

### Tools Available to the Agent

- `rank_candidates_for_job`: Main ranking function
- `list_available_jobs`: Shows available job descriptions
- `get_job_details`: Detailed information about specific jobs
- `search_candidates_by_skill`: Find candidates with specific skills
- Plus default smolagents tools (web search, Python interpreter, etc.)

## 📊 Sample Data

The system comes with sample data including:

### Candidates (8 total)
- Alice Johnson (Data Scientist, 5 years)
- Bob Smith (Frontend Developer, 3 years)
- Carol Davis (Backend Developer, 7 years)
- David Wilson (Python Developer, 4 years)
- Emma Brown (Data Analyst, 6 years)
- Frank Miller (Systems Engineer, 8 years)
- Grace Lee (UI/UX Designer, 4 years)
- Henry Chen (DevOps Engineer, 5 years)

### Job Descriptions (5 total)
1. Senior Data Scientist at TechCorp
2. Frontend Developer at WebTech Solutions
3. Backend Software Engineer at Enterprise Systems Inc
4. Python Developer at StartupTech
5. DevOps Engineer at CloudFirst

## 🔧 Customization

### Adding New Candidates
Edit `candidate_data.py` and add new entries to the `CANDIDATES` list:

```python
{
    "id": 9,
    "name": "New Candidate",
    "email": "new.candidate@email.com",
    "skills": ["Skill1", "Skill2", "Skill3"],
    "experience_years": 5,
    "education": "MS Computer Science",
    "previous_roles": ["Role1", "Role2"],
    "certifications": ["Cert1", "Cert2"],
    "summary": "Brief summary of the candidate..."
}
```

### Adding New Job Descriptions
Edit `candidate_data.py` and add new entries to the `SAMPLE_JOB_DESCRIPTIONS` list:

```python
{
    "id": 6,
    "title": "New Job Title",
    "company": "Company Name",
    "description": "Job description...",
    "required_skills": ["Skill1", "Skill2"],
    "preferred_skills": ["Skill3", "Skill4"],
    "min_experience": 3,
    "education_requirements": "BS in Computer Science",
    "responsibilities": ["Responsibility1", "Responsibility2"]
}
```

### Modifying Scoring Weights
Edit the `rank_candidates` method in `candidate_ranking_tool.py` to adjust the weight distribution:

```python
overall_score = (
    skills_score * 0.4 +           # 40% weight on skills
    experience_score * 0.25 +      # 25% weight on experience
    education_score * 0.20 +       # 20% weight on education
    role_relevance_score * 0.15    # 15% weight on role relevance
)
```

## 🚨 Troubleshooting

### Common Issues

1. **No model available**: Make sure you have either a HuggingFace token or Ollama installed
2. **Import errors**: Run `pip install -r requirements.txt`
3. **Permission errors**: Make sure `main.py` is executable: `chmod +x main.py`

### Error Messages

- `❌ Could not set up any model`: Check your model configuration (HF token, Ollama, etc.)
- `❌ HuggingFace API setup failed`: Verify your HF_TOKEN is valid and has the right permissions
- `❌ LiteLLM setup failed`: Make sure Ollama is running if using local models

## 🤝 Contributing

Feel free to contribute by:
1. Adding more sophisticated ranking algorithms
2. Implementing support for custom job descriptions (not just sample data)
3. Adding more evaluation criteria
4. Improving the UI/UX
5. Adding support for more LLM providers

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [smolagents](https://github.com/huggingface/smolagents) by HuggingFace
- Uses various open-source models and APIs
- Inspired by modern AI agent architectures 