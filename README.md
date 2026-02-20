# Video Downloader

A web-based video downloader application built with Flask and yt-dlp. This application allows users to download videos from various supported platforms (YouTube, Vimeo, etc.) with a clean, modern web interface and real-time progress tracking.

## Features

- **Web Interface**: Clean, responsive UI with progress tracking
- **Real-time Progress**: Live updates on download progress, speed, and ETA
- **Multiple Formats**: Downloads in best available quality
- **Error Handling**: Comprehensive error messages and validation
- **CLI Version**: Command-line interface for direct downloads
- **Heroku Ready**: Configured for easy deployment

## Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

1. Clone or download this repository
2. Navigate to the project directory
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Application

1. Run the Flask app:
   ```bash
   python app.py
   ```
2. Open your browser and go to `http://localhost:5000`
3. Paste a video URL in the input field
4. Click "Download" to start the download
5. Monitor progress in real-time
6. Once complete, download the video file

### Command Line Interface

Run the CLI version:
```bash
python dowmload.py
```
Follow the prompts to enter the video URL.

## Deployment

### Heroku

This project is configured for Heroku deployment:

1. Create a Heroku app
2. Push your code to Heroku
3. The `Procfile` and `requirements.txt` are already configured

## Supported Platforms

This application uses yt-dlp, which supports downloading from:
- YouTube
- Vimeo
- Dailymotion
- And many more (see yt-dlp documentation for full list)

## Project Structure

```
video downloader/
├── app.py                 # Main Flask application
├── dowmload.py           # CLI version (note: filename has typo)
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment configuration
├── templates/
│   └── index.html        # Web interface template
├── static/
│   └── style.css         # CSS styles
└── downloads/            # Downloaded videos (created automatically)
```

## Dependencies

- Flask: Web framework
- yt-dlp: Video downloading library
- gunicorn: WSGI server for production

## Disclaimer

This application is for educational purposes only. Users are responsible for ensuring they have the right to download and use any content. Downloading copyrighted material without permission may violate copyright laws. The developers are not responsible for any misuse of this software.

## License

MIT License - see LICENSE file for details (if applicable)
