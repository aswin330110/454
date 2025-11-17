# 🚀 Quick Start Guide for Windows

## Super Easy - 3 Steps!

### Step 1: Install Python (if not already installed)

1. Download Python from https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Click "Install Now"

### Step 2: Download this Repository

1. Download the repository as ZIP from GitHub
2. Extract it to a folder (e.g., `C:\git-zip-extractor`)
3. Navigate to that folder

### Step 3: Start the Web Interface

**Double-click `START_WEB_INTERFACE.bat`**

That's it! Your browser will show the tool at `http://localhost:5000`

---

## Using the Tool

### 1. Get a Repository ZIP File

**From GitHub:**
1. Go to any GitHub repository
2. Click the green "Code" button
3. Click "Download ZIP"
4. Save it somewhere

**Example repositories to try:**
- https://github.com/django/django (large Python project)
- https://github.com/facebook/react (JavaScript library)
- Any of your own repositories!

### 2. Upload to the Tool

1. Open `http://localhost:5000` in your browser
2. **Drag and drop** your ZIP file onto the upload area
   - OR click the upload area to browse for the file

3. The file will appear below with its name and size

### 3. Configure Options (Optional)

Choose what you want:
- ✅ **Generate HTML** - Interactive web page with syntax highlighting
- ✅ **Generate Markdown** - GitHub-style documentation
- ✅ **Include Statistics** - File counts, languages, sizes
- ✅ **Directory Tree** - Visual folder structure
- ✅ **Syntax Highlighting** - Colorful code in HTML

**Tip**: Leave everything checked for the full experience!

### 4. Process the Repository

1. Click the big **"🎯 Process Repository"** button
2. Watch the progress bar
3. Wait for it to complete (usually 10-60 seconds)

### 5. Download Your Files

You'll see a results page with:

**Statistics:**
- Total files
- Total lines of code
- Total size
- Language breakdown

**Download Options:**
- 📄 **PDF** - Professional document for sharing
- 🌐 **HTML** - Click "View HTML" to see it in your browser!
- 📝 **Markdown** - For GitHub or documentation
- 📋 **Text** - Simple plain text version
- 📊 **JSON** - Statistics in JSON format

### 6. Done!

Click "Process Another Repository" to do more, or close the browser when done.

---

## Tips for Best Results

### ✅ DO:
- Start with smaller repositories (< 100MB) to test
- Try the HTML output first - it's beautiful!
- Use the "View HTML" button to see syntax highlighting
- Check the statistics to understand your code
- Download multiple formats for different uses

### ❌ DON'T:
- Upload files larger than 500MB (it will fail)
- Upload non-ZIP files
- Close the browser while processing
- Process multiple files at once

---

## What You Get

### PDF Output
- Professional-looking document
- Table of contents
- Statistics tables
- Formatted code
- Perfect for:
  - Sharing with team members
  - Printing
  - Archiving
  - Code reviews

### HTML Output (★ BEST!)
- Beautiful modern design
- Color-coded syntax highlighting
- Smooth navigation
- Interactive tables
- Perfect for:
  - Viewing in browser
  - Sharing via web
  - Online documentation
  - Code presentations

### Markdown Output
- GitHub-compatible format
- Code blocks with syntax
- Clean formatting
- Perfect for:
  - GitHub/GitLab wikis
  - README files
  - Online documentation
  - Version control

### Text Output
- Plain text format
- Works everywhere
- No formatting needed
- Perfect for:
  - Email sharing
  - Plain text editors
  - Quick reference
  - Grep/search

### JSON Stats
- Machine-readable data
- All statistics
- Language breakdown
- Perfect for:
  - Automation
  - Data analysis
  - Custom scripts
  - Metrics tracking

---

## Troubleshooting

### "Python is not installed"
1. Download from https://www.python.org/downloads/
2. Install with "Add to PATH" checked
3. Restart the batch file

### "Port 5000 is already in use"
1. Close other applications using port 5000
2. Or edit `web_app.py` and change `port=5000` to `port=8080`
3. Then use `http://localhost:8080`

### "Upload failed"
- Make sure it's a ZIP file (not RAR, 7Z, etc.)
- Check file size (must be under 500MB)
- Try a smaller repository first

### "Processing failed"
- Check the error message
- Try a different/smaller repository
- Make sure you have disk space
- Check the console window for details

### Page won't load
- Make sure the batch file is still running
- Try closing and reopening your browser
- Try `http://127.0.0.1:5000` instead

---

## Command Line Alternative

If you prefer command line:

```cmd
python git_zip_to_pdf.py my-repository.zip
```

This creates an output folder with all files.

---

## Need Help?

1. Check [WEB_INTERFACE_README.md](WEB_INTERFACE_README.md) for detailed info
2. Check [README.md](README.md) for full documentation
3. Look at the console window for error messages

---

## Example Workflow

**Let's process a React repository:**

1. ✅ Go to https://github.com/facebook/react
2. ✅ Click "Code" → "Download ZIP"
3. ✅ Save to Downloads folder
4. ✅ Double-click `START_WEB_INTERFACE.bat`
5. ✅ Open `http://localhost:5000`
6. ✅ Drag `react-main.zip` to upload area
7. ✅ Click "Process Repository"
8. ✅ Wait ~30 seconds
9. ✅ Click "View HTML" to see beautiful syntax-highlighted code!
10. ✅ Download PDF for your team

**That's it! You now have beautiful documentation of React's source code!**

---

**Happy documenting! 🎉**

If you found this useful, star the repository on GitHub!
