import sys
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

class GitAnalyzer:
    def __init__(self, model_name: str = "llama3"):
        self.llm = OllamaLLM(
            model=model_name, 
            temperature=0.2,
            base_url="http://127.0.0.1:11434" 
        )
        self.prompt_template = PromptTemplate.from_template(
            """You are an expert Principal Software Engineer and System Architect. 
Your task is to analyze a single code file diff from a local Git repository and provide an actionable, deep technical architectural review.

FILE BEING REVIEWED: {file_path}

CODE DIFF (CHANGES):
{diff_text}

CRITICAL INSTRUCTIONS:
1. Focus ONLY on major architectural flaws, performance bottlenecks, missing edge cases, or resource leaks.
2. If the code is well-written, do not invent issues; acknowledge the solid design.
3. Keep your advice concise, direct, and completely free of conversational filler.

Please structure your review using these exact markdown headings:
### Key Architectural Impact
(Assess how these changes alter or affect the codebase structure)

### Critical Vulnerabilities / Optimization Risks
(Detail any memory leaks, concurrency risks, or O-notation complexity scaling issues)

### Refactoring Recommendations
(Provide brief, clear structural suggestions for improvement)
---
"""
        )

    def analyze_diff_stream(self, file_path: str, diff_text: str, governor) -> None:
        formatted_prompt = self.prompt_template.format(
            file_path=file_path,
            diff_text=diff_text
        )

        try:
            for chunk in self.llm.stream(formatted_prompt):
                sys.stdout.write(chunk)
                sys.stdout.flush()
        except Exception as e:
            print(f"\nError during analysis: {e}")
                

