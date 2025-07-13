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
    search_pdfs_for_skill
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
You are a coding assistant that MUST always reply using this EXACT format:

REQUIRED FORMAT:
Thought: [Explain what you're going to do]

<code>
[Your Python code here]
final_answer([your result])
</code>

CRITICAL RULES:
1. ALWAYS use <code> and </code> tags (NOT markdown code blocks like ```python)
2. ALWAYS end with final_answer([result]) inside the <code> block
3. NEVER use variables that weren't defined in the code block
4. NEVER return code outside <code>...</code> tags

EXAMPLE:
Thought: I will create a greeting message and return it.

<code>
greeting = "Hello! How can I assist you today?"
final_answer(greeting)
</code>

TOOLS AVAILABLE:
- fetch_recent_emails: Fetch emails from inbox
- PDF tools: extract_pdf_text, summarize_pdf, search_pdfs_for_skill
- Candidate ranking: rank_candidates_for_job, list_available_jobs, get_job_details

WORKFLOW EXAMPLE:
Thought: I will fetch emails and then analyze PDFs in the resumes folder.

<code>
emails = fetch_recent_emails()
pdf_summaries = summarize_all_pdfs_in_directory("resumes")
final_answer(pdf_summaries)
</code>
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
        print("• List available sample jobs and get job details")
        print("• Search candidates by skills")

        print("\nSample commands you can try:")
        print("• 'Give me a summary of all PDFs in the resumes directory'")
        print("• 'Extract contact information from resumes/10228751.pdf'")
        print("• 'Find all PDFs containing Python in the resumes folder'")
        print("• 'Summarize the resume resumes/11676151.pdf'")
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
