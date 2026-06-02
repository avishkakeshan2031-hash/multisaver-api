from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # ඔබේ WordPress සයිට් එකෙන් එන ඉල්ලීම් (Requests) බ්ලොක් නොවීම සඳහා

@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"status": "error", "message": "Please provide a video URL"}), 400
        
    try:
        # yt-dlp සඳහා අවශ්‍ය Settings සකස් කිරීම
        ydl_opts = {
            'format': 'best',  # හොඳම Quality එක තෝරාගැනීම
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # වීඩියো එක බාගත කරන්නේ නැතුව එහි තොරතුරු (Metadata) පමණක් ලබාගැනීම
            info = ydl.extract_info(video_url, download=False)
            
            # සෘජු බාගත කිරීමේ ලින්ක් එක (Direct Video URL) ලබාගැනීම
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