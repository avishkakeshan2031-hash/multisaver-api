from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"status": "error", "message": "Please provide a video URL"}), 400
        
    try:
        # YouTube Bot Block එක මඟහැරීමට අවශ්‍ය ප්‍රධාන Settings
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            # YouTube එක සර්වර් එකක් වෙනුවට සාමාන්‍ය Android/iOS App එකක් ලෙස හැඟවීමට:
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'web'],
                    'skip': ['dash', 'hls']
                }
            },
            # Fake Browser Headers එකතු කිරීම
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_link = info.get('url')
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail', '')
            
            return jsonify({
                "status": "success",
                "title": title,
                "thumbnail": thumbnail,
                "download_url": direct_link
            })
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
