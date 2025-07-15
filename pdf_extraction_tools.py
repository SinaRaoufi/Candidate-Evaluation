import os
import re
import fitz  # PyMuPDF
from typing import List, Dict, Any, Optional
from smolagents import tool
import glob


class PDFExtractor:
    """
    A comprehensive PDF extraction class for processing resumes and documents.
    Extracts text, URLs, contact information, and provides summarization.
    """

    def __init__(self):
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        # Improved phone pattern to handle various formats and spaces
        self.phone_pattern = re.compile(
            r'(\+?\d{1,3}[-.\s]*\d{2,4}[-.\s]*\d{2,4}[-.\s]*\d{2,4})'
        )

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract all text content from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text content as a string
        """
        try:
            doc = fitz.open(pdf_path)
            text = ""

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
                text += "\n\n"  # Add separation between pages

            doc.close()
            return text.strip()
        except Exception as e:
            return f"Error extracting text from {pdf_path}: {str(e)}"

    def extract_urls_from_pdf(self, pdf_path: str) -> List[str]:
        """
        Extract all URLs from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of URLs found in the PDF
        """
        try:
            text = self.extract_text_from_pdf(pdf_path)
            urls = self.url_pattern.findall(text)
            return list(set(urls))  # Remove duplicates
        except Exception as e:
            return [f"Error extracting URLs from {pdf_path}: {str(e)}"]

    def extract_contact_info(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract contact information from a PDF resume.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary containing contact information
        """
        try:
            text = self.extract_text_from_pdf(pdf_path)

            # Extract emails
            all_emails = self.email_pattern.findall(text)

            # Filter emails to prioritize personal emails and exclude university/supervisor emails
            personal_emails = []
            university_keywords = ['uni-', 'university',
                                   'edu', 'ac.', 'informatik', 'cs.']

            for email in all_emails:
                email_lower = email.lower()
                # Check if this is likely a personal email (not university/supervisor)
                is_university = any(
                    keyword in email_lower for keyword in university_keywords)
                if not is_university:
                    personal_emails.append(email)

            # If we found personal emails, use those. Otherwise, fall back to the first email found
            emails_to_use = personal_emails if personal_emails else all_emails[:1]

            # Extract phone numbers with improved pattern
            phones = self.phone_pattern.findall(text)
            # Clean up phone numbers by removing extra spaces
            cleaned_phones = []
            personal_phones = []
            office_phones = []

            for phone in phones:
                cleaned_phone = re.sub(
                    r'\s+', ' ', phone.strip())  # Normalize spaces
                # Ensure it's a complete number
                if len(cleaned_phone.replace(' ', '').replace('-', '').replace('.', '')) >= 10:
                    cleaned_phones.append(cleaned_phone)
                    # Prioritize mobile numbers (usually start with specific patterns)
                    # German mobile numbers typically start with +49 1xx or contain patterns like 176, 177, etc.
                    if any(pattern in cleaned_phone for pattern in ['176', '177', '178', '179', '151', '152', '157', '159']):
                        personal_phones.append(cleaned_phone)
                    else:
                        office_phones.append(cleaned_phone)

            # Prioritize personal phones, fall back to office phones if needed
            phones_to_use = personal_phones if personal_phones else office_phones

            # Extract URLs
            urls = self.url_pattern.findall(text)

            # Improved name extraction - look for name in the first few lines
            lines = text.split('\n')
            potential_name = ""
            for line in lines[:5]:
                line = line.strip()
                if line and len(line.split()) >= 2:  # At least 2 words
                    # Look for lines that could be names
                    words = line.split()
                    if (not any(char.isdigit() for char in line) and
                        '@' not in line and
                        'http' not in line.lower() and
                        not line.lower().endswith(('germany', 'university')) and
                            all(len(word) > 1 for word in words)):  # Each word should be more than 1 character
                        # Remove common titles/suffixes
                        filtered_words = [word for word in words if word.lower() not in [
                            'master', 'of', 'sciences', 'bachelor', 'phd', 'dr.', 'prof.', 'msc', 'bsc', 'msc.', 'bsc.']]
                        # Should have at least first and last name after filtering
                        if len(filtered_words) >= 2:
                            potential_name = ' '.join(filtered_words)
                            break

            return {
                "name": potential_name,
                "emails": list(set(emails_to_use)),
                "phones": list(set(phones_to_use)),
                "urls": list(set(urls)),
                "file_path": pdf_path
            }
        except Exception as e:
            return {
                "error": f"Error extracting contact info from {pdf_path}: {str(e)}",
                "file_path": pdf_path
            }

    def extract_skills_keywords(self, pdf_path: str, skill_keywords: List[str] = None) -> List[str]:
        """
        Extract skills and keywords from a PDF resume.

        Args:
            pdf_path: Path to the PDF file
            skill_keywords: List of skills to search for (optional)

        Returns:
            List of found skills/keywords
        """
        if skill_keywords is None:
            skill_keywords = [
                "python", "java", "javascript", "typescript", "react", "angular", "vue",
                "node.js", "express", "django", "flask", "fastapi", "sql", "mongodb",
                "postgresql", "mysql", "redis", "docker", "kubernetes", "aws", "azure",
                "gcp", "git", "jenkins", "ci/cd", "machine learning", "data science",
                "artificial intelligence", "tensorflow", "pytorch", "pandas", "numpy",
                "html", "css", "bootstrap", "tailwind", "scss", "webpack", "api",
                "rest", "graphql", "microservices", "agile", "scrum", "devops"
            ]

        try:
            text = self.extract_text_from_pdf(pdf_path).lower()
            found_skills = []

            for skill in skill_keywords:
                if skill.lower() in text:
                    found_skills.append(skill)

            return found_skills
        except Exception as e:
            return [f"Error extracting skills from {pdf_path}: {str(e)}"]

    def summarize_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Create a comprehensive summary of a PDF resume.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary containing summary information
        """
        try:
            text = self.extract_text_from_pdf(pdf_path)
            contact_info = self.extract_contact_info(pdf_path)
            skills = self.extract_skills_keywords(pdf_path)

            # Calculate basic statistics
            word_count = len(text.split())
            line_count = len(text.split('\n'))

            # Extract filename
            filename = os.path.basename(pdf_path)

            return {
                "filename": filename,
                "file_path": pdf_path,
                "contact_info": contact_info,
                "skills_found": skills,
                "statistics": {
                    "word_count": word_count,
                    "line_count": line_count,
                    "text_length": len(text)
                },
                "text_preview": text[:500] + "..." if len(text) > 500 else text
            }
        except Exception as e:
            return {
                "filename": os.path.basename(pdf_path),
                "file_path": pdf_path,
                "error": f"Error summarizing {pdf_path}: {str(e)}"
            }


# Initialize the extractor
pdf_extractor = PDFExtractor()


@tool
def list_resume_files() -> str:
    """
    List all available resume files in the resumes directory.

    Returns:
        A formatted string listing all PDF files in the resumes directory
    """
    resumes_dir = "./resumes"

    if not os.path.exists(resumes_dir):
        return "Error: resumes directory does not exist."

    pdf_files = glob.glob(os.path.join(resumes_dir, "*.pdf"))

    if not pdf_files:
        return "No PDF files found in the resumes directory."

    result = f"📁 Available Resume Files in {resumes_dir}:\n"
    result += "=" * 40 + "\n"

    for i, pdf_path in enumerate(pdf_files, 1):
        filename = os.path.basename(pdf_path)
        result += f"{i}. {filename}\n"

    result += f"\nTotal: {len(pdf_files)} resume files\n"
    result += "\nTo access a file, use: resumes/filename.pdf"

    return result


@tool
def get_resume_filenames() -> str:
    """
    Get a simple list of resume filenames for processing.

    Returns:
        A formatted string with just the filenames, one per line
    """
    resumes_dir = "./resumes"

    if not os.path.exists(resumes_dir):
        return "Error: resumes directory does not exist."

    pdf_files = glob.glob(os.path.join(resumes_dir, "*.pdf"))

    if not pdf_files:
        return "No PDF files found in the resumes directory."

    filenames = [os.path.basename(pdf_path) for pdf_path in pdf_files]
    return "\n".join(filenames)


@tool
def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract all text content from a PDF file.

    Args:
        pdf_path: Path to the PDF file (relative or absolute)

    Returns:
        The extracted text content from the PDF
    """
    if not os.path.isabs(pdf_path):
        # Handle relative paths
        if not pdf_path.startswith('./'):
            pdf_path = './' + pdf_path

    if not os.path.exists(pdf_path):
        return f"Error: File {pdf_path} does not exist."

    return pdf_extractor.extract_text_from_pdf(pdf_path)


