"""Upload files to GitHub using the API without git credentials."""
import base64
import requests
from pathlib import Path
from typing import Optional


def push_to_github(
    file_path: str,
    repo_owner: str,
    repo_name: str,
    github_token: Optional[str] = None,
    commit_message: str = "Auto-update data"
) -> bool:
    """
    Push a file to GitHub using the GitHub API.
    
    Args:
        file_path: Local path to the file to upload
        repo_owner: GitHub username/org
        repo_name: Repository name
        github_token: GitHub Personal Access Token (optional, uses env/secrets if not provided)
        commit_message: Commit message
    
    Returns:
        True if successful, False otherwise
    """
    if not github_token:
        # Try to get from Streamlit secrets or environment
        try:
            import streamlit as st
            github_token = st.secrets.get("GITHUB_TOKEN")
        except:
            import os
            github_token = os.environ.get("GITHUB_TOKEN")
    
    if not github_token:
        print("⚠️ No GitHub token found - skipping push")
        return False
    
    try:
        # Read file content
        with open(file_path, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        
        # Get relative path for GitHub (e.g., "api_exports/all_goods.json")
        file_path_obj = Path(file_path)
        # Assuming we're in the repo root
        relative_path = str(file_path_obj.relative_to(Path.cwd()))
        
        # GitHub API URL
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{relative_path}"
        
        # Get current file SHA (needed for updates)
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(api_url, headers=headers)
        sha = response.json().get('sha') if response.status_code == 200 else None
        
        # Prepare the update
        data = {
            "message": commit_message,
            "content": content,
            "branch": "main"
        }
        
        if sha:
            data["sha"] = sha
        
        # Push to GitHub
        response = requests.put(api_url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            print(f"✅ Pushed {relative_path} to GitHub")
            return True
        else:
            print(f"❌ GitHub API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error pushing to GitHub: {e}")
        return False
