from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"status": "error", "message": "Please provide a video URL"}), 400
        
    try:
        # Format ගැටලුව 100%ක් විසඳන සකස් කළ Settings
        ydl_opts = {
            # වීඩියෝ සහ ඕඩියෝ දෙකම අඩංගු හොඳම තනි Format එක (mp4) ස්වයංක්‍රීයව තෝරාගැනීම
            'format': 'best[ext=mp4]/best', 
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        if os.path.exists('cookies.txt'):
            ydl_opts['cookiefile'] = 'cookies.txt'
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # සෘජු බාගත කිරීමේ ලින්ක් එක ලබාගැනීම
            direct_link = info.get('url')
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail', '')
            
            # සෘජු ලින්ක් එකක් නොමැති නම් ඇති විය හැකි දෝෂ මඟහැරීම
            if not direct_link:
                # සමහර වෙලාවට formats ලැයිස්තුවේ අන්තිම එකෙන් URL එක ගැනීම
                formats = info.get('formats', [])
                for f in reversed(formats):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        direct_link = f.get('url')
                        break
            
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
