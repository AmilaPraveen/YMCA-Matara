# YMCA Matara Website - User Guide

A complete guide for managing the YMCA Matara website with the automated news system.

---

## 📁 Project Structure

```
ymca-matara/
├── index.html          ← Landing page (About YMCA Matara)
├── news.html           ← News list (auto-generated)
├── build_site.py       ← Python automation script
└── news/               ← Your programme folders go here
    └── [programme-name]/
        ├── description.txt
        ├── photo1.jpg
        ├── video.mp4
        └── index.html  ← Auto-generated
```

---

## 🚀 Quick Start: Adding a New Programme

### Step 1: Create a Folder

Create a new folder inside `news/` with a descriptive name using hyphens:

```
news/youth-leadership-camp-2024/
news/football-tournament/
news/community-cleanup-drive/
```

> **Tip:** The folder name becomes the page title. `youth-leadership-camp` → **Youth Leadership Camp**

### Step 2: Add Description

Create `description.txt` inside your folder and write your programme details:

```
news/football-tournament/description.txt
```

Example content:
```
YMCA Matara Football Tournament 2024

We successfully hosted our annual football tournament with 
12 teams participating from across the Southern Province.

Event Highlights:
• Opening ceremony with chief guest Mr. John Silva
• Round-robin matches over 3 days
• Finals watched by 500+ spectators

Winners: Team Phoenix
Runner-up: Team Warriors

Thank you to all participants, sponsors, and volunteers!
```

### Step 3: Add Photos & Videos (Optional)

Drop your media files directly into the folder:

```
news/football-tournament/
├── description.txt
├── opening-ceremony.jpg
├── trophy-presentation.jpg
├── match-highlights.mp4
└── team-photo.png
```

**Supported formats:**
- **Images:** .jpg, .jpeg, .png, .gif, .webp, .svg
- **Videos:** .mp4, .webm, .mov

### Step 4: Run the Build Script

Open terminal/command prompt in the project folder and run:

```bash
python build_site.py
```

You should see:
```
==================================================
  YMCA Matara Website Builder
==================================================

[*] Scanning for programmes...
    Found 2 programme(s)

[*] Generating news.html...
    [OK] Created: news.html

[*] Generating programme pages...
    [OK] Created: news/football-tournament/index.html
         3 media file(s) included
    [OK] Created: news/sample-programme/index.html

==================================================
[+] Build complete!
```

### Step 5: Preview Locally

Start a local server to preview:

```bash
python -m http.server 8000
```

Open your browser and go to: **http://localhost:8000**

### Step 6: Deploy to GitHub

Commit and push your changes:

```bash
git add .
git commit -m "Added football tournament programme"
git push
```

Your website will automatically update on GitHub Pages! ✨

---

## 🔧 GitHub Pages Setup (First Time Only)

### 1. Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Name it: `ymca-matara` (or your preferred name)
3. Set to **Public**
4. Create repository

### 2. Push Your Code

```bash
cd ymca-matara
git init
git add .
git commit -m "Initial commit: YMCA Matara website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ymca-matara.git
git push -u origin main
```

### 3. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select **main** branch
4. Click **Save**
5. Wait 1-2 minutes for deployment

Your site will be live at: `https://YOUR-USERNAME.github.io/ymca-matara/`

---

## 📋 Common Tasks

### Editing the Landing Page

Edit `index.html` directly to update:
- Organization description
- Contact information
- Statistics
- Services offered

### Updating a Programme

1. Navigate to the programme folder: `news/programme-name/`
2. Edit `description.txt`
3. Add/remove media files
4. Run `python build_site.py`
5. Commit and push

### Deleting a Programme

1. Delete the entire folder: `news/programme-name/`
2. Run `python build_site.py`
3. Commit and push

---

## 🎨 Customization

### Changing Colors

Edit the CSS variables in both `index.html` and `build_site.py`:

```css
:root {
    --ymca-blue: #004a99;      /* Main brand color */
    --ymca-blue-dark: #003570; /* Darker shade */
    --ymca-red: #cc0000;       /* Accent color */
}
```

### Updating Contact Information

In `index.html`, find the contact section and update:
- Address
- Phone number
- Email
- Office hours

---

## ❓ Troubleshooting

### "Python not found" Error

Make sure Python is installed:
```bash
python --version
```

On Windows, you might need to use:
```bash
py build_site.py
```

### Images Not Showing

- Check file extensions are lowercase (`.jpg` not `.JPG`)
- Ensure files are in the correct programme folder
- Verify filenames don't have special characters

### Changes Not Appearing on GitHub Pages

- Wait 2-3 minutes after pushing
- Clear browser cache (Ctrl+Shift+R)
- Check GitHub Actions for deployment status

---

## 📞 Support

For technical issues, please contact the website administrator.

---

*Last updated: January 2026*