@tool
def extract_pdf_urls(pdf_path: str) -> str:
    """
    Extract all URLs from a PDF file.

    Args:
        pdf_path: Path to the PDF file (relative or absolute)

    Returns:
        A formatted string listing all URLs found in the PDF
    """
    if not os.path.isabs(pdf_path):
        if not pdf_path.startswith('./'):
            pdf_path = './' + pdf_path

    if not os.path.exists(pdf_path):
        return f"Error: File {pdf_path} does not exist."

    urls = pdf_extractor.extract_urls_from_pdf(pdf_path)

    if not urls:
        return f"No URLs found in {pdf_path}"

    result = f"URLs found in {os.path.basename(pdf_path)}:\n"
    for i, url in enumerate(urls, 1):
        result += f"{i}. {url}\n"

    return result


@tool
def extract_pdf_contact_info(pdf_path: str) -> str:
    """
    Extract contact information (name, email, phone, URLs) from a PDF resume.

    Args:
        pdf_path: Path to the PDF file (relative or absolute)

    Returns:
        A formatted string with contact information
    """
    if not os.path.isabs(pdf_path):
        if not pdf_path.startswith('./'):
            pdf_path = './' + pdf_path

    if not os.path.exists(pdf_path):
        return f"Error: File {pdf_path} does not exist."

    contact_info = pdf_extractor.extract_contact_info(pdf_path)

    if "error" in contact_info:
        return contact_info["error"]

    result = f"Contact Information from {os.path.basename(pdf_path)}:\n"
    result += f"Name: {contact_info.get('name', 'Not found')}\n"

    if contact_info.get('emails'):
        result += f"Emails: {', '.join(contact_info['emails'])}\n"
    else:
        result += "Emails: Not found\n"

    if contact_info.get('phones'):
        result += f"Phones: {', '.join(contact_info['phones'])}\n"
    else:
        result += "Phones: Not found\n"

    if contact_info.get('urls'):
        result += f"URLs: {', '.join(contact_info['urls'])}\n"
    else:
        result += "URLs: Not found\n"

    return result


