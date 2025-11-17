#!/usr/bin/env python3
"""
Web Interface for Advanced Git Zip Extractor
A Flask-based web application for easy repository processing
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
import json
import threading
import uuid

from git_zip_to_pdf import AdvancedGitZipExtractor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'git-zip-extractor-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Ensure folders exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

# Store processing status
processing_status = {}


def allowed_file(filename):
    """Check if file is a zip file."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'


def process_zip_file(job_id, zip_path, output_dir, config):
    """Process zip file in background thread."""
    try:
        processing_status[job_id] = {
            'status': 'processing',
            'progress': 0,
            'message': 'Starting extraction...',
            'error': None
        }

        # Create extractor
        extractor = AdvancedGitZipExtractor(
            zip_path=zip_path,
            output_dir=output_dir
        )

        # Apply config
        if config:
            extractor.config.update(config)

        # Extract
        processing_status[job_id]['progress'] = 20
        processing_status[job_id]['message'] = 'Extracting repository...'
        extractor.extract_zip()

        # Collect files
        processing_status[job_id]['progress'] = 40
        processing_status[job_id]['message'] = 'Analyzing files...'
        files_data = extractor.collect_files()

        if not files_data:
            processing_status[job_id] = {
                'status': 'error',
                'progress': 0,
                'message': 'No files found to process',
                'error': 'No processable files found in the repository'
            }
            return

        # Generate outputs
        processing_status[job_id]['progress'] = 50
        processing_status[job_id]['message'] = 'Generating text file...'
        extractor.generate_text_file(files_data)

        processing_status[job_id]['progress'] = 60
        processing_status[job_id]['message'] = 'Generating HTML...'
        if extractor.config.get('generate_html', True):
            extractor.generate_html(files_data)

        processing_status[job_id]['progress'] = 70
        processing_status[job_id]['message'] = 'Generating Markdown...'
        if extractor.config.get('generate_markdown', True):
            extractor.generate_markdown(files_data)

        processing_status[job_id]['progress'] = 80
        processing_status[job_id]['message'] = 'Generating PDF...'
        extractor.generate_pdf(files_data)

        processing_status[job_id]['progress'] = 90
        processing_status[job_id]['message'] = 'Saving statistics...'
        extractor.save_stats_json()

        # Get stats
        stats = extractor.repo_stats.get_summary()

        processing_status[job_id] = {
            'status': 'completed',
            'progress': 100,
            'message': 'Processing complete!',
            'error': None,
            'output_dir': str(Path(output_dir).name),
            'stats': {
                'total_files': stats['total_files'],
                'total_lines': stats['total_lines'],
                'total_size': extractor.format_size(stats['total_size']),
                'languages': stats['languages']
            },
            'files': {
                'pdf': 'repository_content.pdf',
                'html': 'repository_content.html',
                'markdown': 'repository_content.md',
                'text': 'repository_content.txt',
                'json': 'repository_stats.json'
            }
        }

    except Exception as e:
        processing_status[job_id] = {
            'status': 'error',
            'progress': 0,
            'message': 'Processing failed',
            'error': str(e)
        }


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and start processing."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only ZIP files are allowed'}), 400

    try:
        # Generate unique job ID
        job_id = str(uuid.uuid4())

        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        upload_path = Path(app.config['UPLOAD_FOLDER']) / f"{timestamp}_{filename}"
        file.save(str(upload_path))

        # Create output directory
        output_dir = Path(app.config['OUTPUT_FOLDER']) / f"output_{timestamp}_{job_id[:8]}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Get configuration from request
        config = {}
        if request.form.get('config'):
            try:
                config = json.loads(request.form.get('config'))
            except:
                pass

        # Start processing in background
        thread = threading.Thread(
            target=process_zip_file,
            args=(job_id, str(upload_path), str(output_dir), config)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'job_id': job_id,
            'message': 'Processing started'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/status/<job_id>')
def get_status(job_id):
    """Get processing status."""
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404

    return jsonify(processing_status[job_id])


@app.route('/download/<job_id>/<filename>')
def download_file(job_id, filename):
    """Download generated file."""
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404

    status = processing_status[job_id]

    if status['status'] != 'completed':
        return jsonify({'error': 'Processing not completed'}), 400

    output_dir = Path(app.config['OUTPUT_FOLDER']) / status['output_dir']
    file_path = output_dir / filename

    if not file_path.exists():
        return jsonify({'error': 'File not found'}), 404

    return send_file(
        str(file_path),
        as_attachment=True,
        download_name=filename
    )


@app.route('/view/<job_id>/<filename>')
def view_file(job_id, filename):
    """View generated HTML file in browser."""
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404

    status = processing_status[job_id]

    if status['status'] != 'completed':
        return jsonify({'error': 'Processing not completed'}), 400

    output_dir = Path(app.config['OUTPUT_FOLDER']) / status['output_dir']
    file_path = output_dir / filename

    if not file_path.exists():
        return jsonify({'error': 'File not found'}), 404

    if filename.endswith('.html'):
        return send_file(str(file_path))
    else:
        return send_file(str(file_path), as_attachment=True)


@app.route('/results/<job_id>')
def results(job_id):
    """Show results page."""
    if job_id not in processing_status:
        return "Job not found", 404

    status = processing_status[job_id]

    if status['status'] != 'completed':
        return render_template('processing.html', job_id=job_id)

    return render_template('results.html', job_id=job_id, status=status)


@app.route('/cleanup/<job_id>', methods=['POST'])
def cleanup(job_id):
    """Clean up processed files."""
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404

    try:
        status = processing_status[job_id]

        if 'output_dir' in status:
            output_dir = Path(app.config['OUTPUT_FOLDER']) / status['output_dir']
            if output_dir.exists():
                shutil.rmtree(output_dir)

        # Remove from status
        del processing_status[job_id]

        return jsonify({'message': 'Cleanup successful'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("ADVANCED GIT ZIP EXTRACTOR - WEB INTERFACE")
    print("=" * 80)
    print("\nStarting web server...")
    print("\n📱 Open your browser and go to:")
    print("\n   http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
