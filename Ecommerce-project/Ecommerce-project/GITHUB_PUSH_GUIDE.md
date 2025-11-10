# Step-by-Step Guide: Push to GitHub

Follow these steps to push your capstone project to GitHub.

---

## Step 1: Check Git Status

```bash
git status
```

Make sure you're in the project directory and Git is initialized.

---

## Step 2: Add All Files

```bash
git add .
```

This stages all files for commit.

---

## Step 3: Commit Your Changes

```bash
git commit -m "Initial commit: Django eCommerce Capstone Project with Docker"
```

---

## Step 4: Create GitHub Repository

1. Go to **https://github.com/new**
2. Fill in the details:
   - **Repository name**: `ecommerce-capstone-project`
   - **Description**: "Django eCommerce Multi-Vendor Platform - Capstone Project"
   - **Visibility**: **PUBLIC** (important for portfolio!)
   - **Do NOT** check "Initialize this repository with a README"
3. Click **"Create repository"**

---

## Step 5: Add Remote Origin

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-capstone-project.git
```

Example:
```bash
git remote add origin https://github.com/Elton2/ecommerce-capstone-project.git
```

---

## Step 6: Rename Branch to Main

```bash
git branch -M main
```

---

## Step 7: Push to GitHub

```bash
git push -u origin main
```

You may be prompted for your GitHub credentials.

---

## Step 8: Push All Branches

If you have docs and container branches:

```bash
git push --all origin
```

---

## Step 9: Verify on GitHub

1. Go to your repository URL
2. Check that all files are visible
3. Verify README.md displays correctly
4. Check that all branches are present

---

## Step 10: Update capstone.txt

Update the `capstone.txt` file with your actual repository URL:

```
https://github.com/YOUR_USERNAME/ecommerce-capstone-project
```

---

## Troubleshooting

### Authentication Error

If you get authentication errors, you may need to use a Personal Access Token:

1. Go to **GitHub Settings** → **Developer settings** → **Personal access tokens**
2. Generate a new token with `repo` permissions
3. Use the token as your password when pushing

### Remote Already Exists

If you get "remote origin already exists":

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-capstone-project.git
```

### Large Files

If you have large files causing issues:

1. Make sure `.gitignore` is properly configured
2. Remove large files from staging:
   ```bash
   git rm --cached path/to/large/file
   ```

---

## Final Checklist

- [ ] Repository is PUBLIC
- [ ] All files pushed successfully
- [ ] README.md displays correctly
- [ ] .gitignore is working (no venv, __pycache__, etc.)
- [ ] capstone.txt contains correct URL
- [ ] docker1.txt is included
- [ ] Documentation is included

---

**Your repository should be accessible at:**
```
https://github.com/YOUR_USERNAME/ecommerce-capstone-project
```

This URL goes in your `capstone.txt` file for submission!
