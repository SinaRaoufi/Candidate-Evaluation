#!/usr/bin/env python3
"""
AI Agent for Candidate Ranking using smolagents

This program creates an AI agent that can rank candidates for job descriptions
based on various criteria including skills, experience, education, and role relevance.

Usage:
    python main.py

Then interact with the agent through the terminal interface.
"""
from pdf_extraction_tools import (
    extract_pdf_text,
    extract_pdf_urls,
    extract_pdf_contact_info,
    summarize_pdf,
    summarize_all_pdfs_in_directory,
    search_pdfs_for_skill,
    list_resume_files,
    get_resume_filenames
)
from candidate_ranking_tool import (
    rank_candidates_for_job,
    list_available_jobs,
    get_job_details,
    search_candidates_by_skill
)
from fetch_emails_tool import fetch_recent_emails
from smolagents import CodeAgent, InferenceClientModel, LiteLLMModel, TransformersModel
from dotenv import load_dotenv
from typing import Optional
import sys
import os
from pydantic.warnings import PydanticDeprecatedSince20
import warnings
warnings.filterwarnings("ignore")

# Suppress Pydantic v2-specific deprecation warnings
warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)

# Suppress other deprecated API usage (e.g., httpx)

# Load environment variables
load_dotenv()


class CandidateRankingAgent:
    """
    Main agent class that handles candidate ranking operations.
    """

    def __init__(self):
        self.agent = None
        self.model = None
        self.setup_model()
        self.setup_agent()

    def setup_model(self):
        """
        Set up the language model for the agent.
        Priority: HuggingFace API > LiteLLM > Local Transformers
        """
        try:
            # Try HuggingFace API first (recommended)
            hf_token = os.getenv("HF_TOKEN")
            if hf_token:
                print("🔧 Setting up HuggingFace API model...")
                self.model = InferenceClientModel(
                    model_id="qwen2.5-coder:7b",
                    token=hf_token
                )
                # check if it is working
                test_response = self.model.invoke("Hello", max_tokens=5)
                if not test_response or "error" in str(test_response).lower():
                    raise Exception(
                        "Hugging Face API is unavailable or quota exceeded.")

                print("✅ HuggingFace API model ready!")
                return
        except Exception as e:
            print(f"❌ HuggingFace API setup failed: {e}")

        try:
            # Try LiteLLM with local models (ollama)
            print("🔧 Setting up LiteLLM model (trying local ollama)...")
            self.model = LiteLLMModel(
                model_id="ollama/qwen2.5-coder:7b",
                system_message="""
You are a helpful AI assistant specialized in candidate ranking and PDF analysis.

CRITICAL RULES:
1. ALWAYS use <code> and </code> tags when calling tools
2. When a tool call produces output, that output IS your final answer - do NOT continue with more steps
3. Only call ONE tool per response unless explicitly asked to do multiple things
4. Do NOT create loops or repetitive calls

REQUIRED FORMAT:
Thought: [Brief explanation of what you'll do]

<code>
[Single tool call here]
</code>

AVAILABLE TOOLS:
- list_available_jobs(): Lists all job descriptions with their IDs
- get_job_details(job_id): Get detailed information about a specific job  
- rank_candidates_for_job(job_id, candidates_data, top_n): Rank candidates for a job
- search_candidates_by_skill(skill, candidates_data): Find candidates with specific skills
- extract_pdf_text(file_path): Extract text from a PDF
- summarize_pdf(file_path): Summarize a PDF resume
- summarize_all_pdfs_in_directory(directory): Summarize all PDFs in a directory
- search_pdfs_for_skill(directory, skill): Search PDFs for specific skills
- list_resume_files(): List all available resume files in the resumes directory
- get_resume_filenames(): Get just the filenames for processing
- fetch_recent_emails(): Fetch recent emails

IMPORTANT: All candidate resumes are located in the "./resumes" directory. When working with candidate data:
- Use "resumes" or "./resumes" as the directory path for PDF operations
- Always use the correct file paths like "resumes/CV_Yihang_Chen.pdf"

EXAMPLES:

User: "List available jobs"
Response:
Thought: I'll list all available job descriptions.

<code>
list_available_jobs()
</code>

User: "Summarize all resumes"  
Response:
Thought: I'll summarize all PDFs in the resumes directory.

<code>
summarize_all_pdfs_in_directory("resumes")
</code>

User: "Extract contact info from Yihang Chen's resume"
Response:
Thought: I'll extract contact information from the specified resume.

<code>
extract_pdf_contact_info("resumes/CV_Yihang_Chen.pdf")
</code>

User: "What resume files are available?"
Response:
Thought: I'll list all available resume files.

<code>
list_resume_files()
</code>

User: "Give me a list of candidates"  
Response:
Thought: I'll get all candidate information by summarizing all resumes in the directory.

<code>
summarize_all_pdfs_in_directory("resumes")
</code>

IMPORTANT: After the tool executes and produces output, STOP. That output is your final answer.
""",
                allow_all_imports=True,
                additional_authorized_imports=[
                    "os", "pdf_tools", "candidate_ranking_tool", "glob"]
            )
            print("✅ LiteLLM model ready!")
            return
        except Exception as e:
            print(f"❌ LiteLLM setup failed: {e}")

        try:
            # Fallback to local Transformers model
            print("🔧 Setting up local Transformers model...")
            self.model = TransformersModel(
                model_id="microsoft/DialoGPT-medium"
            )
            print("✅ Local Transformers model ready!")
            return
        except Exception as e:
            print(f"❌ Transformers setup failed: {e}")

        print("❌ Could not set up any model. Please check your configuration.")
        sys.exit(1)

    def setup_agent(self):
        """
        Set up the agent with our custom tools.
        """
        print("🔧 Setting up agent with candidate ranking tools...")

        # Custom tools for candidate ranking and PDF processing
        tools = [
            rank_candidates_for_job,
            list_available_jobs,
            get_job_details,
            search_candidates_by_skill,
            extract_pdf_text,
            extract_pdf_urls,
            extract_pdf_contact_info,
            summarize_pdf,
            summarize_all_pdfs_in_directory,
            search_pdfs_for_skill,
            list_resume_files,
            get_resume_filenames,
            fetch_recent_emails
        ]

        self.agent = CodeAgent(
            tools=tools,
            model=self.model,
            add_base_tools=True,  # Add default tools like web search
            stream_outputs=True   # Enable streaming for better user experience

        )

        print("✅ Agent ready with candidate ranking and PDF extraction capabilities!")

    def run_interactive_session(self):
        """
        Run an interactive session with the agent.
        """
        print("\n" + "="*60)
        print("🤖 AI CANDIDATE RANKING AGENT")
        print("="*60)
        print("\nWelcome! I can help you rank candidates and extract information from PDF resumes.")
        print("\nWhat I can do:")
        print("• Rank candidates for specific job descriptions")
        print("• Extract text, URLs, and contact info from PDF resumes")
        print("• Summarize individual PDFs or entire directories")
        print("• Search PDFs for specific skills or keywords")
        print("• List available resume files and job descriptions")
        print("• Search candidates by skills")

        print("\nSample commands you can try:")
        print("• 'Show me all available resume files'")
        print("• 'Give me a summary of all PDFs in the resumes directory'")
        print("• 'Extract contact information from resumes/CV_Yihang_Chen.pdf'")
        print("• 'Find all PDFs containing Python in the resumes folder'")
        print("• 'Summarize the resume resumes/CV_Wasim_SyedTalal.pdf'")
        print("• 'Give me the 3 best fit candidates for job 1'")
        print("• 'Show me all available jobs'")

        print("\nType 'quit' or 'exit' to end the session.")
        print("-" * 60)

        while True:
            try:
                user_input = input("\n🔍 Your request: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thank you for using the AI Candidate Ranking Agent!")
                    break

                if not user_input:
                    print("Please enter a request or 'quit' to exit.")
                    continue

                print(f"\n🤖 Processing: {user_input}")
                print("-" * 40)

                # Run the agent
                response = self.agent.run(user_input)

                print(f"\n📋 Response:\n{response}")
                print("-" * 60)

            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'quit' to exit.")

    def run_single_query(self, query: str) -> str:
        """
        Run a single query and return the response.

        Args:
            query: The user query

        Returns:
            The agent's response
        """
        try:
            return self.agent.run(query)
        except Exception as e:
            return f"Error processing query: {e}"


