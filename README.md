# Advanced Git Zip Extractor Tool

A powerful Python tool that extracts git repositories from zip files and converts them into multiple professional formats with advanced features including syntax highlighting, statistics, and beautiful visualizations.

## 🚀 Features

### Core Features
- ✅ **Multiple Output Formats**: PDF, HTML, Markdown, and Text
- ✅ **Syntax Highlighting**: Beautiful code highlighting in HTML output
- ✅ **Repository Statistics**: Comprehensive analysis of files, languages, and sizes
- ✅ **Directory Tree Visualization**: Visual representation of repository structure
- ✅ **Progress Bars**: Real-time feedback during processing
- ✅ **Smart Encoding Detection**: Automatically detects and handles different file encodings
- ✅ **Configurable**: JSON configuration file support for customization

### Advanced Features
- 📊 **Detailed Statistics**: File counts, line counts, language breakdown, size analysis
- 🎨 **Professional PDF**: Tables, styled headers, table of contents
- 🌐 **Interactive HTML**: Smooth scrolling, responsive design, navigation menu
- 📝 **Markdown Export**: GitHub-flavored markdown with code blocks
- 🌲 **Directory Trees**: ASCII tree visualization of repository structure
- 🎯 **Smart File Detection**: Comprehensive support for 100+ file types
- 🔍 **Accurate Language Detection**: Recognizes 50+ programming languages
- ⚡ **Performance Optimized**: Handles large repositories efficiently
- 🛡️ **Binary File Filtering**: Automatically excludes images, executables, etc.
- 📈 **JSON Stats Export**: Machine-readable statistics

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

The tool requires:
- **reportlab** (required): PDF generation
- **Pygments** (recommended): Syntax highlighting
- **tqdm** (recommended): Progress bars
- **chardet** (required): Encoding detection
- **Flask** (for web interface): Web server
- **Werkzeug** (for web interface): WSGI utilities

## 🌐 Web Interface (Easiest Way - Perfect for Windows!)

### Quick Start

**Windows Users:**
1. Double-click `START_WEB_INTERFACE.bat`
2. Open browser to `http://localhost:5000`
3. Drag & drop your ZIP file
4. Click "Process Repository"
5. Download your files!

**Mac/Linux Users:**
```bash
./start_web_interface.sh
# Then open http://localhost:5000
```

### Features

- 📤 **Drag & Drop Upload** - Modern, intuitive interface
- ⚡ **Real-Time Progress** - Live updates during processing
- 📊 **Beautiful Results** - Interactive statistics dashboard
- 🎨 **Modern Design** - Gradient backgrounds, smooth animations
- ⚙️ **Configurable** - Choose output formats and options
- 🌐 **Browser-Based** - No command line needed!

### How to Use

1. **Start the Server**
   - Windows: Double-click `START_WEB_INTERFACE.bat`
   - Mac/Linux: Run `./start_web_interface.sh`

2. **Open Browser**
   - Navigate to `http://localhost:5000`

3. **Upload ZIP File**
   - Drag and drop your repository ZIP
   - Or click to browse

4. **Configure Options** (optional)
   - Choose output formats (HTML, PDF, Markdown)
   - Enable/disable statistics and features

5. **Process**
   - Click "Process Repository"
   - Watch real-time progress

6. **Download Results**
   - View statistics and charts
   - Download all generated files
   - Preview HTML in browser

See [WEB_INTERFACE_README.md](WEB_INTERFACE_README.md) for detailed web interface documentation.

## 🎯 Command Line Usage

### Basic Usage

```bash
python git_zip_to_pdf.py <path-to-zip-file>
```

Example:
```bash
python git_zip_to_pdf.py my-repository.zip
```

This creates a timestamped output folder containing:
- `repository_content.pdf` - Professional PDF with formatting
- `repository_content.html` - Interactive HTML with syntax highlighting
- `repository_content.md` - Markdown documentation
- `repository_content.txt` - Plain text version
- `repository_stats.json` - Statistics in JSON format
- `extracted/` - The extracted repository files

