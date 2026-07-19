import os
from concurrent.futures import ThreadPoolExecutor
from git import Repo

class GitManager:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        
        self.whitelist_extensions = {'.py', '.js', '.ts', '.go', '.java', '.cpp', '.rb', '.rs'}
        self.blacklist_directories = {'node_modules', 'venv', '.git', 'dist', 'build', 'target'}
        self.max_char_limit = 12000 

    def _should_process_file(self, file_path: str) -> bool:
        parts = set(file_path.split(os.sep))
        if parts.intersection(self.blacklist_directories):
            return False
            
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in self.whitelist_extensions:
            return False
            
        return True

    def _process_single_diff(self, diff_item) -> dict:
        try:
            file_path = diff_item.b_path or diff_item.a_path
            
            if not self._should_process_file(file_path):
                return None

            diff_text = diff_item.diff.decode('utf-8', errors='ignore')
            
            is_truncated = False
            if len(diff_text) > self.max_char_limit:
                diff_text = diff_text[:self.max_char_limit] + "\n\n[TRUNCATED: DIFF EXCEEDS SYSTEM MAXIMUM CONFIGURATION]"
                is_truncated = True

            return {
                "file_path": file_path,
                "change_type": diff_item.change_type,
                "diff": diff_text,
                "truncated": is_truncated
            }
        except Exception as e:
            return {"file_path": getattr(diff_item, 'b_path', 'Unknown'), "error": str(e)}

    def get_repo_diffs(self, target_rev: str = "HEAD~1") -> list:
        diff_index = self.repo.index.diff(target_rev, create_patch=True)
        
        results = []
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_results = executor.map(self._process_single_diff, diff_index)
            
            for res in future_results:
                if res and "error" not in res:
                    results.append(res)
                elif res and "error" in res:
                    print(f"Failed to parse file {res['file_path']}: {res['error']}")
                    
        return results