def print_setup_instructions():
    """
    Print setup instructions for the user.
    """
    print("\n" + "="*60)
    print("🚀 SETUP INSTRUCTIONS")
    print("="*60)
    print("\nFor the best experience, set up your environment:")
    print("\n1. HuggingFace API (Recommended):")
    print("   - Get a free token from https://huggingface.co/settings/tokens")
    print("   - Set HF_TOKEN environment variable or create .env file:")
    print("     HF_TOKEN=your_token_here")

    print("\n2. Alternative: Local Ollama")
    print("   - Install Ollama: https://ollama.com/")
    print("   - Run: ollama pull qwen2.5-coder:7b")
    print("   - Start ollama server: ollama serve")

    print("\n3. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n" + "="*60)


def main():
    """
    Main entry point for the application.
    """
    print("🚀 Starting AI Candidate Ranking Agent...")

    # Check if we have any model configuration
    if not os.getenv("HF_TOKEN"):
        print("\n⚠️  No HuggingFace token found. The agent will try alternative models.")
        print("For best results, please set up a HuggingFace API token.")
        print_setup_instructions()

        # Ask user if they want to continue
        continue_anyway = input(
            "\nContinue without HuggingFace token? (y/n): ").lower()
        if continue_anyway != 'y':
            print("Please set up your environment and try again.")
            sys.exit(0)

    try:
        # Initialize the agent
        agent = CandidateRankingAgent()

        # Check if running with command line arguments
        if len(sys.argv) > 1:
            # Run single query from command line
            query = " ".join(sys.argv[1:])
            response = agent.run_single_query(query)
            print(f"\n📋 Response:\n{response}")
        else:
            # Run interactive session
            agent.run_interactive_session()

    except Exception as e:
        print(f"\n❌ Failed to start agent: {e}")
        print("\nPlease check your setup and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