### Advanced Usage

#### Custom Output Directory
```bash
python git_zip_to_pdf.py repo.zip -o my-output-folder
```

#### Use Configuration File
```bash
python git_zip_to_pdf.py repo.zip -c config.json
```

#### Skip Specific Outputs
```bash
python git_zip_to_pdf.py repo.zip --no-html --no-markdown
```

### Command-Line Options

```
positional arguments:
  zip_file              Path to the git repository zip file

options:
  -h, --help            Show help message
  -o, --output DIR      Output directory (default: creates timestamped folder)
  -c, --config FILE     Configuration file (JSON)
  --no-html             Skip HTML generation
  --no-markdown         Skip Markdown generation
  --no-stats            Skip statistics in output
```

## ⚙️ Configuration

Create a `config.json` file to customize behavior:

```json
{
  "max_file_size": 10485760,
  "max_lines_per_file": 10000,
  "max_lines_in_pdf": 1000,
  "include_stats": true,
  "include_tree": true,
  "syntax_highlighting": true,
  "generate_html": true,
  "generate_markdown": true,
  "page_size": "letter",
  "font_size": 8
}
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `max_file_size` | 10MB | Maximum file size to process (bytes) |
| `max_lines_per_file` | 10000 | Maximum lines to read from a single file |
| `max_lines_in_pdf` | 1000 | Maximum lines per file in PDF output |
| `include_stats` | true | Include repository statistics |
| `include_tree` | true | Include directory tree visualization |
| `syntax_highlighting` | true | Enable syntax highlighting in HTML |
| `generate_html` | true | Generate HTML output |
| `generate_markdown` | true | Generate Markdown output |
| `page_size` | "letter" | PDF page size ("letter" or "A4") |
| `font_size` | 8 | Font size for code in PDF |

## 📋 Supported File Types

### Programming Languages (50+)
Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, R, Julia, Lua, Perl, Dart, Elixir, Clojure, Haskell, Elm, OCaml, Erlang

### Web Technologies
HTML, CSS, SCSS, Sass, Less, Vue, Svelte, JSX, TSX

### Data & Config
JSON, YAML, TOML, XML, INI, ENV

### Documentation
Markdown, reStructuredText, AsciiDoc, LaTeX

### Database
SQL, PostgreSQL, MySQL, GraphQL, Prisma

### Scripts & Build
Shell, Bash, PowerShell, Batch, Makefile, Dockerfile

### And Many More!

## 🎨 Output Formats

### 1. PDF Output
- **Professional Layout**: Styled headers, tables, and code blocks
- **Table of Contents**: Easy navigation through files
- **Statistics Section**: Visual tables with file and language stats
- **Directory Tree**: ASCII visualization of repository structure
- **Formatted Code**: Monospace font with proper indentation
- **File Metadata**: Language, line count, and size for each file
- **Page Management**: Automatic page breaks between files

### 2. HTML Output
- **Modern Design**: Responsive, gradient headers, card layouts
- **Syntax Highlighting**: Pygments-powered code highlighting
- **Interactive Navigation**: Sticky nav menu, smooth scrolling
- **Statistics Dashboard**: Visual stat cards and tables
- **Mobile-Friendly**: Responsive design for all devices
- **Dark Code Blocks**: Professional Monokai theme

### 3. Markdown Output
- **GitHub-Flavored**: Compatible with GitHub, GitLab, etc.
- **Code Blocks**: Language-specific syntax blocks
- **Clickable TOC**: Anchor links to each file
- **Statistics Tables**: Formatted tables for stats
- **Directory Tree**: Monospace tree visualization

### 4. Text Output
- **Plain Text**: Universal compatibility
- **Clear Sections**: Delimited file boundaries
- **Full Statistics**: Complete stats in text format
- **Table of Contents**: Numbered file listing
- **Metadata**: Language and size info for each file

### 5. JSON Stats
- **Machine-Readable**: Perfect for automation
- **Complete Metrics**: All statistics in structured format
- **Language Breakdown**: Detailed per-language stats
- **File Type Analysis**: File extension distribution

## 📊 Statistics & Analysis

The tool provides comprehensive repository analysis:

### File Statistics
- Total number of files
- Total lines of code
- Total repository size
- File type distribution

### Language Analysis
- Files per language
- Lines of code per language
- Percentage breakdown
- Size per language

### Code Metrics
- Non-empty lines
- Comment detection
- Code-to-comment ratio (per file)

## 🌲 Directory Tree

Beautiful ASCII tree visualization:

```
my-project
├── src
│   ├── components
│   │   ├── Header.js
│   │   └── Footer.js
│   ├── utils
│   │   └── helpers.js
│   └── index.js
├── tests
│   └── test_app.py
├── package.json
└── README.md
```

## 🔧 What Gets Included

### ✅ Included Files

**Source Code:**
- All major programming languages (Python, JavaScript, Java, C++, Go, Rust, etc.)
- Web files (HTML, CSS, SCSS, Vue, React components)
- Configuration files (JSON, YAML, TOML, ENV)
- Documentation (Markdown, RST, AsciiDoc)
- Scripts (Shell, Bash, PowerShell, Batch)
- Database files (SQL, GraphQL, Prisma)
- Special files (Dockerfile, Makefile, LICENSE, README)

### ❌ Excluded Files

**Automatically Filtered:**
- Binary files (images, videos, executables, PDFs)
- Build artifacts (dist, build, target, bin, obj)
- Dependencies (node_modules, vendor, Pods)
- Version control (`.git` directory)
- IDE files (`.idea`, `.vscode`, `.vs`)
- Cache directories (`.cache`, `.pytest_cache`, `.coverage`)
- Temporary files (`.swp`, `.swo`, `.DS_Store`)
- Very large files (>10MB by default)

## 💡 Examples

### Example 1: Download and Process GitHub Repository

```bash
# Download repository as zip from GitHub
# (e.g., https://github.com/username/repo/archive/refs/heads/main.zip)

