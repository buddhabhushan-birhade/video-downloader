import os
import threading
import yt_dlp
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# Configure download folder (local to the app)
DOWNLOAD_FOLDER = os.path.join(app.root_path, "downloads")
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Global dictionary to store progress
download_status = {
    'progress': '0',
    'speed': 'N/A',
    'eta': 'N/A',
    'status': 'idle',
    'error': None,
    'filename': None
}

def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%', '').strip()
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        download_status['progress'] = p
        download_status['speed'] = speed
        download_status['eta'] = eta
    elif d['status'] == 'finished':
        download_status['progress'] = '100'
        download_status['status'] = 'finished'
        # Get the final filename from the path
        filename = os.path.basename(d.get('info_dict', {}).get('_filename', 'video.mp4'))
        download_status['filename'] = filename

def run_download(url):
    download_status['status'] = 'downloading'
    download_status['error'] = None
    download_status['filename'] = None
    
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # We need to extract info to get the filename accurately if hook fails to provide it cleanly
            info = ydl.extract_info(url, download=True)
            download_status['filename'] = os.path.basename(info.get('_filename', 'video.mp4'))
    except Exception as e:
        download_status['error'] = str(e)
        download_status['status'] = 'error'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/progress')
def progress():
    def generate():
        while True:
            import time
            status = download_status.get('status')
            p_val = download_status.get('progress', '0')
            error = download_status.get('error')
            filename = download_status.get('filename')
            
            data = {
                "progress": p_val,
                "speed": download_status.get('speed', 'N/A'),
                "eta": download_status.get('eta', 'N/A'),
                "status": status,
                "error": error,
                "filename": filename
            }
            
            import json
            yield f"data: {json.dumps(data)}\n\n"
            
            if status in ['finished', 'error'] and p_val == '100':
                break
            if status == 'error':
                break
                
            time.sleep(0.5)
    return app.response_class(generate(), mimetype='text/event-stream')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Reset status
    download_status['progress'] = '0'
    download_status['status'] = 'starting'
    download_status['error'] = None
    download_status['filename'] = None

    # Link verification
    try:
        ydl_opts_check = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts_check) as ydl:
            ydl.extract_info(url, download=False)
    except Exception as e:
        error_msg = str(e)
        if "Unsupported URL" in error_msg or "not a valid URL" in error_msg:
            return jsonify({'error': 'Illegal website source or invalid URL provided.'}), 400
        return jsonify({'error': f'Link verification failed: {error_msg}'}), 400

    # Start download thread
    thread = threading.Thread(target=run_download, args=(url,))
    thread.daemon = True
    thread.start()
            
    return jsonify({
        'success': True, 
        'message': 'Download started...'
    })

@app.route('/get-video/<path:filename>')
def get_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
