#!/usr/bin/env python3
"""
Automated Zenodo uploader for research code and data.

This script handles the upload of GitHub releases to Zenodo, creating a new
deposition, uploading files, and publishing with DOI assignment.

Requirements:
    - ZENODO_TOKEN environment variable (from https://zenodo.org/account/settings/applications/)
    - requests library

Usage:
    export ZENODO_TOKEN="your_token_here"
    python scripts/upload_to_zenodo.py --repo-owner elkinnavarro-glitch --repo-name immune-state-geometry-scATAC --tag v1.0.0
"""

import os
import sys
import argparse
import json
import requests
from pathlib import Path
from datetime import datetime
import subprocess

# Zenodo API endpoints
ZENODO_SANDBOX = "https://sandbox.zenodo.org/api"
ZENODO_PROD = "https://zenodo.org/api"


class ZenodoUploader:
    """Handle uploads to Zenodo."""
    
    def __init__(self, token, use_sandbox=True):
        """Initialize Zenodo uploader.
        
        Args:
            token: Zenodo API token
            use_sandbox: Use sandbox (testing) or production
        """
        self.token = token
        self.base_url = ZENODO_SANDBOX if use_sandbox else ZENODO_PROD
        self.headers = {"Authorization": f"Bearer {token}"}
        print(f"\u2713 Zenodo uploader initialized ({'sandbox' if use_sandbox else 'production'})")
    
    def create_deposition(self, metadata):
        """Create a new deposition.
        
        Args:
            metadata: Dict with deposition metadata
            
        Returns:
            Dict with deposition info including id and bucket_url
        """
        url = f"{self.base_url}/deposit/depositions"
        response = requests.post(
            url,
            json={"metadata": metadata},
            headers=self.headers,
            timeout=30
        )
        response.raise_for_status()
        deposition = response.json()
        print(f"\u2713 Deposition created: {deposition['id']}")
        return deposition
    
    def upload_file(self, deposition_id, file_path):
        """Upload a file to deposition.
        
        Args:
            deposition_id: ID of target deposition
            file_path: Path to file to upload
            
        Returns:
            File metadata
        """
        bucket_url = f"{self.base_url}/deposit/depositions/{deposition_id}/files"
        file_path = Path(file_path)
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f)}
            response = requests.post(
                bucket_url,
                files=files,
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=60
            )
        
        response.raise_for_status()
        file_info = response.json()
        print(f"\u2713 Uploaded: {file_path.name}")
        return file_info
    
    def publish_deposition(self, deposition_id):
        """Publish a deposition (creates DOI and makes public).
        
        Args:
            deposition_id: ID of deposition to publish
            
        Returns:
            Published deposition info
        """
        url = f"{self.base_url}/deposit/depositions/{deposition_id}/actions/publish"
        response = requests.post(
            url,
            headers=self.headers,
            timeout=30
        )
        response.raise_for_status()
        deposition = response.json()
        doi = deposition['metadata'].get('doi', 'pending')
        print(f"\u2713 Published! DOI: {doi}")
        return deposition
    
    def download_release(self, repo_owner, repo_name, tag, download_dir="releases"):
        """Download GitHub release assets.
        
        Args:
            repo_owner: GitHub repo owner
            repo_name: GitHub repo name
            tag: Release tag
            download_dir: Where to download files
            
        Returns:
            List of downloaded file paths
        """
        download_path = Path(download_dir)
        download_path.mkdir(exist_ok=True)
        
        # Get release info from GitHub API
        gh_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/tags/{tag}"
        response = requests.get(gh_url, timeout=30)
        response.raise_for_status()
        release = response.json()
        
        files = []
        for asset in release.get('assets', []):
            download_url = asset['browser_download_url']
            file_path = download_path / asset['name']
            
            print(f"Downloading {asset['name']}...")
            response = requests.get(download_url, timeout=60)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            files.append(file_path)
            print(f"\u2713 Downloaded: {asset['name']}")
        
        return files


def load_zenodo_metadata(metadata_file=".zenodo.json"):
    """Load Zenodo metadata from JSON file.
    
    Args:
        metadata_file: Path to .zenodo.json
        
    Returns:
        Metadata dict
    """
    with open(metadata_file, 'r') as f:
        return json.load(f)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Upload GitHub release to Zenodo with automated DOI"
    )
    parser.add_argument(
        "--repo-owner",
        required=True,
        help="GitHub repository owner"
    )
    parser.add_argument(
        "--repo-name",
        required=True,
        help="GitHub repository name"
    )
    parser.add_argument(
        "--tag",
        default="main",
        help="Git tag/release to upload (default: main)"
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use Zenodo sandbox (testing) instead of production"
    )
    parser.add_argument(
        "--metadata",
        default=".zenodo.json",
        help="Path to metadata file"
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip GitHub download (files already present)"
    )
    
    args = parser.parse_args()
    
    # Get Zenodo token
    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        print("Error: ZENODO_TOKEN environment variable not set")
        print("Get token from: https://zenodo.org/account/settings/applications/")
        sys.exit(1)
    
    try:
        # Load metadata
        if not Path(args.metadata).exists():
            print(f"Error: {args.metadata} not found")
            sys.exit(1)
        
        metadata = load_zenodo_metadata(args.metadata)
        print(f"\u2713 Loaded metadata from {args.metadata}")
        
        # Initialize uploader
        uploader = ZenodoUploader(token, use_sandbox=args.sandbox)
        
        # Download files
        if not args.skip_download:
            print(f"\nDownloading release {args.tag}...")
            files = uploader.download_release(args.repo_owner, args.repo_name, args.tag)
        else:
            # Find existing files
            files = list(Path("releases").glob("*")) if Path("releases").exists() else []
        
        if not files:
            print("No files to upload")
            sys.exit(1)
        
        # Create deposition
        print("\nCreating Zenodo deposition...")
        deposition = uploader.create_deposition(metadata)
        deposition_id = deposition['id']
        
        # Upload files
        print("\nUploading files...")
        for file_path in files:
            uploader.upload_file(deposition_id, file_path)
        
        # Publish
        print("\nPublishing deposition...")
        published = uploader.publish_deposition(deposition_id)
        
        # Extract DOI
        doi = published['metadata'].get('doi')
        record_id = published['record_id']
        
        print(f"\n{'='*70}")
        print(f"SUCCESS! Zenodo record created and published")
        print(f"{'='*70}")
        print(f"Record ID: {record_id}")
        print(f"DOI: {doi}")
        print(f"URL: https://zenodo.org/record/{record_id}")
        print(f"{'='*70}\n")
        
        # Save info
        info = {
            "timestamp": datetime.now().isoformat(),
            "deposition_id": deposition_id,
            "record_id": record_id,
            "doi": doi,
            "url": f"https://zenodo.org/record/{record_id}",
            "tag": args.tag
        }
        
        with open("zenodo_release.json", "w") as f:
            json.dump(info, f, indent=2)
        
        print(f"\u2713 Release info saved to zenodo_release.json")
        
        return 0
    
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