@tool
def summarize_pdf(pdf_path: str) -> str:
    """
    Create a comprehensive summary of a PDF resume including contact info, skills, and statistics.

    Args:
        pdf_path: Path to the PDF file (relative or absolute)

    Returns:
        A formatted string with comprehensive PDF summary
    """
    if not os.path.isabs(pdf_path):
        if not pdf_path.startswith('./'):
            pdf_path = './' + pdf_path

    if not os.path.exists(pdf_path):
        return f"Error: File {pdf_path} does not exist."

    summary = pdf_extractor.summarize_pdf(pdf_path)

    if "error" in summary:
        return summary["error"]

    result = f"📄 SUMMARY: {summary['filename']}\n"
    result += "=" * 50 + "\n"

    # Contact Information
    contact = summary['contact_info']
    result += "👤 CONTACT INFORMATION:\n"
    result += f"  Name: {contact.get('name', 'Not found')}\n"
    result += f"  Emails: {', '.join(contact.get('emails', [])) or 'Not found'}\n"
    result += f"  Phones: {', '.join(contact.get('phones', [])) or 'Not found'}\n"
    result += f"  URLs: {', '.join(contact.get('urls', [])) or 'Not found'}\n\n"

    # Skills
    result += "🛠️ SKILLS IDENTIFIED:\n"
    skills = summary.get('skills_found', [])
    if skills:
        result += f"  {', '.join(skills[:15])}"  # Show first 15 skills
        if len(skills) > 15:
            result += f" (+{len(skills) - 15} more)"
        result += "\n\n"
    else:
        result += "  No technical skills identified\n\n"

    # Statistics
    stats = summary['statistics']
    result += "📊 DOCUMENT STATISTICS:\n"
    result += f"  Word Count: {stats['word_count']}\n"
    result += f"  Lines: {stats['line_count']}\n"
    result += f"  Characters: {stats['text_length']}\n\n"

    # Preview
    result += "📝 TEXT PREVIEW:\n"
    result += summary['text_preview']

    return result


