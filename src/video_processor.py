#!/usr/bin/env python3
import cv2
import rospy
import numpy as np
from queue import Queue
from threading import Thread
from sensor_msgs.msg import Image

class VideoProcessor:
    def __init__(self):
        # Initialize the ROS node and subscriber
        rospy.init_node('video_processor')
        self.sub = rospy.Subscriber('webcam_video', Image, self.process_frame)

        # Create a queue to store the processed frames
        self.frame_queue = Queue()

        # Start a thread to encode the frames as JPEG images
        self.encoder_thread = Thread(target=self.frame_encoder)
        self.encoder_thread.start()

    def process_frame(self, msg):
        print("recieved frame")
        # Convert the ROS image message to a OpenCV image
        image_data = np.frombuffer(msg.data, np.uint8)
        frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        # Do any desired processing on the frame here...

        # Resize the frame to a smaller size (for faster transmission)
        frame = cv2.resize(frame, (640, 480))

        # Add the processed frame to the queue
        self.frame_queue.put(frame)

    def frame_encoder(self):
        # Continuously retrieve frames from the queue and encode them as JPEG images
        while True:
            # Get the next frame from the queue
            frame = self.frame_queue.get()

            # Encode the frame as a JPEG image
            jpeg_frame = cv2.imencode('.png', frame)[1].tobytes()
            jpeg_frame = np.array(jpeg_frame)
            print("encoded recieved frame")

            # Send the encoded frame to the HTTP server for display
            self.http_server.send_frame(jpeg_frame)

# if __name__ == '__main__':
#     processor = VideoProcessor()
#     rospy.spin()
