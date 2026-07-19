import os
import click
from concurrent.futures import ThreadPoolExecutor

import concurrent

from src.git_manager import GitManager
from src.governor import LLMGovernor
from src.analyzer import GitAnalyzer

@click.command()
@click.option('--repo-path', default=".", help='Path to the local Git repository.')
@click.option('--target-rev', default="HEAD~1", help='The target commit or branch to compare against (e.g., HEAD~1, main, origin/develop).')
@click.option('--model', default="llama3", help='The local Ollama model to use for analysis.')
@click.option('--max-llm-concurrent', default=1, help='How many LLM reviews to run simultaneously. Do not exceed 1-2 for local setups.')
def analyze(repo_path, target_rev, model, max_llm_concurrent):
    if not os.path.exists(repo_path):
        click.echo(f"Error: The path '{repo_path}' does not exist.", err=True)
        return

    click.echo(f"Initializing GitArchitect on repo: {os.path.abspath(repo_path)}")
    click.echo(f"Extracting diffs against: {target_rev}...")

    # 1. Initialize the system components
    try:
        git_manager = GitManager(repo_path=repo_path)
    except Exception as e:
        click.echo(f"Error connecting to Git repository: {e}", err=True)
        return
        
    analyzer = GitAnalyzer(model_name=model)
    governor = LLMGovernor(max_concurrent=max_llm_concurrent, delay_seconds=1.5)

    # 2. Extract and filter the file diffs
    diffs = git_manager.get_repo_diffs(target_rev=target_rev)
    
    if not diffs:
        click.echo("No valid code diffs found. (Check if your branch is up to date or if only non-whitelisted files were changed.)")
        return

    click.echo(f"Found {len(diffs)} file(s) for architectural review. Spooling local LLM...\n")

    with ThreadPoolExecutor(max_workers=max_llm_concurrent + 1) as executor:
        for item in diffs:
            # We don't want to analyze deleted files (nothing to review)
            if item.get("change_type") != 'D':
                executor.submit(
                    analyzer.analyze_diff_stream,
                    item["file_path"],
                    item["diff"],
                    governor
                )

if __name__ == '__main__':
    analyze()