import fal_client
import  os
from flask import Flask, request, jsonify

app =Flask(__name__)

os.environ["FAL_KEY"] =""
def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
           print(log["message"])
@app.route('/generate_video', methods=['POST'])

def generate_video():
    try:
        # Extract the prompt from the POST request body
        data = request.get_json()
        prompt = data.get('prompt')
        duration = data.get('duration', 60)
        if not  prompt:
            return jsonify({'error': 'No prompt provided'})

        result = fal_client.subscribe(
            "fal-ai/ltx-video",

            arguments={

                "prompt": prompt,

                "duration": duration
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )

        def extract_url(data):

            if "video" in data and "url" in data["video"]:
                return data["video"]["url"]
            return None

        url = extract_url(result)
        return jsonify({"video_url":url})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ =="__main__":
    app.run(debug=True)
