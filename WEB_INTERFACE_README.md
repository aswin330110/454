# 🌐 Web Interface Guide

## Quick Start for Windows Users

1. **Double-click `START_WEB_INTERFACE.bat`**
   - The batch file will automatically install dependencies if needed
   - A command window will open showing the server status

2. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

3. **Upload your ZIP file**:
   - Drag and drop your repository ZIP file
   - OR click the upload area to browse

4. **Configure options** (optional):
   - Choose which output formats you want
   - Enable/disable statistics, syntax highlighting, etc.

5. **Click "Process Repository"**
   - Watch the real-time progress bar
   - Wait for processing to complete

6. **Download your files!**
   - View statistics and language breakdown
   - Download PDF, HTML, Markdown, Text, or JSON
   - View HTML directly in your browser

## For Mac/Linux Users

Run the shell script:
```bash
./start_web_interface.sh
```

Or run directly with Python:
```bash
python3 web_app.py
```

Then open `http://localhost:5000` in your browser.

## Features

### 📤 Drag & Drop Upload
- Modern, intuitive interface
- Drag and drop your ZIP files
- Or click to browse

### ⚡ Real-Time Progress
- Live progress bar showing current step
- Status messages during processing
- Estimated time remaining

### 📊 Beautiful Results Page
- Repository statistics dashboard
- Language breakdown with visual charts
- Download all generated files
- Preview HTML directly in browser

### ⚙️ Configurable Options
Choose what to generate:
- ✅ HTML with syntax highlighting
- ✅ Markdown documentation
- ✅ PDF with statistics
- ✅ Plain text version
- ✅ JSON statistics

Enable/disable features:
- 📊 Statistics analysis
- 🌲 Directory tree visualization
- 💻 Syntax highlighting
- 📈 Code metrics

### 🎨 Modern Design
- Gradient backgrounds
- Smooth animations
- Responsive layout
- Mobile-friendly

## How It Works

1. **Upload**: ZIP file is uploaded to server
2. **Extract**: Repository is extracted from ZIP
3. **Analyze**: Files are scanned and analyzed
4. **Generate**: Multiple output formats are created
5. **Download**: All files available for download

## Screenshots

### Home Page
Beautiful landing page with drag-and-drop upload:
- Modern gradient design
- Clear instructions
- Configuration options

### Processing
Real-time progress updates:
- Progress bar showing percentage
- Current step description
- Smooth animations

### Results
Comprehensive results page:
- Statistics cards showing key metrics
- Language breakdown table
- Download buttons for all formats
- Preview option for HTML

## Troubleshooting

### Port 5000 Already in Use

If you see an error about port 5000:

**Option 1**: Stop other applications using port 5000

**Option 2**: Edit `web_app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Use port 8080 instead
```

Then access at `http://localhost:8080`

### Cannot Access from Network

By default, the server is accessible only from your computer.

To allow access from other devices on your network:
- The server already listens on `0.0.0.0`
- Find your computer's IP address
- Access from other devices using `http://YOUR_IP:5000`

**Windows**: Run `ipconfig` to find your IP
**Mac/Linux**: Run `ifconfig` or `ip addr` to find your IP

### Upload Fails

If upload fails:
1. Check file is actually a ZIP file
2. Check file size (max 500MB)
3. Check disk space available
4. Try a smaller repository first

### Processing Errors

If processing fails:
1. Check the error message shown
2. Try with a different/smaller ZIP file
3. Check console/terminal for detailed errors
4. Make sure all dependencies are installed

## Advanced Configuration

### Change Upload Limits

Edit `web_app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
```

### Custom Output Directory

Edit `web_app.py`:
```python
app.config['OUTPUT_FOLDER'] = 'my_outputs'
```

### Add Authentication

For production use, add authentication:
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == 'admin' and password == 'secret':
        return username

@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')
```

## Security Notes

⚠️ **Important**: This web interface is designed for local use only!

For production deployment:
1. Add authentication
2. Add rate limiting
3. Add file upload validation
4. Use HTTPS
5. Set proper file size limits
6. Add virus scanning
7. Use a production WSGI server (not Flask's built-in server)

## File Cleanup

The web app automatically:
- Stores uploads in `uploads/` directory
- Creates outputs in `outputs/` directory
- Provides cleanup button on results page
- Auto-cleanup option when leaving page

To manually clean up:
- Delete contents of `uploads/` folder
- Delete contents of `outputs/` folder

## Technical Details

### Stack
- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Processing**: Multi-threaded background processing
- **Storage**: Local filesystem

### File Structure
```
.
├── web_app.py              # Flask application
├── templates/
│   ├── index.html          # Upload page
│   └── results.html        # Results page
├── uploads/                # Temporary upload storage
└── outputs/                # Generated outputs
```

### API Endpoints

- `GET /` - Main upload page
- `POST /upload` - Upload and start processing
- `GET /status/<job_id>` - Check processing status
- `GET /results/<job_id>` - View results page
- `GET /download/<job_id>/<filename>` - Download file
- `GET /view/<job_id>/<filename>` - View HTML in browser
- `POST /cleanup/<job_id>` - Clean up files

## Performance

- Handles repositories up to 500MB (configurable)
- Multi-threaded processing
- Real-time status updates
- Efficient memory usage
- Background processing doesn't block UI

## Support

For issues or questions:
1. Check this guide first
2. Check the main README.md
3. Look at console/terminal errors
4. Try with a simple test repository

## Tips

✅ **Best Practices**:
- Start with smaller repositories to test
- Close old result pages before processing new files
- Use cleanup button to free disk space
- Keep browser window open during processing

❌ **Avoid**:
- Don't upload multiple files simultaneously
- Don't close browser during processing
- Don't upload non-ZIP files
- Don't exceed 500MB file size

---

**Enjoy the web interface! 🚀**
