from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    try:
        video_url = request.form["video_url"]
        save_path = request.form["save_path"]
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        ydl_opts = {
            "outtmpl": f"{save_path}/%(title)s.%(ext)s",
            "format": "best",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_file = ydl.prepare_filename(info_dict)
        
        return send_file(video_file, as_attachment=True)
    except Exception as e:
        return render_template("index.html", message=f"Error: {str(e)}", message_type="red")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
