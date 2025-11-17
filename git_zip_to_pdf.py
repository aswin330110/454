#!/usr/bin/env python3
"""
Git Zip Extractor Tool
Extracts a git repository from a zip file and converts it to PDF and text formats.
"""

import os
import sys
import zipfile
import argparse
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor


class GitZipExtractor:
    """Extract and convert git repository to PDF and text formats."""

    # Files and directories to ignore
    IGNORE_PATTERNS = {
        '.git', '.gitignore', '.DS_Store', '__pycache__',
        'node_modules', '.venv', 'venv', '.idea', '.vscode',
        '*.pyc', '*.pyo', '*.pyd', '.pytest_cache', '.coverage',
        '*.egg-info', 'dist', 'build', '.tox'
    }

    # Binary file extensions to skip
    BINARY_EXTENSIONS = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
        '.pdf', '.zip', '.tar', '.gz', '.rar', '.7z',
        '.exe', '.dll', '.so', '.dylib',
        '.mp3', '.mp4', '.avi', '.mov', '.wav',
        '.bin', '.dat', '.db', '.sqlite'
    }

    # Text file extensions that are safe to include
    TEXT_EXTENSIONS = {
        '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp',
        '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt',
        '.html', '.css', '.scss', '.sass', '.less',
        '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg',
        '.md', '.txt', '.rst', '.log',
        '.sh', '.bash', '.zsh', '.fish',
        '.sql', '.graphql', '.proto',
        '.dockerfile', '.gitignore', '.env.example'
    }

    def __init__(self, zip_path, output_dir=None):
        """
        Initialize the extractor.

        Args:
            zip_path: Path to the zip file
            output_dir: Directory to save outputs (default: creates new folder)
        """
        self.zip_path = Path(zip_path)
        if not self.zip_path.exists():
            raise FileNotFoundError(f"Zip file not found: {zip_path}")

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

    def should_ignore(self, path):
        """Check if a file/directory should be ignored."""
        path_str = str(path)
        parts = Path(path_str).parts

        # Check if any part matches ignore patterns
        for part in parts:
            if part in self.IGNORE_PATTERNS:
                return True
            # Check for pattern matching (*.pyc, etc.)
            for pattern in self.IGNORE_PATTERNS:
                if '*' in pattern:
                    ext = pattern.replace('*', '')
                    if part.endswith(ext):
                        return True
        return False

    def is_binary_file(self, file_path):
        """Check if a file is binary."""
        # Check extension
        if file_path.suffix.lower() in self.BINARY_EXTENSIONS:
            return True

        # Try to read first few bytes
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                # If file contains null bytes, it's likely binary
                if b'\x00' in chunk:
                    return True
        except Exception:
            return True

        return False

    def is_text_file(self, file_path):
        """Check if a file is a text file we should include."""
        # Check if extension is in our text extensions list
        if file_path.suffix.lower() in self.TEXT_EXTENSIONS:
            return True

        # Check files without extension (like Dockerfile, Makefile)
        if not file_path.suffix and file_path.name in ['Dockerfile', 'Makefile', 'README', 'LICENSE']:
            return True

        return False

    def extract_zip(self):
        """Extract the zip file."""
        print(f"Extracting {self.zip_path}...")
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_dir)
        print(f"Extracted to {self.extract_dir}")

    def collect_files(self):
        """Collect all relevant files from the extracted repository."""
        files_data = []

        for root, dirs, files in os.walk(self.extract_dir):
            # Filter directories to ignore
            dirs[:] = [d for d in dirs if not self.should_ignore(Path(root) / d)]

            for file in sorted(files):
                file_path = Path(root) / file

                # Skip ignored files
                if self.should_ignore(file_path):
                    continue

                # Skip binary files
                if self.is_binary_file(file_path):
                    continue

                # Only include text files
                if not self.is_text_file(file_path):
                    continue

                # Read file content
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    relative_path = file_path.relative_to(self.extract_dir)
                    files_data.append({
                        'path': str(relative_path),
                        'content': content
                    })
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")

        return files_data

    def generate_text_file(self, files_data):
        """Generate a formatted text file from the repository."""
        text_output = self.output_dir / "repository_content.txt"

        print(f"Generating text file: {text_output}")

        with open(text_output, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"Repository: {self.zip_path.stem}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total files: {len(files_data)}\n")
            f.write("=" * 80 + "\n\n")

            for file_data in files_data:
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"File: {file_data['path']}\n")
                f.write("=" * 80 + "\n")
                f.write(file_data['content'])
                f.write("\n\n")

        print(f"Text file saved: {text_output}")
        return text_output

    def generate_pdf(self, files_data):
        """Generate a formatted PDF from the repository."""
        pdf_output = self.output_dir / "repository_content.pdf"

        print(f"Generating PDF: {pdf_output}")

        # Create PDF document
        doc = SimpleDocTemplate(
            str(pdf_output),
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        # Container for PDF elements
        story = []

        # Styles
        styles = getSampleStyleSheet()

        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=HexColor('#1a1a1a'),
            spaceAfter=12,
            alignment=TA_LEFT
        )

        # File header style
        file_header_style = ParagraphStyle(
            'FileHeader',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=HexColor('#0066cc'),
            spaceAfter=6,
            spaceBefore=6,
            alignment=TA_LEFT
        )

        # Code style
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Code'],
            fontSize=8,
            leftIndent=20,
            fontName='Courier',
            textColor=HexColor('#2d2d2d')
        )

        # Add title page
        story.append(Paragraph(f"Repository: {self.zip_path.stem}", title_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Paragraph(f"Total files: {len(files_data)}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        story.append(PageBreak())

        # Add files
        for idx, file_data in enumerate(files_data):
            # File header
            story.append(Paragraph(f"File: {file_data['path']}", file_header_style))
            story.append(Spacer(1, 0.1*inch))

            # File content - split into lines and add as preformatted
            content = file_data['content']

            # Limit very long files
            lines = content.split('\n')
            if len(lines) > 500:
                lines = lines[:500] + ['... (file truncated for PDF)']
                content = '\n'.join(lines)

            # Add content as preformatted text
            try:
                # Escape special characters for reportlab
                content_safe = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Preformatted(content_safe, code_style))
            except Exception as e:
                story.append(Paragraph(f"[Error displaying content: {e}]", styles['Normal']))

            story.append(Spacer(1, 0.2*inch))

            # Add page break between files (except for the last one)
            if idx < len(files_data) - 1:
                story.append(PageBreak())

        # Build PDF
        try:
            doc.build(story)
            print(f"PDF saved: {pdf_output}")
            return pdf_output
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None

    def process(self):
        """Main processing method."""
        print("\n" + "=" * 80)
        print("Git Zip Extractor Tool")
        print("=" * 80 + "\n")

        # Extract zip
        self.extract_zip()

        # Collect files
        print("\nCollecting files...")
        files_data = self.collect_files()
        print(f"Found {len(files_data)} files to process")

        if not files_data:
            print("Warning: No files found to process!")
            return

        # Generate outputs
        text_file = self.generate_text_file(files_data)
        pdf_file = self.generate_pdf(files_data)

        print("\n" + "=" * 80)
        print("Processing complete!")
        print("=" * 80)
        print(f"\nOutput directory: {self.output_dir.absolute()}")
        print(f"Text file: {text_file.name}")
        if pdf_file:
            print(f"PDF file: {pdf_file.name}")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Extract git repository from zip and convert to PDF and text formats'
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

    args = parser.parse_args()

    try:
        extractor = GitZipExtractor(args.zip_file, args.output)
        extractor.process()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
