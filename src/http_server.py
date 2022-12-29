#!/usr/bin/env python3
import os
from flask import Flask, render_template, Response
from video_processor import VideoProcessor

app = Flask(__name__)

# Create an instance of the VideoProcessor class
video_processor = VideoProcessor()

@app.route('/')
def index():
    # Render the HTML page with the video stream
    return render_template(
        os.path.join(
            os.path.dirname(__file__),
            'index.html'
        )
    )

@app.route('/video_feed')
def video_feed():
    # Get the next frame from the video processor
    frame = video_processor.frame_queue.get()

    # Serve the frame as a JPEG image
    return Response(frame, mimetype='image/png')

if __name__ == '__main__':
    app.run(port=5000)