python git_zip_to_pdf.py repo-main.zip
```

Output:
```
repo-main_output_20231117_143022/
├── repository_content.pdf       # Professional PDF
├── repository_content.html      # Interactive HTML
├── repository_content.md        # Markdown docs
├── repository_content.txt       # Plain text
├── repository_stats.json        # JSON statistics
└── extracted/                   # Source files
    └── repo-main/
        └── (repository files)
```

### Example 2: Custom Configuration

Create `my-config.json`:
```json
{
  "max_lines_in_pdf": 2000,
  "font_size": 9,
  "page_size": "A4",
  "syntax_highlighting": true,
  "generate_html": true,
  "generate_markdown": false
}
```

Run:
```bash
python git_zip_to_pdf.py project.zip -c my-config.json -o docs
```

### Example 3: Quick PDF Only

```bash
python git_zip_to_pdf.py repo.zip --no-html --no-markdown -o quick-pdf
```

## 🎯 Use Cases

### 1. **Code Documentation**
Generate professional documentation for code review or archival

### 2. **Portfolio Presentation**
Create beautiful PDFs of your projects for presentations

### 3. **Code Sharing**
Share repository contents in a readable format without sending archives

### 4. **Offline Reference**
Keep offline copies of repositories in readable formats

### 5. **Code Analysis**
Get statistics and insights about repository composition

### 6. **Learning Resource**
Study codebases in well-formatted documents

### 7. **Backup Documentation**
Create timestamped backups with full statistics

## 📈 Performance

- **Fast Processing**: Optimized file reading and processing
- **Progress Tracking**: Real-time progress bars for large repositories
- **Memory Efficient**: Streams files instead of loading all at once
- **Smart Truncation**: Limits very large files automatically
- **Parallel-Ready**: Architecture supports future parallel processing

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'reportlab'"

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: "No syntax highlighting in HTML"

**Solution**: Install Pygments:
```bash
pip install Pygments
```

### Issue: "No progress bars showing"

**Solution**: Install tqdm:
```bash
pip install tqdm
```

### Issue: "Encoding errors when reading files"

**Solution**: The tool uses chardet for automatic encoding detection. Make sure it's installed:
```bash
pip install chardet
```

### Issue: "PDF generation fails with large files"

**Solution**: Use a configuration file to reduce `max_lines_in_pdf`:
```json
{
  "max_lines_in_pdf": 500
}
```

### Issue: "Repository too large / out of memory"

**Solution**:
- Reduce `max_file_size` in config
- Use `--no-html` to skip HTML generation
- Process smaller portions of the repository

## 🆚 Comparison with Basic Version

| Feature | Basic Version | Enhanced Version |
|---------|---------------|------------------|
| Output Formats | PDF, Text | PDF, HTML, Markdown, Text, JSON |
| Syntax Highlighting | ❌ | ✅ (HTML) |
| Statistics | Basic file count | Comprehensive analysis |
| Directory Tree | ❌ | ✅ |
| Progress Bars | ❌ | ✅ |
| Encoding Detection | Basic UTF-8 | Smart detection |
| File Type Support | ~20 | 100+ |
| Language Detection | Basic | 50+ languages |
| Configuration | ❌ | ✅ (JSON config) |
| PDF Quality | Basic | Professional tables & styling |
| HTML Output | ❌ | ✅ (Interactive) |
| Performance | Good | Optimized |

## 📝 Changelog

### Version 2.0 (Enhanced)
- ✨ Added HTML output with syntax highlighting
- ✨ Added Markdown export
- ✨ Added JSON statistics export
- ✨ Comprehensive repository statistics
- ✨ Directory tree visualization
- ✨ Progress bars for better UX
- ✨ Smart encoding detection
- ✨ Configuration file support
- ✨ 100+ file type support
- ✨ Professional PDF styling with tables
- ✨ Improved performance
- ✨ Better error handling
- 🐛 Fixed encoding issues
- 🐛 Fixed binary file detection
- 🐛 Fixed large file handling

### Version 1.0 (Basic)
- Initial release
- PDF and text generation
- Basic file filtering

## 🔐 Security

- The tool only reads files from the provided zip
- No network access required
- All processing is local
- Safe for processing private repositories

## 📄 License

This tool is provided as-is for personal, educational, and commercial use.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional output formats (EPUB, DocBook, etc.)
- More language support
- Better syntax highlighting in PDF
- Parallel processing for large repos
- GUI interface
- Cloud integration

## 🐛 Known Limitations

- PDF syntax highlighting is basic (monospace only)
- Very large files (>10MB) are skipped by default
- Binary files are excluded (images, videos, etc.)
- Some special characters may need escaping in PDF

## 💬 FAQ

**Q: Can I process private repositories?**
A: Yes! All processing is local. No data is sent anywhere.

**Q: What if my repository is very large?**
A: Use configuration to limit file sizes and line counts, or use `--no-html` to reduce memory usage.

**Q: Can I customize the PDF styling?**
A: Yes! The code is modular and easy to customize. Edit the style definitions in `git_zip_to_pdf.py`.

**Q: Does it work on Windows/Mac/Linux?**
A: Yes! Python is cross-platform and all dependencies support all major operating systems.

**Q: Can I use this for commercial projects?**
A: Yes! Feel free to use it for any purpose.

## 🙏 Acknowledgments

Built with:
- **ReportLab** for PDF generation
- **Pygments** for syntax highlighting
- **tqdm** for progress bars
- **chardet** for encoding detection

## 📞 Support

For issues, questions, or feature requests, please check the troubleshooting section above or review the code comments for detailed documentation.

---

**Made with ❤️ for developers who love beautiful documentation**
