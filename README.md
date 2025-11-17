# Git Zip Extractor Tool

A Python tool that extracts a git repository from a zip file and converts it into both PDF and text formats with proper formatting and alignment.

## Features

- ✅ Extracts git repositories from zip files
- ✅ Generates a formatted PDF with syntax-friendly layout
- ✅ Generates a formatted text file
- ✅ Automatically ignores common non-source files (node_modules, .git, binaries, etc.)
- ✅ Handles multiple programming languages and file types
- ✅ Creates organized output in a new folder
- ✅ Proper alignment and formatting for code readability
- ✅ Skips binary files and includes only text-based source files

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install reportlab
```

## Usage

### Basic Usage

```bash
python git_zip_to_pdf.py <path-to-zip-file>
```

Example:
```bash
python git_zip_to_pdf.py my-repository.zip
```

This will create a new folder named `my-repository_output_TIMESTAMP` containing:
- `repository_content.pdf` - PDF version of the repository
- `repository_content.txt` - Text version of the repository
- `extracted/` - The extracted repository files

### Specify Output Directory

```bash
python git_zip_to_pdf.py <path-to-zip-file> -o <output-directory>
```

Example:
```bash
python git_zip_to_pdf.py my-repository.zip -o ./output
```

### Help

```bash
python git_zip_to_pdf.py --help
```

## What Gets Included

### Included Files

The tool includes the following types of files:
- **Source Code**: `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.java`, `.c`, `.cpp`, `.h`, `.go`, `.rs`, `.rb`, `.php`, `.swift`, `.kt`, etc.
- **Web Files**: `.html`, `.css`, `.scss`, `.sass`, `.less`
- **Configuration**: `.json`, `.xml`, `.yaml`, `.yml`, `.toml`, `.ini`, `.cfg`
- **Documentation**: `.md`, `.txt`, `.rst`
- **Scripts**: `.sh`, `.bash`, `.zsh`, `.fish`
- **Database**: `.sql`, `.graphql`, `.proto`
- **Special Files**: `Dockerfile`, `Makefile`, `README`, `LICENSE`, etc.

### Excluded Files/Directories

The tool automatically excludes:
- `.git` directory and git-related files
- `node_modules`, `.venv`, `venv`
- `__pycache__`, `.pytest_cache`
- Binary files (images, videos, executables, archives)
- IDE configuration directories (`.idea`, `.vscode`)
- Build artifacts (`dist`, `build`, `.egg-info`)

## Output Format

### PDF Format

The PDF includes:
- Title page with repository name, generation date, and file count
- Each file on its own section with:
  - File path as a header
  - Formatted code content with proper indentation
  - Monospace font for code readability
  - Color-coded headers for easy navigation

### Text Format

The text file includes:
- Header with repository information
- Each file separated by clear delimiters
- Original file path and content
- Maintains original formatting and indentation

## Examples

### Example 1: Process a downloaded repository

```bash
# Download a repository as zip from GitHub
# (e.g., https://github.com/username/repo/archive/refs/heads/main.zip)

python git_zip_to_pdf.py repo-main.zip
```

Output structure:
```
repo-main_output_20231117_143022/
├── repository_content.pdf
├── repository_content.txt
└── extracted/
    └── repo-main/
        └── (repository files)
```

### Example 2: Custom output location

```bash
python git_zip_to_pdf.py project.zip -o my-docs
```

Output structure:
```
my-docs/
├── repository_content.pdf
├── repository_content.txt
└── extracted/
    └── (repository files)
```

## Advanced Configuration

You can modify the following in `git_zip_to_pdf.py`:

### Add More File Extensions

Edit the `TEXT_EXTENSIONS` set in the `GitZipExtractor` class:

```python
TEXT_EXTENSIONS = {
    '.py', '.js', # ... existing extensions
    '.your_extension',  # Add your custom extension
}
```

### Add More Ignore Patterns

Edit the `IGNORE_PATTERNS` set:

```python
IGNORE_PATTERNS = {
    '.git', 'node_modules',  # ... existing patterns
    'your_folder',  # Add custom folder to ignore
}
```

### Modify PDF Styling

Adjust the styles in the `generate_pdf` method:

```python
# Title style
title_style = ParagraphStyle(
    'CustomTitle',
    fontSize=16,  # Change font size
    textColor=HexColor('#1a1a1a'),  # Change color
    # ... other properties
)
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'reportlab'"

**Solution**: Install reportlab:
```bash
pip install reportlab
```

### Issue: "FileNotFoundError: Zip file not found"

**Solution**: Ensure the path to your zip file is correct. Use absolute paths if needed:
```bash
python git_zip_to_pdf.py /full/path/to/your/file.zip
```

### Issue: "No files found to process!"

**Solution**: This may occur if:
- The zip file is empty
- All files are binary or in ignored directories
- Check if the zip contains a valid repository structure

### Issue: PDF generation fails or produces errors

**Solution**:
- Very large files (>500 lines) are automatically truncated in the PDF
- If you encounter memory issues, consider processing smaller repositories or splitting them

## Limitations

- Very large repositories may take time to process
- PDF files have a line limit per file (500 lines) to prevent memory issues
- Binary files are automatically skipped
- Some special characters in code may need escaping for PDF generation

## License

This tool is provided as-is for personal and educational use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Author

Created to help developers document and share repository contents in readable formats.
