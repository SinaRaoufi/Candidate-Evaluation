from typing import List, Dict, Any, Tuple
import json
from smolagents import tool
from candidate_data import CANDIDATES, SAMPLE_JOB_DESCRIPTIONS


class CandidateRanker:
    """
    A comprehensive candidate ranking system that evaluates candidates
    based on multiple criteria including skills, experience, education, and relevance.
    """

    def __init__(self):
        self.candidates = CANDIDATES
        self.job_descriptions = SAMPLE_JOB_DESCRIPTIONS

    def calculate_skills_match(self, candidate_skills: List[str],
                               required_skills: List[str],
                               preferred_skills: List[str]) -> Tuple[float, Dict]:
        """
        Calculate skills match score based on required and preferred skills.
        Returns a score between 0 and 1 and detailed breakdown.
        """
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        preferred_skills_lower = [skill.lower() for skill in preferred_skills]

        # Calculate required skills match
        required_matches = sum(1 for skill in required_skills_lower
                               if skill in candidate_skills_lower)
        required_score = required_matches / \
            len(required_skills_lower) if required_skills_lower else 0

        # Calculate preferred skills match
        preferred_matches = sum(1 for skill in preferred_skills_lower
                                if skill in candidate_skills_lower)
        preferred_score = preferred_matches / \
            len(preferred_skills_lower) if preferred_skills_lower else 0

        # Weighted average (required skills are more important)
        overall_score = (required_score * 0.7) + (preferred_score * 0.3)

        breakdown = {
            "required_matches": required_matches,
            "required_total": len(required_skills_lower),
            "required_score": required_score,
            "preferred_matches": preferred_matches,
            "preferred_total": len(preferred_skills_lower),
            "preferred_score": preferred_score,
            "overall_score": overall_score
        }

        return overall_score, breakdown

    def calculate_experience_score(self, candidate_experience: int,
                                   min_experience: int) -> Tuple[float, Dict]:
        """
        Calculate experience score based on minimum requirements.
        Returns a score between 0 and 1 and explanation.
        """
        if candidate_experience >= min_experience:
            # Bonus for extra experience, but with diminishing returns
            extra_years = candidate_experience - min_experience
            bonus = min(extra_years * 0.1, 0.3)  # Max 30% bonus
            score = min(1.0, 0.8 + bonus)
        else:
            # Penalty for insufficient experience
            shortage = min_experience - candidate_experience
            penalty = shortage * 0.2
            score = max(0.0, 0.8 - penalty)

        breakdown = {
            "candidate_experience": candidate_experience,
            "min_required": min_experience,
            "meets_requirement": candidate_experience >= min_experience,
            "score": score
        }

        return score, breakdown

    def calculate_education_score(self, candidate_education: str,
                                  education_requirements: str) -> Tuple[float, Dict]:
        """
        Calculate education score based on degree level and field relevance.
        Returns a score between 0 and 1 and explanation.
        """
        education_mapping = {
            "phd": 4, "doctorate": 4,
            "ms": 3, "master": 3, "masters": 3,
            "bs": 2, "bachelor": 2, "bachelors": 2,
            "associate": 1, "diploma": 1
        }

        # Extract degree level from candidate education
        candidate_level = 0
        for degree, level in education_mapping.items():
            if degree in candidate_education.lower():
                candidate_level = max(candidate_level, level)

        # Extract required degree level
        required_level = 0
        for degree, level in education_mapping.items():
            if degree in education_requirements.lower():
                required_level = max(required_level, level)

        # Calculate score
        if candidate_level >= required_level:
            score = 0.8 + (candidate_level - required_level) * 0.1
        else:
            score = max(0.0, 0.8 - (required_level - candidate_level) * 0.2)

        score = min(1.0, score)

        breakdown = {
            "candidate_education": candidate_education,
            "required_education": education_requirements,
            "candidate_level": candidate_level,
            "required_level": required_level,
            "meets_requirement": candidate_level >= required_level,
            "score": score
        }

        return score, breakdown

    def calculate_role_relevance(self, previous_roles: List[str],
                                 job_title: str) -> Tuple[float, Dict]:
        """
        Calculate relevance score based on previous roles and job title.
        Returns a score between 0 and 1 and explanation.
        """
        job_keywords = job_title.lower().split()
        role_matches = 0

        for role in previous_roles:
            role_words = role.lower().split()
            if any(keyword in role_words for keyword in job_keywords):
                role_matches += 1

        # Calculate score based on role matches
        if role_matches > 0:
            score = min(1.0, 0.6 + (role_matches * 0.2))
        else:
            score = 0.3  # Base score for any professional experience

        breakdown = {
            "previous_roles": previous_roles,
            "job_title": job_title,
            "role_matches": role_matches,
            "score": score
        }

        return score, breakdown

    def rank_candidates(self, job_description: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Rank all candidates for a given job description.
        Returns a list of candidates with scores and explanations.
        """
        ranked_candidates = []

        for candidate in self.candidates:
            # Calculate individual scores
            skills_score, skills_breakdown = self.calculate_skills_match(
                candidate["skills"],
                job_description["required_skills"],
                job_description["preferred_skills"]
            )

            experience_score, experience_breakdown = self.calculate_experience_score(
                candidate["experience_years"],
                job_description["min_experience"]
            )

            education_score, education_breakdown = self.calculate_education_score(
                candidate["education"],
                job_description["education_requirements"]
            )

            role_relevance_score, role_breakdown = self.calculate_role_relevance(
                candidate["previous_roles"],
                job_description["title"]
            )

            # Calculate overall score with weights
            overall_score = (
                skills_score * 0.4 +           # 40% weight on skills
                experience_score * 0.25 +      # 25% weight on experience
                education_score * 0.20 +       # 20% weight on education
                role_relevance_score * 0.15    # 15% weight on role relevance
            )

            # Create candidate result
            candidate_result = {
                "candidate": candidate,
                "overall_score": overall_score,
                "scores": {
                    "skills": skills_score,
                    "experience": experience_score,
                    "education": education_score,
                    "role_relevance": role_relevance_score
                },
                "breakdowns": {
                    "skills": skills_breakdown,
                    "experience": experience_breakdown,
                    "education": education_breakdown,
                    "role_relevance": role_breakdown
                }
            }

            ranked_candidates.append(candidate_result)

        # Sort by overall score (highest first)
        ranked_candidates.sort(key=lambda x: x["overall_score"], reverse=True)

        return ranked_candidates

    def format_candidate_summary(self, candidate_result: Dict[str, Any], rank: int) -> str:
        """
        Format a candidate result into a human-readable summary.
        """
        candidate = candidate_result["candidate"]
        scores = candidate_result["scores"]
        breakdowns = candidate_result["breakdowns"]

        summary = f"""
Rank #{rank}: {candidate['name']}
Email: {candidate['email']}
Overall Score: {candidate_result['overall_score']:.2f}/1.00

Score Breakdown:
• Skills Match: {scores['skills']:.2f}/1.00 ({breakdowns['skills']['required_matches']}/{breakdowns['skills']['required_total']} required, {breakdowns['skills']['preferred_matches']}/{breakdowns['skills']['preferred_total']} preferred)
• Experience: {scores['experience']:.2f}/1.00 ({candidate['experience_years']} years vs {breakdowns['experience']['min_required']} required)
• Education: {scores['education']:.2f}/1.00 ({candidate['education']})
• Role Relevance: {scores['role_relevance']:.2f}/1.00 ({breakdowns['role_relevance']['role_matches']} matching roles)

Key Skills: {', '.join(candidate['skills'][:5])}{'...' if len(candidate['skills']) > 5 else ''}
Previous Roles: {', '.join(candidate['previous_roles'])}
Summary: {candidate['summary']}
"""
        return summary.strip()


# Create global ranker instance
ranker = CandidateRanker()


@tool
def rank_candidates_for_job(job_description: str, top_n: int = 3) -> str:
    """
    Ranks candidates for a specific job description and returns the top N candidates.

    Args:
        job_description: The job description text or job ID (1-5 for sample jobs)
        top_n: Number of top candidates to return (default: 3)
    """
    try:
        # Check if job_description is a number (sample job ID)
        if job_description.isdigit():
            job_id = int(job_description)
            if 1 <= job_id <= len(SAMPLE_JOB_DESCRIPTIONS):
                job_data = SAMPLE_JOB_DESCRIPTIONS[job_id - 1]
            else:
                return f"Invalid job ID. Please use 1-{len(SAMPLE_JOB_DESCRIPTIONS)} for sample jobs."
        else:
            # For now, we'll use the first sample job as default
            # In a real implementation, you would parse the job description
            job_data = SAMPLE_JOB_DESCRIPTIONS[0]

        # Rank candidates
        ranked_candidates = ranker.rank_candidates(job_data)

        # Format results
        result = f"Job: {job_data['title']} at {job_data['company']}\n"
        result += f"Required Skills: {', '.join(job_data['required_skills'])}\n"
        result += f"Minimum Experience: {job_data['min_experience']} years\n\n"
        result += f"Top {top_n} Candidates:\n"
        result += "=" * 50 + "\n"

        for i, candidate_result in enumerate(ranked_candidates[:top_n]):
            result += ranker.format_candidate_summary(candidate_result, i + 1)
            if i < top_n - 1:
                result += "\n" + "-" * 50 + "\n"

        return result

    except Exception as e:
        return f"Error ranking candidates: {str(e)}"


@tool
def list_available_jobs() -> str:
    """
    Lists all available sample job descriptions with their IDs.
    """
    result = "Available Sample Jobs:\n"
    result += "=" * 30 + "\n"

    for i, job in enumerate(SAMPLE_JOB_DESCRIPTIONS, 1):
        result += f"{i}. {job['title']} at {job['company']}\n"
        result += f"   Required Skills: {', '.join(job['required_skills'])}\n"
        result += f"   Min Experience: {job['min_experience']} years\n\n"

    return result


@tool
def get_job_details(job_id: str) -> str:
    """
    Gets detailed information about a specific job.

    Args:
        job_id: The job ID (1-5 for sample jobs)
    """
    try:
        if not job_id.isdigit():
            return "Please provide a valid job ID (1-5 for sample jobs)."

        job_id_int = int(job_id)
        if 1 <= job_id_int <= len(SAMPLE_JOB_DESCRIPTIONS):
            job = SAMPLE_JOB_DESCRIPTIONS[job_id_int - 1]

            result = f"Job Details:\n"
            result += f"Title: {job['title']}\n"
            result += f"Company: {job['company']}\n"
            result += f"Description: {job['description']}\n\n"
            result += f"Required Skills: {', '.join(job['required_skills'])}\n"
            result += f"Preferred Skills: {', '.join(job['preferred_skills'])}\n"
            result += f"Minimum Experience: {job['min_experience']} years\n"
            result += f"Education Requirements: {job['education_requirements']}\n\n"
            result += f"Responsibilities:\n"
            for resp in job['responsibilities']:
                result += f"• {resp}\n"

            return result
        else:
            return f"Invalid job ID. Please use 1-{len(SAMPLE_JOB_DESCRIPTIONS)} for sample jobs."

    except Exception as e:
        return f"Error getting job details: {str(e)}"


@tool
def search_candidates_by_skill(skill: str) -> str:
    """
    Searches for candidates who have a specific skill.

    Args:
        skill: The skill to search for
    """
    try:
        matching_candidates = []
        skill_lower = skill.lower()

        for candidate in CANDIDATES:
            if any(skill_lower in candidate_skill.lower() for candidate_skill in candidate["skills"]):
                matching_candidates.append(candidate)

        if not matching_candidates:
            return f"No candidates found with skill: {skill}"

        result = f"Candidates with skill '{skill}':\n"
        result += "=" * 40 + "\n"

        for candidate in matching_candidates:
            result += f"• {candidate['name']} ({candidate['experience_years']} years experience)\n"
            result += f"  Skills: {', '.join(candidate['skills'])}\n"
            result += f"  Previous Roles: {', '.join(candidate['previous_roles'])}\n\n"

        return result

    except Exception as e:
        return f"Error searching candidates: {str(e)}"
