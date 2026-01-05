#!/usr/bin/env python3
"""
YMCA Matara Website Build Script
================================
This script automatically generates the news section of the YMCA Matara website.

Usage:
    python build_site.py

What it does:
1. Scans the 'news/' directory for programme folders
2. Generates 'news.html' with links to all programmes
3. Generates 'index.html' inside each programme folder with description and media gallery
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Configuration
SCRIPT_DIR = Path(__file__).parent
NEWS_DIR = SCRIPT_DIR / "news"
NEWS_HTML = SCRIPT_DIR / "news.html"

# Supported media extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov', '.avi', '.mkv'}

# YMCA Brand Colors
YMCA_BLUE = "#004a99"
YMCA_BLUE_DARK = "#003570"
YMCA_RED = "#cc0000"


def folder_to_title(folder_name: str) -> str:
    """Convert folder name to title case (e.g., 'youth-camp' -> 'Youth Camp')"""
    # Replace hyphens and underscores with spaces
    title = re.sub(r'[-_]', ' ', folder_name)
    # Title case
    return title.title()


def get_common_styles() -> str:
    """Return the common CSS styles used across all pages"""
    return '''
        :root {
            --ymca-blue: #004a99;
            --ymca-blue-dark: #003570;
            --ymca-red: #cc0000;
            --ymca-red-dark: #a30000;
            --white: #ffffff;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-600: #4b5563;
            --gray-700: #374151;
            --gray-800: #1f2937;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--gray-700);
            background: var(--gray-50);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Navigation */
        .navbar {
            background: linear-gradient(135deg, var(--ymca-blue) 0%, var(--ymca-blue-dark) 100%);
            padding: 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: var(--shadow-lg);
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 1.5rem;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 1rem 0;
            text-decoration: none;
            color: var(--white);
        }

        .logo-icon {
            width: 45px;
            height: 45px;
            background: var(--white);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.9rem;
            color: var(--ymca-blue);
            box-shadow: var(--shadow-md);
        }

        .logo-text {
            font-weight: 700;
            font-size: 1.25rem;
            letter-spacing: -0.025em;
        }

        .logo-text span {
            display: block;
            font-size: 0.75rem;
            font-weight: 500;
            opacity: 0.9;
            letter-spacing: 0.05em;
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 0.25rem;
        }

        .nav-links a {
            display: block;
            padding: 0.75rem 1.5rem;
            color: var(--white);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            border-radius: 8px;
            transition: all 0.2s ease;
            position: relative;
        }

        .nav-links a:hover {
            background: rgba(255,255,255,0.15);
        }

        .nav-links a.active {
            background: rgba(255,255,255,0.2);
        }

        .nav-links a.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 30px;
            height: 3px;
            background: var(--ymca-red);
            border-radius: 3px 3px 0 0;
        }

        /* Page Header */
        .page-header {
            background: linear-gradient(135deg, var(--ymca-blue) 0%, var(--ymca-blue-dark) 50%, #002244 100%);
            color: var(--white);
            padding: 3rem 1.5rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .page-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 1;
        }

        .page-header-content {
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        .page-header h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 800;
            margin-bottom: 0.75rem;
            letter-spacing: -0.025em;
        }

        .page-header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* Main Content */
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 1.5rem;
            flex: 1;
        }

        /* News List Styles */
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        .news-card {
            background: var(--white);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: all 0.3s ease;
            border: 1px solid var(--gray-100);
            text-decoration: none;
            color: inherit;
            display: block;
        }

        .news-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-xl);
        }

        .news-card-header {
            background: linear-gradient(135deg, var(--ymca-blue), var(--ymca-blue-dark));
            padding: 2rem;
            color: var(--white);
        }

        .news-card-header h3 {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .news-card-body {
            padding: 1.5rem 2rem;
        }

        .news-card-body p {
            color: var(--gray-600);
            font-size: 0.95rem;
        }

        .news-card-footer {
            padding: 0 2rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--ymca-blue);
            font-weight: 500;
            font-size: 0.9rem;
        }

        /* Programme Page Styles */
        .programme-content {
            background: var(--white);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--gray-100);
            margin-bottom: 2rem;
        }

        .programme-description {
            white-space: pre-wrap;
            line-height: 1.8;
            color: var(--gray-700);
            font-size: 1.05rem;
        }

        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--ymca-blue);
            text-decoration: none;
            font-weight: 500;
            margin-bottom: 1.5rem;
            transition: color 0.2s;
        }

        .back-link:hover {
            color: var(--ymca-blue-dark);
        }

        /* Media Gallery */
        .gallery-section {
            margin-top: 2rem;
        }

        .gallery-section h2 {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--gray-800);
            margin-bottom: 1.5rem;
        }

        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }

        .gallery-item {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: transform 0.3s ease;
        }

        .gallery-item:hover {
            transform: scale(1.02);
        }

        .gallery-item img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            display: block;
        }

        .gallery-item video {
            width: 100%;
            display: block;
            background: #000;
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            background: var(--white);
            border-radius: 20px;
            box-shadow: var(--shadow-md);
        }

        .empty-state-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }

        .empty-state h3 {
            font-size: 1.5rem;
            color: var(--gray-800);
            margin-bottom: 0.5rem;
        }

        .empty-state p {
            color: var(--gray-600);
        }

        /* Footer */
        .footer {
            background: var(--gray-800);
            color: var(--white);
            padding: 2rem 1.5rem;
            text-align: center;
            margin-top: auto;
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
        }

        .footer-text {
            opacity: 0.7;
            font-size: 0.85rem;
        }

        /* Mobile Menu Toggle */
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--white);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
        }

        @media (max-width: 768px) {
            .mobile-menu-btn {
                display: block;
            }

            .nav-links {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: var(--ymca-blue-dark);
                flex-direction: column;
                padding: 1rem;
                gap: 0.5rem;
            }

            .nav-links.active {
                display: flex;
            }

            .nav-links a {
                padding: 1rem;
                text-align: center;
            }

            .main-content {
                padding: 2rem 1rem;
            }

            .programme-content {
                padding: 1.5rem;
            }

            .gallery-grid {
                grid-template-columns: 1fr;
            }
        }
    '''


def generate_news_html(programmes: list) -> str:
    """Generate the main news.html page listing all programmes"""
    
    # Generate programme cards
    if programmes:
        cards_html = ""
        for prog in programmes:
            cards_html += f'''
            <a href="news/{prog['folder']}/index.html" class="news-card">
                <div class="news-card-header">
                    <h3>{prog['title']}</h3>
                </div>
                <div class="news-card-body">
                    <p>Click to view details, photos, and videos from this programme.</p>
                </div>
                <div class="news-card-footer">
                    View Programme →
                </div>
            </a>
            '''
        content_html = f'<div class="news-grid">{cards_html}</div>'
    else:
        content_html = '''
        <div class="empty-state">
            <div class="empty-state-icon">📰</div>
            <h3>No Programmes Yet</h3>
            <p>Check back soon for updates on our latest programmes and activities!</p>
        </div>
        '''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Latest news and programmes from YMCA Matara, Sri Lanka.">
    <title>News & Programmes | YMCA Matara</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>{get_common_styles()}</style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="index.html" class="logo">
                <div class="logo-icon">YMCA</div>
                <div class="logo-text">
                    YMCA Matara
                    <span>Sri Lanka</span>
                </div>
            </a>
            <button class="mobile-menu-btn" onclick="toggleMenu()" aria-label="Toggle menu">☰</button>
            <ul class="nav-links" id="navLinks">
                <li><a href="index.html">About</a></li>
                <li><a href="news.html" class="active">News</a></li>
            </ul>
        </div>
    </nav>

    <!-- Page Header -->
    <header class="page-header">
        <div class="page-header-content">
            <h1>News & Programmes</h1>
            <p>Stay updated with our latest activities and completed programmes</p>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        {content_html}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <p class="footer-text">© 2024 YMCA Matara, Sri Lanka. Part of the World YMCA Movement.</p>
        </div>
    </footer>

    <script>
        function toggleMenu() {{
            document.getElementById('navLinks').classList.toggle('active');
        }}
    </script>
</body>
</html>'''


def generate_programme_html(title: str, description: str, media_files: list) -> str:
    """Generate the programme detail page"""
    
    # Generate gallery items
    gallery_html = ""
    for media in media_files:
        ext = Path(media).suffix.lower()
        if ext in IMAGE_EXTENSIONS:
            alt_text = Path(media).stem.replace('-', ' ').replace('_', ' ').title()
            gallery_html += f'''
            <div class="gallery-item">
                <img src="{media}" alt="{alt_text}" loading="lazy">
            </div>
            '''
        elif ext in VIDEO_EXTENSIONS:
            gallery_html += f'''
            <div class="gallery-item">
                <video src="{media}" controls preload="metadata"></video>
            </div>
            '''
    
    # Gallery section (only if there are media files)
    gallery_section = ""
    if gallery_html:
        gallery_section = f'''
        <section class="gallery-section">
            <h2>📸 Photos & Videos</h2>
            <div class="gallery-grid">
                {gallery_html}
            </div>
        </section>
        '''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} - YMCA Matara Programme">
    <title>{title} | YMCA Matara</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>{get_common_styles()}</style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="../../index.html" class="logo">
                <div class="logo-icon">YMCA</div>
                <div class="logo-text">
                    YMCA Matara
                    <span>Sri Lanka</span>
                </div>
            </a>
            <button class="mobile-menu-btn" onclick="toggleMenu()" aria-label="Toggle menu">☰</button>
            <ul class="nav-links" id="navLinks">
                <li><a href="../../index.html">About</a></li>
                <li><a href="../../news.html" class="active">News</a></li>
            </ul>
        </div>
    </nav>

    <!-- Page Header -->
    <header class="page-header">
        <div class="page-header-content">
            <h1>{title}</h1>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        <a href="../../news.html" class="back-link">← Back to News</a>
        
        <article class="programme-content">
            <div class="programme-description">{description}</div>
            {gallery_section}
        </article>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <p class="footer-text">© 2024 YMCA Matara, Sri Lanka. Part of the World YMCA Movement.</p>
        </div>
    </footer>

    <script>
        function toggleMenu() {{
            document.getElementById('navLinks').classList.toggle('active');
        }}
    </script>
</body>
</html>'''


def scan_programmes() -> list:
    """Scan the news directory for programme folders"""
    programmes = []
    
    if not NEWS_DIR.exists():
        print(f"[*] Creating news directory: {NEWS_DIR}")
        NEWS_DIR.mkdir(parents=True, exist_ok=True)
        return programmes
    
    for item in NEWS_DIR.iterdir():
        # Skip hidden files/folders and non-directories
        if item.name.startswith('.') or not item.is_dir():
            continue
        
        programmes.append({
            'folder': item.name,
            'title': folder_to_title(item.name),
            'path': item
        })
    
    # Sort alphabetically by title
    programmes.sort(key=lambda x: x['title'])
    
    return programmes


def get_media_files(folder_path: Path) -> list:
    """Get all media files in a programme folder"""
    media_files = []
    
    for item in folder_path.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            # Skip description.txt and index.html
            if item.name.lower() in ('description.txt', 'index.html'):
                continue
            # Check if it's a media file
            if ext in IMAGE_EXTENSIONS or ext in VIDEO_EXTENSIONS:
                media_files.append(item.name)
    
    # Sort alphabetically
    media_files.sort()
    
    return media_files


def build_site():
    """Main function to build the site"""
    print("=" * 50)
    print("  YMCA Matara Website Builder")
    print("=" * 50)
    print()
    
    # Scan for programmes
    print("[*] Scanning for programmes...")
    programmes = scan_programmes()
    print(f"    Found {len(programmes)} programme(s)")
    print()
    
    # Generate news.html
    print("[*] Generating news.html...")
    news_html = generate_news_html(programmes)
    with open(NEWS_HTML, 'w', encoding='utf-8') as f:
        f.write(news_html)
    print(f"    [OK] Created: {NEWS_HTML}")
    print()
    
    # Generate programme pages
    if programmes:
        print("[*] Generating programme pages...")
        for prog in programmes:
            folder_path = prog['path']
            description_file = folder_path / "description.txt"
            
            # Read description
            description = ""
            if description_file.exists():
                with open(description_file, 'r', encoding='utf-8') as f:
                    description = f.read()
            else:
                description = "No description available."
                print(f"    [!] No description.txt found in {prog['folder']}")
            
            # Get media files
            media_files = get_media_files(folder_path)
            
            # Generate HTML
            programme_html = generate_programme_html(
                prog['title'],
                description,
                media_files
            )
            
            # Write to file
            output_file = folder_path / "index.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(programme_html)
            
            print(f"    [OK] Created: news/{prog['folder']}/index.html")
            if media_files:
                print(f"         {len(media_files)} media file(s) included")
        print()
    
    print("=" * 50)
    print("[+] Build complete!")
    print()
    print("Summary:")
    print(f"    - news.html updated with {len(programmes)} programme(s)")
    print(f"    - {len(programmes)} programme page(s) generated")
    print()
    print("Next steps:")
    print("    1. Run: python -m http.server 8000")
    print("    2. Open: http://localhost:8000")
    print("    3. Commit and push to GitHub")
    print("=" * 50)


if __name__ == "__main__":
    build_site()
