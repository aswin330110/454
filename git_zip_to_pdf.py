#!/usr/bin/env python3
"""
Advanced Git Zip Extractor Tool
Extracts a git repository from a zip file and converts it to multiple formats with advanced features.
"""

import os
import sys
import zipfile
import argparse
import json
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Dict, Optional, Tuple
import chardet
import re

# PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Preformatted, Table, TableStyle, KeepTogether, PageTemplate,
    Frame, NextPageTemplate, Flowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.platypus.tableofcontents import TableOfContents

# Syntax highlighting
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_for_filename, get_lexer_by_name, guess_lexer
    from pygments.formatters import HtmlFormatter, TerminalFormatter
    from pygments.util import ClassNotFound
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

# Progress bar
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class FileStats:
    """Statistics for a file."""
    def __init__(self, path: Path, content: str):
        self.path = path
        self.size = len(content.encode('utf-8'))
        self.lines = len(content.splitlines())
        self.extension = path.suffix.lower()
        self.language = self.detect_language()

        # Code metrics
        non_empty_lines = [l for l in content.splitlines() if l.strip()]
        self.non_empty_lines = len(non_empty_lines)

        comment_patterns = {
            'python': r'^\s*#',
            'javascript': r'^\s*//',
            'java': r'^\s*//',
            'c': r'^\s*//',
            'ruby': r'^\s*#',
            'shell': r'^\s*#',
        }

        pattern = comment_patterns.get(self.language, r'^\s*[#/]')
        self.comment_lines = len([l for l in content.splitlines() if re.match(pattern, l)])

    def detect_language(self) -> str:
        """Detect programming language from extension."""
        ext_map = {
            '.py': 'python', '.js': 'javascript', '.jsx': 'javascript',
            '.ts': 'typescript', '.tsx': 'typescript',
            '.java': 'java', '.c': 'c', '.cpp': 'c++', '.h': 'c',
            '.cs': 'c#', '.go': 'go', '.rs': 'rust', '.rb': 'ruby',
            '.php': 'php', '.swift': 'swift', '.kt': 'kotlin',
            '.html': 'html', '.css': 'css', '.scss': 'scss',
            '.json': 'json', '.xml': 'xml', '.yaml': 'yaml', '.yml': 'yaml',
            '.md': 'markdown', '.txt': 'text', '.sh': 'shell',
            '.sql': 'sql', '.graphql': 'graphql',
        }
        return ext_map.get(self.extension, 'text')


class RepositoryStats:
    """Aggregate statistics for the repository."""
    def __init__(self):
        self.total_files = 0
        self.total_lines = 0
        self.total_size = 0
        self.language_stats = defaultdict(lambda: {'files': 0, 'lines': 0, 'size': 0})
        self.file_types = Counter()

    def add_file(self, stats: FileStats):
        """Add file statistics."""
        self.total_files += 1
        self.total_lines += stats.lines
        self.total_size += stats.size

        lang = stats.language
        self.language_stats[lang]['files'] += 1
        self.language_stats[lang]['lines'] += stats.lines
        self.language_stats[lang]['size'] += stats.size

        self.file_types[stats.extension] += 1

    def get_summary(self) -> Dict:
        """Get summary statistics."""
        return {
            'total_files': self.total_files,
            'total_lines': self.total_lines,
            'total_size': self.total_size,
            'languages': dict(self.language_stats),
            'file_types': dict(self.file_types),
        }


class DirectoryTree:
    """Build and display directory tree."""
    def __init__(self):
        self.tree = {}

    def add_path(self, path: str):
        """Add a path to the tree."""
        parts = Path(path).parts
        current = self.tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    def build_tree_string(self, tree: Dict = None, prefix: str = "", is_last: bool = True) -> str:
        """Build a string representation of the tree."""
        if tree is None:
            tree = self.tree

        lines = []
        items = sorted(tree.items())

        for i, (name, subtree) in enumerate(items):
            is_last_item = (i == len(items) - 1)

            if prefix == "":
                connector = ""
                new_prefix = ""
            else:
                connector = "└── " if is_last_item else "├── "
                new_prefix = prefix + ("    " if is_last_item else "│   ")

            lines.append(prefix + connector + name)

            if subtree:
                lines.extend(self.build_tree_string(subtree, new_prefix, is_last_item).splitlines())

        return '\n'.join(lines)


