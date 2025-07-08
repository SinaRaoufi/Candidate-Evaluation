#!/usr/bin/env python3
"""
AI Agent for Candidate Ranking using smolagents

This program creates an AI agent that can rank candidates for job descriptions
based on various criteria including skills, experience, education, and role relevance.

Usage:
    python main.py

Then interact with the agent through the terminal interface.
"""

import os
import sys
from typing import Optional
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel, LiteLLMModel, TransformersModel
from candidate_ranking_tool import (
    rank_candidates_for_job,
    list_available_jobs,
    get_job_details,
    search_candidates_by_skill
)
from pdf_extraction_tools import (
    extract_pdf_text,
    extract_pdf_urls,
    extract_pdf_contact_info,
    summarize_pdf,
    summarize_all_pdfs_in_directory,
    search_pdfs_for_skill
)

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
                    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
                    token=hf_token
                )
                print("✅ HuggingFace API model ready!")
                return
        except Exception as e:
            print(f"❌ HuggingFace API setup failed: {e}")

        try:
            # Try LiteLLM with local models (ollama)
            print("🔧 Setting up LiteLLM model (trying local ollama)...")
            self.model = LiteLLMModel(
                model_id="ollama_chat/llama3.2",
                api_key="ollama"
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
            search_pdfs_for_skill
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
    print("   - Run: ollama pull llama3.2")
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
