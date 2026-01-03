# Zenodo Quick Start - Automated Deployment Guide

## Overview

This guide provides **3 easy steps** to deploy your repository to Zenodo with a DOI using ORCID authentication.

## ⚙️ Prerequisites Check

```bash
# Verify Python and git are installed
python --version  # Need 3.7+
git --version

# Install requests library
pip install requests
```

## 🚀 Step 1: Create Zenodo Token via ORCID (5 minutes)

### 1.1 Go to Token Creation Page

**URL**: https://zenodo.org/account/settings/applications/tokens/new

### 1.2 Sign in with ORCID

1. Click "Sign in with ORCID"
2. Enter your ORCID credentials:
   - ORCID ID: `0000-XXXX-XXXX-XXXX` (your ORCID iD)
   - Password: (your ORCID password)
3. Click "Sign in"
4. Authorize Zenodo access when prompted

### 1.3 Create Personal Access Token

1. After login, you'll be at: https://zenodo.org/account/settings/applications/tokens/new
2. Click "Create new token"
3. Enter token name: `immune-state-geometry-deployment`
4. Select required scopes:
   - ✅ `deposit:write` (create and upload)
   - ✅ `deposit:read` (verify uploads)
5. Click "Create"
6. **COPY THE TOKEN** - You won't see it again!

### Example Token
```
Abc1234defGHI567JKL890mnoPQRSTuvwxyz01234567890123456789
```

## 🎯 Step 2: Create GitHub Release

```bash
# Clone repo locally
git clone https://github.com/elkinnavarro-glitch/immune-state-geometry-scATAC.git
cd immune-state-geometry-scATAC

# Create and push a release tag
git tag -a v1.0.0 -m "Initial release: Geometric constraints in immune states"
git push origin v1.0.0
```

GitHub automatically creates a release with source archives.

## 📤 Step 3: Deploy to Zenodo (Automated)

### 3.1 Set Environment Variable

```bash
# macOS/Linux
export ZENODO_TOKEN="paste-your-token-here"

# Windows (PowerShell)
$env:ZENODO_TOKEN="paste-your-token-here"
```

### 3.2 Test with Zenodo Sandbox (Recommended)

```bash
python scripts/upload_to_zenodo.py \
  --repo-owner elkinnavarro-glitch \
  --repo-name immune-state-geometry-scATAC \
  --tag v1.0.0 \
  --sandbox
```

**Expected output**:
```
✓ Zenodo uploader initialized (sandbox)
✓ Loaded metadata from .zenodo.json
✓ Deposition created: 12345
✓ Uploaded: immune-state-geometry-scATAC-v1.0.0.tar.gz
✓ Published! DOI: 10.5281/zenodo.12346

======================================================================
SUCCESS! Zenodo record created and published
======================================================================
Record ID: 12346
DOI: 10.5281/zenodo.12346
URL: https://zenodo.org/record/12346
======================================================================
```

### 3.3 Deploy to Production Zenodo

```bash
python scripts/upload_to_zenodo.py \
  --repo-owner elkinnavarro-glitch \
  --repo-name immune-state-geometry-scATAC \
  --tag v1.0.0
```

## 📝 Step 4: Update README with DOI

### 4.1 Find Your DOI

From the `zenodo_release.json` file created by the script:

```bash
cat zenodo_release.json
```

Look for the `doi` field: `10.5281/zenodo.XXXXXX`

### 4.2 Update README.md

1. Open `README.md`
2. Find this section:
   ```markdown
   - **Zenodo**: [10.5281/zenodo.XXXXXX](https://zenodo.org/record/XXXXXX) *(pending)*
   ```
3. Replace `XXXXXX` with your actual record ID
4. Remove `*(pending)*`
5. Save and commit:
   ```bash
   git add README.md
   git commit -m "docs: Update Zenodo DOI after deployment"
   git push
   ```

## 🔍 Verify Deployment

1. Visit: `https://zenodo.org/record/YOUR-RECORD-ID`
2. Verify all files are uploaded
3. Check metadata is correct
4. Share the DOI in your publications!

## ⚡ Troubleshooting

### Token Issues
- ❌ "Token not found": Check environment variable is set
  ```bash
  echo $ZENODO_TOKEN  # Should print your token
  ```
- ❌ "Invalid token": Regenerate at Zenodo settings

### Upload Failures
- ❌ "Network error": Check internet, try sandbox mode first
- ❌ "File not found": Ensure GitHub release exists with assets

### Help
- Zenodo API Docs: https://developers.zenodo.org/
- ORCID Support: https://support.orcid.org/
- Script Issues: Open GitHub issue in this repo

## ✅ Success!

Once complete, your repository has:
- ✓ Public Zenodo record
- ✓ Permanent DOI
- ✓ Citation metadata
- ✓ Searchable on Zenodo
- ✓ README documentation updated

**Estimated time**: ~15 minutes total

---

**Next**: Use your DOI in journal submissions, grants, and citations!