class AdvancedGitZipExtractor:
    """Advanced extractor with enhanced features."""

    # Extended ignore patterns
    IGNORE_PATTERNS = {
        '.git', '.gitignore', '.gitattributes', '.gitmodules',
        '.DS_Store', 'Thumbs.db', 'desktop.ini',
        '__pycache__', '*.pyc', '*.pyo', '*.pyd',
        'node_modules', 'bower_components',
        '.venv', 'venv', 'env', 'ENV',
        '.idea', '.vscode', '.vs', '*.swp', '*.swo',
        '.pytest_cache', '.coverage', '.nyc_output',
        '*.egg-info', 'dist', 'build', '.tox',
        'target', 'bin', 'obj',
        '.next', '.nuxt', '.cache',
        'coverage', 'htmlcov',
        '.gradle', '.maven',
        'vendor', 'Pods',
    }

    # Binary extensions (expanded)
    BINARY_EXTENSIONS = {
        # Images
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp', '.tiff',
        # Documents
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        # Archives
        '.zip', '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z', '.jar', '.war', '.ear',
        # Executables
        '.exe', '.dll', '.so', '.dylib', '.a', '.lib', '.o', '.obj',
        # Media
        '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.wav', '.flac', '.ogg',
        # Databases
        '.bin', '.dat', '.db', '.sqlite', '.sqlite3',
        # Fonts
        '.ttf', '.otf', '.woff', '.woff2', '.eot',
        # Other
        '.class', '.pyc', '.pyo', '.wasm',
    }

    # Comprehensive text extensions
    TEXT_EXTENSIONS = {
        # Programming languages
        '.py', '.pyw', '.pyx', '.pxd',
        '.js', '.jsx', '.mjs', '.cjs',
        '.ts', '.tsx', '.d.ts',
        '.java', '.scala', '.kt', '.kts', '.groovy',
        '.c', '.h', '.cpp', '.hpp', '.cc', '.cxx', '.c++',
        '.cs', '.vb', '.fs', '.fsx',
        '.go', '.rs', '.rb', '.php', '.swift', '.m', '.mm',
        '.r', '.R', '.jl', '.lua', '.perl', '.pl',
        '.dart', '.ex', '.exs', '.clj', '.cljs',
        '.hs', '.elm', '.ml', '.erl',
        # Web
        '.html', '.htm', '.xhtml', '.xml', '.xsl',
        '.css', '.scss', '.sass', '.less', '.styl',
        '.vue', '.svelte',
        # Config & Data
        '.json', '.json5', '.jsonc', '.yaml', '.yml', '.toml',
        '.ini', '.cfg', '.conf', '.config', '.properties',
        '.env', '.env.example', '.env.local', '.env.production',
        # Documentation
        '.md', '.markdown', '.rst', '.txt', '.text', '.adoc',
        '.tex', '.org',
        # Scripts
        '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',
        # Database
        '.sql', '.psql', '.mysql', '.graphql', '.gql', '.prisma',
        # Build & CI
        '.gradle', '.maven', '.sbt', '.cake', '.make',
        '.dockerfile', '.containerfile', '.dockerignore',
        '.gitignore', '.npmignore', '.eslintrc', '.prettierrc',
        # Others
        '.proto', '.thrift', '.avro',
        '.vim', '.emacs', '.editorconfig',
        '.lock', '.sum',
    }

    # Special files without extensions
    SPECIAL_FILES = {
        'Dockerfile', 'Containerfile', 'Makefile', 'Rakefile',
        'Gemfile', 'Podfile', 'Cartfile', 'Brewfile',
        'README', 'LICENSE', 'COPYING', 'NOTICE', 'AUTHORS',
        'CHANGELOG', 'CHANGES', 'VERSION', 'TODO',
        'Vagrantfile', 'Procfile', 'Guardfile',
    }

    def __init__(self, zip_path: str, output_dir: Optional[str] = None,
                 config_file: Optional[str] = None):
        """Initialize the advanced extractor."""
        self.zip_path = Path(zip_path)
        if not self.zip_path.exists():
            raise FileNotFoundError(f"Zip file not found: {zip_path}")

        # Load configuration
        self.config = self.load_config(config_file)

        # Create output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            repo_name = self.zip_path.stem
            self.output_dir = Path(f"{repo_name}_output_{timestamp}")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Extraction directory
        self.extract_dir = self.output_dir / "extracted"
        self.extract_dir.mkdir(exist_ok=True)

        # Statistics
        self.repo_stats = RepositoryStats()
        self.dir_tree = DirectoryTree()

    def load_config(self, config_file: Optional[str]) -> Dict:
        """Load configuration from file."""
        default_config = {
            'max_file_size': 10 * 1024 * 1024,  # 10MB
            'max_lines_per_file': 10000,
            'max_lines_in_pdf': 1000,
            'include_stats': True,
            'include_tree': True,
            'syntax_highlighting': PYGMENTS_AVAILABLE,
            'generate_html': True,
            'generate_markdown': True,
            'page_size': 'letter',
            'font_size': 8,
        }

        if config_file and Path(config_file).exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")

        return default_config

    def should_ignore(self, path: Path) -> bool:
        """Check if a file/directory should be ignored."""
        path_str = str(path)
        parts = path.parts

        for part in parts:
            # Exact match
            if part in self.IGNORE_PATTERNS:
                return True

            # Pattern matching
            for pattern in self.IGNORE_PATTERNS:
                if '*' in pattern:
                    ext = pattern.replace('*', '')
                    if part.endswith(ext):
                        return True

            # Hidden files (except special ones)
            if part.startswith('.') and part not in {'.gitignore', '.env.example', '.editorconfig'}:
                # Allow known config files
                if not any(part.endswith(ext) for ext in ['.md', '.txt', '.json', '.yaml', '.yml']):
                    return True

        return False

    def detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding."""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(min(100000, os.path.getsize(file_path)))
                result = chardet.detect(raw_data)
                return result['encoding'] or 'utf-8'
        except Exception:
            return 'utf-8'

    def is_binary_file(self, file_path: Path) -> bool:
        """Check if a file is binary."""
        # Check extension
        if file_path.suffix.lower() in self.BINARY_EXTENSIONS:
            return True

        # Check file size (skip very large files)
        try:
            if os.path.getsize(file_path) > self.config['max_file_size']:
                return True
        except Exception:
            return True

        # Try to read first few bytes
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(8192)
                # If file contains null bytes, it's binary
                if b'\x00' in chunk:
                    return True

                # Check for high proportion of non-text bytes
                non_text = sum(1 for byte in chunk if byte < 32 and byte not in {9, 10, 13})
                if len(chunk) > 0 and non_text / len(chunk) > 0.3:
                    return True
        except Exception:
            return True

        return False

    def is_text_file(self, file_path: Path) -> bool:
        """Check if a file is a text file we should include."""
        # Check extension
        if file_path.suffix.lower() in self.TEXT_EXTENSIONS:
            return True

        # Check special files
        if file_path.name in self.SPECIAL_FILES:
            return True

        # Check UPPERCASE variants
        if file_path.name.upper() in self.SPECIAL_FILES:
            return True

        return False

    def extract_zip(self):
        """Extract the zip file with progress."""
        print(f"\n{'='*80}")
        print(f"Extracting: {self.zip_path.name}")
        print(f"{'='*80}")

        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            members = zip_ref.namelist()

            if TQDM_AVAILABLE:
                for member in tqdm(members, desc="Extracting files", unit="file"):
                    zip_ref.extract(member, self.extract_dir)
            else:
                zip_ref.extractall(self.extract_dir)
                print(f"Extracted {len(members)} items")

    def collect_files(self) -> List[Dict]:
        """Collect all relevant files with metadata."""
        print(f"\n{'='*80}")
        print("Scanning repository...")
        print(f"{'='*80}")

        files_data = []
        all_files = []

        # First pass: collect all files
        for root, dirs, files in os.walk(self.extract_dir):
            # Filter directories
            dirs[:] = [d for d in dirs if not self.should_ignore(Path(root) / d)]

            for file in files:
                file_path = Path(root) / file
                if not self.should_ignore(file_path):
                    all_files.append(file_path)

        # Process files with progress
        iterator = tqdm(all_files, desc="Processing files", unit="file") if TQDM_AVAILABLE else all_files

        for file_path in iterator:
            # Skip binary files
            if self.is_binary_file(file_path):
                continue

            # Only include text files
            if not self.is_text_file(file_path):
                continue

            # Detect encoding and read content
            try:
                encoding = self.detect_encoding(file_path)

                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()

                relative_path = file_path.relative_to(self.extract_dir)

                # Create file stats
                stats = FileStats(file_path, content)
                self.repo_stats.add_file(stats)
                self.dir_tree.add_path(str(relative_path))

                # Limit line count
                lines = content.splitlines()
                if len(lines) > self.config['max_lines_per_file']:
                    content = '\n'.join(lines[:self.config['max_lines_per_file']])
                    content += f"\n\n... (truncated, {len(lines) - self.config['max_lines_per_file']} more lines)"

                files_data.append({
                    'path': str(relative_path),
                    'content': content,
                    'stats': stats,
                    'size': stats.size,
                    'lines': stats.lines,
                    'language': stats.language,
                })

            except Exception as e:
                print(f"\nWarning: Could not read {file_path}: {e}")

        # Sort files by path
        files_data.sort(key=lambda x: x['path'])

        print(f"\nCollected {len(files_data)} files")
        return files_data

    def generate_stats_report(self) -> str:
        """Generate statistics report."""
        stats = self.repo_stats.get_summary()

        report = []
        report.append("=" * 80)
        report.append("REPOSITORY STATISTICS")
        report.append("=" * 80)
        report.append(f"\nTotal Files: {stats['total_files']:,}")
        report.append(f"Total Lines: {stats['total_lines']:,}")
        report.append(f"Total Size: {self.format_size(stats['total_size'])}")

        report.append("\n" + "-" * 80)
        report.append("Languages Breakdown:")
        report.append("-" * 80)

        # Sort by lines
        sorted_langs = sorted(
            stats['languages'].items(),
            key=lambda x: x[1]['lines'],
            reverse=True
        )

        for lang, lang_stats in sorted_langs:
            percentage = (lang_stats['lines'] / stats['total_lines'] * 100) if stats['total_lines'] > 0 else 0
            report.append(
                f"{lang.capitalize():<15} {lang_stats['files']:>6} files  "
                f"{lang_stats['lines']:>8,} lines  {percentage:>5.1f}%"
            )

        report.append("\n" + "-" * 80)
        report.append("File Types:")
        report.append("-" * 80)

        sorted_types = sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)
        for ext, count in sorted_types[:15]:  # Top 15
            ext_display = ext if ext else '(no extension)'
            report.append(f"{ext_display:<20} {count:>6} files")

        return '\n'.join(report)

    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def generate_text_file(self, files_data: List[Dict]) -> Path:
        """Generate comprehensive text file."""
        text_output = self.output_dir / "repository_content.txt"

        print(f"\n{'='*80}")
        print("Generating text file...")
        print(f"{'='*80}")

        with open(text_output, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write(f"REPOSITORY: {self.zip_path.stem}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Files: {len(files_data)}\n")
            f.write("=" * 80 + "\n\n")

            # Statistics
            if self.config['include_stats']:
                f.write(self.generate_stats_report())
                f.write("\n\n")

            # Directory tree
            if self.config['include_tree']:
                f.write("=" * 80 + "\n")
                f.write("DIRECTORY STRUCTURE\n")
                f.write("=" * 80 + "\n")
                f.write(self.dir_tree.build_tree_string())
                f.write("\n\n")

            # Table of contents
            f.write("=" * 80 + "\n")
            f.write("TABLE OF CONTENTS\n")
            f.write("=" * 80 + "\n")
            for idx, file_data in enumerate(files_data, 1):
                f.write(f"{idx:4d}. {file_data['path']}\n")
            f.write("\n\n")

            # Files
            f.write("=" * 80 + "\n")
            f.write("FILE CONTENTS\n")
            f.write("=" * 80 + "\n\n")

            for idx, file_data in enumerate(files_data, 1):
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"[{idx}/{len(files_data)}] {file_data['path']}\n")
                f.write(f"Language: {file_data['language']} | Lines: {file_data['lines']} | Size: {self.format_size(file_data['size'])}\n")
                f.write("=" * 80 + "\n\n")
                f.write(file_data['content'])
                f.write("\n\n")

        print(f"✓ Text file saved: {text_output.name}")
        return text_output

    def generate_markdown(self, files_data: List[Dict]) -> Path:
        """Generate Markdown documentation."""
        md_output = self.output_dir / "repository_content.md"

        print("Generating Markdown file...")

        with open(md_output, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# {self.zip_path.stem}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total Files:** {len(files_data)}\n\n")
            f.write("---\n\n")

            # Statistics
            if self.config['include_stats']:
                f.write("## Statistics\n\n")
                stats = self.repo_stats.get_summary()
                f.write(f"- **Total Files:** {stats['total_files']:,}\n")
                f.write(f"- **Total Lines:** {stats['total_lines']:,}\n")
                f.write(f"- **Total Size:** {self.format_size(stats['total_size'])}\n\n")

                f.write("### Languages\n\n")
                f.write("| Language | Files | Lines | Percentage |\n")
                f.write("|----------|-------|-------|------------|\n")

                sorted_langs = sorted(stats['languages'].items(), key=lambda x: x[1]['lines'], reverse=True)
                for lang, lang_stats in sorted_langs:
                    percentage = (lang_stats['lines'] / stats['total_lines'] * 100) if stats['total_lines'] > 0 else 0
                    f.write(f"| {lang.capitalize()} | {lang_stats['files']} | {lang_stats['lines']:,} | {percentage:.1f}% |\n")
                f.write("\n")

            # Directory tree
            if self.config['include_tree']:
                f.write("## Directory Structure\n\n")
                f.write("```\n")
                f.write(self.dir_tree.build_tree_string())
                f.write("\n```\n\n")

            # Table of contents
            f.write("## Table of Contents\n\n")
            for idx, file_data in enumerate(files_data, 1):
                anchor = file_data['path'].replace('/', '-').replace('.', '').replace(' ', '-').lower()
                f.write(f"{idx}. [{file_data['path']}](#{anchor})\n")
            f.write("\n---\n\n")

            # Files
            f.write("## Files\n\n")
            for idx, file_data in enumerate(files_data, 1):
                anchor = file_data['path'].replace('/', '-').replace('.', '').replace(' ', '-').lower()
                f.write(f"### {file_data['path']}\n\n")
                f.write(f"**Language:** {file_data['language']} | ")
                f.write(f"**Lines:** {file_data['lines']} | ")
                f.write(f"**Size:** {self.format_size(file_data['size'])}\n\n")

                # Code block with language
                lang = file_data['language']
                if lang == 'c++':
                    lang = 'cpp'
                elif lang == 'c#':
                    lang = 'csharp'

                f.write(f"```{lang}\n")
                f.write(file_data['content'])
                f.write("\n```\n\n")
                f.write("---\n\n")

        print(f"✓ Markdown file saved: {md_output.name}")
        return md_output

    def generate_html(self, files_data: List[Dict]) -> Path:
        """Generate HTML documentation with syntax highlighting."""
        html_output = self.output_dir / "repository_content.html"

        print("Generating HTML file...")

        with open(html_output, 'w', encoding='utf-8') as f:
            # HTML header
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            margin-bottom: 30px;
            border-radius: 8px;
        }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        h2 {{ color: #667eea; margin: 30px 0 15px; padding-bottom: 10px; border-bottom: 2px solid #667eea; }}
        h3 {{ color: #764ba2; margin: 20px 0 10px; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-card h3 {{ color: white; margin: 0; font-size: 2em; }}
        .stat-card p {{ margin: 5px 0 0; opacity: 0.9; }}
        .toc {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .toc ul {{ list-style: none; column-count: 2; column-gap: 20px; }}
        .toc li {{ margin: 5px 0; }}
        .toc a {{
            color: #667eea;
            text-decoration: none;
            padding: 5px 10px;
            display: block;
            border-radius: 4px;
            transition: background 0.3s;
        }}
        .toc a:hover {{ background: #e7e9fc; }}
        .file-section {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .file-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        .file-meta {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        .file-meta span {{
            background: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9em;
            line-height: 1.5;
        }}
        code {{ font-family: 'Courier New', Courier, monospace; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
        tr:hover {{ background: #f8f9fa; }}
        .tree {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', Courier, monospace;
            overflow-x: auto;
        }}
        nav {{
            position: sticky;
            top: 0;
            background: white;
            padding: 10px 0;
            border-bottom: 2px solid #667eea;
            margin-bottom: 20px;
            z-index: 100;
        }}
        nav a {{
            color: #667eea;
            text-decoration: none;
            padding: 8px 15px;
            margin: 0 5px;
            border-radius: 4px;
            transition: background 0.3s;
        }}
        nav a:hover {{ background: #e7e9fc; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p>Generated: {date}</p>
        </header>

        <nav>
            <a href="#stats">Statistics</a>
            <a href="#tree">Directory Tree</a>
            <a href="#toc">Table of Contents</a>
            <a href="#files">Files</a>
        </nav>
""".format(
                title=self.zip_path.stem,
                date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))

            # Statistics
            if self.config['include_stats']:
                stats = self.repo_stats.get_summary()
                f.write('        <section id="stats">\n')
                f.write('            <h2>Statistics</h2>\n')
                f.write('            <div class="stats">\n')
                f.write(f'                <div class="stat-card"><h3>{stats["total_files"]:,}</h3><p>Files</p></div>\n')
                f.write(f'                <div class="stat-card"><h3>{stats["total_lines"]:,}</h3><p>Lines</p></div>\n')
                f.write(f'                <div class="stat-card"><h3>{self.format_size(stats["total_size"])}</h3><p>Size</p></div>\n')
                f.write('            </div>\n')

                f.write('            <h3>Languages</h3>\n')
                f.write('            <table>\n')
                f.write('                <tr><th>Language</th><th>Files</th><th>Lines</th><th>Percentage</th></tr>\n')

                sorted_langs = sorted(stats['languages'].items(), key=lambda x: x[1]['lines'], reverse=True)
                for lang, lang_stats in sorted_langs:
                    percentage = (lang_stats['lines'] / stats['total_lines'] * 100) if stats['total_lines'] > 0 else 0
                    f.write(f'                <tr><td>{lang.capitalize()}</td><td>{lang_stats["files"]}</td>'
                           f'<td>{lang_stats["lines"]:,}</td><td>{percentage:.1f}%</td></tr>\n')
                f.write('            </table>\n')
                f.write('        </section>\n')

            # Directory tree
            if self.config['include_tree']:
                f.write('        <section id="tree">\n')
                f.write('            <h2>Directory Structure</h2>\n')
                f.write('            <div class="tree">\n')
                tree_str = self.dir_tree.build_tree_string().replace('<', '&lt;').replace('>', '&gt;')
                f.write(f'                <pre>{tree_str}</pre>\n')
                f.write('            </div>\n')
                f.write('        </section>\n')

            # Table of contents
            f.write('        <section id="toc">\n')
            f.write('            <h2>Table of Contents</h2>\n')
            f.write('            <div class="toc">\n')
            f.write('                <ul>\n')
            for idx, file_data in enumerate(files_data, 1):
                file_id = f"file-{idx}"
                f.write(f'                    <li><a href="#{file_id}">{file_data["path"]}</a></li>\n')
            f.write('                </ul>\n')
            f.write('            </div>\n')
            f.write('        </section>\n')

            # Files
            f.write('        <section id="files">\n')
            f.write('            <h2>Files</h2>\n')

            for idx, file_data in enumerate(files_data, 1):
                file_id = f"file-{idx}"
                f.write(f'            <div class="file-section" id="{file_id}">\n')
                f.write('                <div class="file-header">\n')
                f.write(f'                    <h3>{file_data["path"]}</h3>\n')
                f.write('                    <div class="file-meta">\n')
                f.write(f'                        <span>📝 {file_data["language"]}</span>\n')
                f.write(f'                        <span>📊 {file_data["lines"]} lines</span>\n')
                f.write(f'                        <span>💾 {self.format_size(file_data["size"])}</span>\n')
                f.write('                    </div>\n')
                f.write('                </div>\n')

                # Code with syntax highlighting
                content = file_data['content']

                if PYGMENTS_AVAILABLE and self.config['syntax_highlighting']:
                    try:
                        lexer = get_lexer_for_filename(file_data['path'])
                        formatter = HtmlFormatter(style='monokai', noclasses=True, linenos='inline')
                        highlighted = highlight(content, lexer, formatter)
                        f.write(f'                {highlighted}\n')
                    except:
                        # Fallback to plain pre
                        content_escaped = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        f.write(f'                <pre><code>{content_escaped}</code></pre>\n')
                else:
                    content_escaped = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    f.write(f'                <pre><code>{content_escaped}</code></pre>\n')

                f.write('            </div>\n')

            f.write('        </section>\n')

            # Footer
            f.write("""    </div>
    <script>
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    </script>
</body>
</html>
""")

        print(f"✓ HTML file saved: {html_output.name}")
        return html_output

    def generate_pdf(self, files_data: List[Dict]) -> Optional[Path]:
        """Generate advanced PDF with table of contents and better formatting."""
        pdf_output = self.output_dir / "repository_content.pdf"

        print("Generating PDF file...")

        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                str(pdf_output),
                pagesize=letter if self.config['page_size'] == 'letter' else A4,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch,
                title=f"Repository: {self.zip_path.stem}"
            )

            story = []
            styles = getSampleStyleSheet()

            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=HexColor('#1a1a1a'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )

            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=HexColor('#667eea'),
                spaceAfter=12,
                spaceBefore=12,
            )

            file_header_style = ParagraphStyle(
                'FileHeader',
                parent=styles['Heading2'],
                fontSize=10,
                textColor=HexColor('#764ba2'),
                spaceAfter=6,
                spaceBefore=10,
                leftIndent=0,
                fontName='Helvetica-Bold'
            )

            code_style = ParagraphStyle(
                'Code',
                parent=styles['Code'],
                fontSize=self.config['font_size'],
                leftIndent=10,
                fontName='Courier',
                textColor=HexColor('#2d2d2d'),
                leading=self.config['font_size'] + 2,
            )

            # Title page
            story.append(Spacer(1, 1*inch))
            story.append(Paragraph(f"<b>{self.zip_path.stem}</b>", title_style))
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                ParagraphStyle('center', parent=styles['Normal'], alignment=TA_CENTER)
            ))
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(
                f"Total Files: {len(files_data)}",
                ParagraphStyle('center', parent=styles['Normal'], alignment=TA_CENTER)
            ))
            story.append(PageBreak())

            # Statistics
            if self.config['include_stats']:
                story.append(Paragraph("Repository Statistics", heading_style))

                stats = self.repo_stats.get_summary()

                # Stats table
                stats_data = [
                    ['Metric', 'Value'],
                    ['Total Files', f"{stats['total_files']:,}"],
                    ['Total Lines', f"{stats['total_lines']:,}"],
                    ['Total Size', self.format_size(stats['total_size'])],
                ]

                stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#667eea')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
                ]))
                story.append(stats_table)
                story.append(Spacer(1, 0.2*inch))

                # Language breakdown
                story.append(Paragraph("Languages", ParagraphStyle('subheading', parent=styles['Heading3'])))

                lang_data = [['Language', 'Files', 'Lines', 'Percentage']]
                sorted_langs = sorted(stats['languages'].items(), key=lambda x: x[1]['lines'], reverse=True)

                for lang, lang_stats in sorted_langs[:10]:  # Top 10
                    percentage = (lang_stats['lines'] / stats['total_lines'] * 100) if stats['total_lines'] > 0 else 0
                    lang_data.append([
                        lang.capitalize(),
                        str(lang_stats['files']),
                        f"{lang_stats['lines']:,}",
                        f"{percentage:.1f}%"
                    ])

                lang_table = Table(lang_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 1.5*inch])
                lang_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#764ba2')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
                ]))
                story.append(lang_table)
                story.append(PageBreak())

            # Directory tree
            if self.config['include_tree']:
                story.append(Paragraph("Directory Structure", heading_style))
                tree_str = self.dir_tree.build_tree_string()
                story.append(Preformatted(tree_str, code_style))
                story.append(PageBreak())

            # Table of contents
            story.append(Paragraph("Table of Contents", heading_style))
            story.append(Spacer(1, 0.1*inch))

            for idx, file_data in enumerate(files_data, 1):
                toc_entry = Paragraph(f"{idx}. {file_data['path']}", styles['Normal'])
                story.append(toc_entry)

            story.append(PageBreak())

            # Files
            story.append(Paragraph("File Contents", heading_style))
            story.append(Spacer(1, 0.2*inch))

            for idx, file_data in enumerate(files_data, 1):
                # File header
                file_header = Paragraph(
                    f"[{idx}/{len(files_data)}] {file_data['path']}",
                    file_header_style
                )

                # File metadata
                meta_text = (
                    f"<i>Language: {file_data['language']} | "
                    f"Lines: {file_data['lines']} | "
                    f"Size: {self.format_size(file_data['size'])}</i>"
                )
                file_meta = Paragraph(meta_text, styles['Normal'])

                # Content
                content = file_data['content']
                lines = content.split('\n')

                # Limit lines for PDF
                if len(lines) > self.config['max_lines_in_pdf']:
                    lines = lines[:self.config['max_lines_in_pdf']]
                    lines.append(f"... (truncated, {file_data['lines'] - self.config['max_lines_in_pdf']} more lines)")
                    content = '\n'.join(lines)

                # Escape special characters
                content_safe = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                # Keep file header and content together
                file_content = [
                    file_header,
                    file_meta,
                    Spacer(1, 0.05*inch),
                    Preformatted(content_safe, code_style),
                    Spacer(1, 0.2*inch),
                ]

                story.append(KeepTogether(file_content))

                # Page break between files
                if idx < len(files_data):
                    story.append(PageBreak())

            # Build PDF
            doc.build(story)
            print(f"✓ PDF saved: {pdf_output.name}")
            return pdf_output

        except Exception as e:
            print(f"✗ Error generating PDF: {e}")
            import traceback
            traceback.print_exc()
            return None

    def save_stats_json(self):
        """Save statistics as JSON."""
        json_output = self.output_dir / "repository_stats.json"

        stats = self.repo_stats.get_summary()
        stats['repository'] = self.zip_path.stem
        stats['generated_at'] = datetime.now().isoformat()

        with open(json_output, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)

        print(f"✓ Stats JSON saved: {json_output.name}")

    def process(self):
        """Main processing method."""
        print(f"\n{'='*80}")
        print("ADVANCED GIT ZIP EXTRACTOR")
        print(f"{'='*80}")
        print(f"Source: {self.zip_path}")
        print(f"Output: {self.output_dir}")
        print(f"{'='*80}")

        # Extract
        self.extract_zip()

        # Collect files
        files_data = self.collect_files()

        if not files_data:
            print("\n⚠ Warning: No files found to process!")
            return

        # Generate outputs
        print(f"\n{'='*80}")
        print("Generating output files...")
        print(f"{'='*80}")

        self.generate_text_file(files_data)

        if self.config['generate_markdown']:
            self.generate_markdown(files_data)

        if self.config['generate_html']:
            self.generate_html(files_data)

        self.generate_pdf(files_data)

        self.save_stats_json()

        # Summary
        print(f"\n{'='*80}")
        print("✓ PROCESSING COMPLETE!")
        print(f"{'='*80}")
        print(f"\nOutput directory: {self.output_dir.absolute()}")
        print(f"\nGenerated files:")
        for file in sorted(self.output_dir.glob('repository_*')):
            print(f"  • {file.name}")
        print(f"\n{self.generate_stats_report()}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Advanced Git Repository Extractor - Convert git repos to multiple formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s repo.zip                    # Basic usage
  %(prog)s repo.zip -o output          # Custom output directory
  %(prog)s repo.zip -c config.json     # Use config file
  %(prog)s repo.zip --no-html          # Skip HTML generation
        """
    )

    parser.add_argument(
        'zip_file',
        help='Path to the git repository zip file'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output directory (default: creates new folder with timestamp)',
        default=None
    )
    parser.add_argument(
        '-c', '--config',
        help='Configuration file (JSON)',
        default=None
    )
    parser.add_argument(
        '--no-html',
        help='Skip HTML generation',
        action='store_true'
    )
    parser.add_argument(
        '--no-markdown',
        help='Skip Markdown generation',
        action='store_true'
    )
    parser.add_argument(
        '--no-stats',
        help='Skip statistics',
        action='store_true'
    )

    args = parser.parse_args()

    try:
        extractor = AdvancedGitZipExtractor(args.zip_file, args.output, args.config)

        # Override config with command-line args
        if args.no_html:
            extractor.config['generate_html'] = False
        if args.no_markdown:
            extractor.config['generate_markdown'] = False
        if args.no_stats:
            extractor.config['include_stats'] = False

        extractor.process()

    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
