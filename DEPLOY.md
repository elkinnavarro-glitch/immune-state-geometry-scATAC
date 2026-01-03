# Zenodo Deployment Guide

Automated deployment of this repository to Zenodo with DOI assignment.

## Prerequisites

1. **Zenodo Account**: Create a free account at https://zenodo.org (or https://sandbox.zenodo.org for testing)
2. **API Token**: Generate a personal access token:
   - Go to https://zenodo.org/account/settings/applications/tokens/new
   - Create a new token with **deposit:write** and **deposit:read** scopes
   - Copy the token to a safe location

3. **Python Requirements**:
   ```bash
   pip install requests
   ```

## Quick Start (Manual Deployment)

### Step 1: Set Environment Variable

```bash
export ZENODO_TOKEN="your_token_here"
```

### Step 2: Create GitHub Release

```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

### Step 3: Test with Zenodo Sandbox (Recommended)

```bash
python scripts/upload_to_zenodo.py \
  --repo-owner elkinnavarro-glitch \
  --repo-name immune-state-geometry-scATAC \
  --tag v1.0.0 \
  --sandbox
```

This will:
- Download release assets from GitHub
- Create a deposition on Zenodo Sandbox
- Upload all files
- Publish and assign a test DOI
- Save record info to `zenodo_release.json`

### Step 4: Verify and Deploy to Production

Once satisfied with the sandbox result, deploy to production Zenodo:

```bash
python scripts/upload_to_zenodo.py \
  --repo-owner elkinnavarro-glitch \
  --repo-name immune-state-geometry-scATAC \
  --tag v1.0.0
```

## What Gets Uploaded

The script automatically downloads all assets from the GitHub release:
- Source code archive (.zip/.tar.gz)
- Supplementary files
- Documentation

Metadata comes from `.zenodo.json`:
- Title
- Description
- Authors
- Keywords
- License
- Related identifiers

## Output

After successful deployment, a `zenodo_release.json` file is created:

```json
{
  "timestamp": "2024-01-02T20:00:00",
  "deposition_id": 12345,
  "record_id": 12346,
  "doi": "10.5281/zenodo.12346",
  "url": "https://zenodo.org/record/12346",
  "tag": "v1.0.0"
}
```

## Updating the DOI in README

After successful deployment:

1. Copy the DOI from `zenodo_release.json`
2. Update README.md:
   - Replace `10.5281/zenodo.XXXXXX` with actual DOI
   - Update Zenodo link
3. Commit and push:
   ```bash
   git add README.md
   git commit -m "docs: Update Zenodo DOI"
   git push
   ```

## Automated Deployment (GitHub Actions)

For fully automated deployment on every release, create `.github/workflows/zenodo.yml`:

```yaml
name: Deploy to Zenodo

on:
  release:
    types: [published]

jobs:
  zenodo-upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install requests
      
      - name: Upload to Zenodo
        env:
          ZENODO_TOKEN: ${{ secrets.ZENODO_TOKEN }}
        run: |
          python scripts/upload_to_zenodo.py \
            --repo-owner ${{ github.repository_owner }} \
            --repo-name ${{ github.event.repository.name }} \
            --tag ${{ github.event.release.tag_name }}
      
      - name: Upload release info
        uses: actions/upload-artifact@v3
        with:
          name: zenodo-release-info
          path: zenodo_release.json
```

## Troubleshooting

### Token Issues
- Verify token is set: `echo $ZENODO_TOKEN`
- Check token scopes: **deposit:write** and **deposit:read** are required
- Generate new token if needed

### Network Errors
- Check internet connection
- Try sandbox first: `--sandbox`
- Verify Zenodo is accessible: https://zenodo.org/status

### File Upload Failures
- Check file sizes (Zenodo has limits)
- Verify files exist in release
- Try `--skip-download` if files already downloaded

## Support

For Zenodo API questions: https://developers.zenodo.org
For script issues: Open GitHub issue