@tool
def summarize_all_pdfs_in_directory(directory_path: str) -> str:
    """
    Create summaries of all PDF files in a specified directory.

    Args:
        directory_path: Path to the directory containing PDF files

    Returns:
        A formatted string with summaries of all PDFs in the directory
    """
    if not os.path.isabs(directory_path):
        if not directory_path.startswith('./'):
            directory_path = './' + directory_path

    if not os.path.exists(directory_path):
        return f"Error: Directory {directory_path} does not exist."

    if not os.path.isdir(directory_path):
        return f"Error: {directory_path} is not a directory."

    # Find all PDF files in the directory
    pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
    print(pdf_files)
    if not pdf_files:
        return f"No PDF files found in {directory_path}"

    result = f"📁 SUMMARY OF ALL PDFs IN: {directory_path}\n"
    result += "=" * 60 + "\n"
    result += f"Found {len(pdf_files)} PDF files\n\n"

    for i, pdf_path in enumerate(pdf_files, 1):
        result += f"📄 {i}. {os.path.basename(pdf_path)}\n"
        result += "-" * 40 + "\n"

        summary = pdf_extractor.summarize_pdf(pdf_path)

        if "error" in summary:
            result += f"❌ Error: {summary['error']}\n\n"
            continue

        # Contact Information
        contact = summary['contact_info']
        result += f"👤 Name: {contact.get('name', 'Not found')}\n"
        result += f"📧 Email: {', '.join(contact.get('emails', [])) or 'Not found'}\n"
        result += f"📞 Phone: {', '.join(contact.get('phones', [])) or 'Not found'}\n"

        # URLs
        urls = contact.get('urls', [])
        if urls:
            result += f"🔗 URLs: {', '.join(urls)}\n"

        # Skills (show top 10)
        skills = summary.get('skills_found', [])
        if skills:
            top_skills = skills[:10]
            result += f"🛠️ Skills: {', '.join(top_skills)}"
            if len(skills) > 10:
                result += f" (+{len(skills) - 10} more)"
            result += "\n"

        # Stats
        stats = summary['statistics']
        result += f"📊 Words: {stats['word_count']}, Lines: {stats['line_count']}\n"

        result += "\n"

    return result


@tool
def search_pdfs_for_skill(directory_path: str, skill: str) -> str:
    """
    Search all PDF files in a directory for a specific skill or keyword.

    Args:
        directory_path: Path to the directory containing PDF files
        skill: The skill or keyword to search for

    Returns:
        A formatted string showing which PDFs contain the skill
    """
    if not os.path.isabs(directory_path):
        if not directory_path.startswith('./'):
            directory_path = './' + directory_path

    if not os.path.exists(directory_path):
        return f"Error: Directory {directory_path} does not exist."

    # Find all PDF files in the directory
    pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))

    if not pdf_files:
        return f"No PDF files found in {directory_path}"

    skill_lower = skill.lower()
    matches = []

    for pdf_path in pdf_files:
        try:
            text = pdf_extractor.extract_text_from_pdf(pdf_path).lower()
            if skill_lower in text:
                # Count occurrences
                count = text.count(skill_lower)
                matches.append({
                    "file": os.path.basename(pdf_path),
                    "path": pdf_path,
                    "count": count
                })
        except Exception as e:
            continue

    if not matches:
        return f"No PDFs found containing '{skill}' in {directory_path}"

    # Sort by occurrence count
    matches.sort(key=lambda x: x['count'], reverse=True)

    result = f"🔍 SEARCH RESULTS FOR '{skill}' IN: {directory_path}\n"
    result += "=" * 60 + "\n"
    result += f"Found '{skill}' in {len(matches)} out of {len(pdf_files)} PDFs:\n\n"

    for i, match in enumerate(matches, 1):
        result += f"{i}. {match['file']} ({match['count']} occurrences)\n"

    return result
