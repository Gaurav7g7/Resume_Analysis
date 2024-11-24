import numpy as np
from typing import List, Dict, Tuple
import os
import re
from student_resume_analysis import process_resume  # Import Gaurav's function


class JobPostingProcessor:
    """
    Temporary class to process job postings until Deepika's implementation is ready
    """

    def __init__(self):
        # Common keywords for each category
        self.keyword_categories = {
            "technical_skills": [
                "python",
                "data science",
                "machine learning",
                "ai",
                "programming",
                "software",
                "analysis",
                "research",
                "algorithm",
                "statistics",
                "computer",
                "nlp",
                "database",
                "sql",
                "data mining",
                "information retrieval",
                "natural language processing",
                "text mining",
            ],
            "education": [
                "phd",
                "master",
                "bachelor",
                "degree",
                "university",
                "graduate",
                "undergraduate",
                "computer science",
                "information science",
                "data science",
            ],
            "experience": [
                "research",
                "project",
                "development",
                "analysis",
                "design",
                "implementation",
                "team",
                "laboratory",
                "publication",
            ],
            "soft_skills": [
                "communication",
                "collaboration",
                "team",
                "problem solving",
                "leadership",
                "organization",
                "management",
                "independent",
            ],
        }

    def clean_text(self, text: str) -> str:
        """Clean the text for processing"""
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return text

    def extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """Extract keywords from text based on predefined categories"""
        cleaned_text = self.clean_text(text)
        found_keywords = {category: [] for category in self.keyword_categories}

        for category, keywords in self.keyword_categories.items():
            for keyword in keywords:
                if keyword in cleaned_text:
                    found_keywords[category].append(keyword)

        return found_keywords


class ATSScorer:
    def __init__(self):
        self.job_processor = JobPostingProcessor()
        self.weights = {
            "technical_skills": 0.4,
            "education": 0.3,
            "experience": 0.2,
            "soft_skills": 0.1,
        }

    def calculate_category_score(
        self, resume_keywords: List[str], posting_keywords: List[str]
    ) -> float:
        """Calculate matching score for a specific category"""
        if not resume_keywords or not posting_keywords:
            return 0.0

        resume_keywords = [k.lower() for k in resume_keywords]
        posting_keywords = [k.lower() for k in posting_keywords]

        matches = sum(
            1
            for k in posting_keywords
            if any(k in r or r in k for r in resume_keywords)
        )
        return (matches / len(posting_keywords)) * 100 if posting_keywords else 0

    def calculate_ats_score(
        self, resume_keywords: List[str], job_posting_text: str
    ) -> Tuple[float, Dict, List[str]]:
        """Calculate ATS score and provide recommendations"""
        posting_keywords = self.job_processor.extract_keywords(job_posting_text)

        scores = {}
        for category, weight in self.weights.items():
            category_score = self.calculate_category_score(
                resume_keywords, posting_keywords.get(category, [])
            )
            scores[category] = round(category_score, 2)

        final_score = sum(scores[cat] * weight for cat, weight in self.weights.items())

        recommendations = []
        for category, score in scores.items():
            if score < 70:
                missing = [
                    k
                    for k in posting_keywords.get(category, [])
                    if not any(
                        k.lower() in r.lower() or r.lower() in k.lower()
                        for r in resume_keywords
                    )
                ]
                if missing:
                    recommendations.append(
                        f"Consider adding these {category.replace('_', ' ')}: "
                        f"{', '.join(missing)}"
                    )

        return round(final_score, 2), scores, recommendations


def process_all_postings(resume_path: str, postings_dir: str) -> List[Dict]:
    """Process all job postings and return sorted results"""
    # Get keywords from resume using Gaurav's function
    resume_keywords = process_resume(resume_path)

    scorer = ATSScorer()
    results = []

    for filename in os.listdir(postings_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(postings_dir, filename), "r", encoding="utf-8") as f:
                posting_text = f.read()

            score, detailed_scores, recommendations = scorer.calculate_ats_score(
                resume_keywords, posting_text
            )

            results.append(
                {
                    "posting_name": filename,
                    "overall_score": score,
                    "detailed_scores": detailed_scores,
                    "recommendations": recommendations,
                }
            )

    # Sort by overall score
    results.sort(key=lambda x: x["overall_score"], reverse=True)
    return results


if __name__ == "__main__":
    # Use the actual resume from data directory
    resume_path = "data/resumes/Sarah_Johnson_Resume.pdf"

    print("Processing resume and job postings...")
    try:
        results = process_all_postings(resume_path, "data/job_postings")

        print("\nATS Analysis Results:")
        print("=" * 50)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Posting: {result['posting_name']}")
            print(f"Overall Score: {result['overall_score']}%")
            print("\nDetailed Scores:")
            for category, score in result["detailed_scores"].items():
                print(f"- {category.replace('_', ' ').title()}: {score}%")
            if result["recommendations"]:
                print("\nRecommendations:")
                for rec in result["recommendations"]:
                    print(f"- {rec}")
            print("-" * 50)

    except Exception as e:
        print(f"Error processing files: {str(e)}")
        print("Please ensure:")
        print("1. The resume file exists in data/resumes/")
        print("2. The job posting files exist in data/job_postings/")
        print("3. All required packages are installed")
