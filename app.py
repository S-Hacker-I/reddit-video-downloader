from flask import Flask, request, send_file, jsonify, send_from_directory
import os
import yt_dlp

app = Flask(__name__, static_folder='public')

# Directory to save downloaded videos
DOWNLOAD_DIR = 'downloads'

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/download', methods=['POST'])
def download_video():
    # Extract video URL from JSON payload
    data = request.json
    video_url = data.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    # Ensure the download directory exists
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Clear old files from the download directory
    for file in os.listdir(DOWNLOAD_DIR):
        file_path = os.path.join(DOWNLOAD_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Download the video
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),  # Output file path
        'format': 'bestvideo+bestaudio/best',  # Best quality video and audio
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Check if any files are in the directory
        filenames = os.listdir(DOWNLOAD_DIR)
        if not filenames:
            return jsonify({'error': 'No files were downloaded'}), 500

        filename = filenames[0]  # Get the first file in the directory
        file_path = os.path.join(DOWNLOAD_DIR, filename)

        return send_file(file_path, as_attachment=True, download_name=filename)
    
    except Exception as e:
        app.logger.error(f"Failed to download or convert video: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
