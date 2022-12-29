#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Initialize ROS node and publisher
rospy.init_node('webcam_publisher')
pub = rospy.Publisher('webcam_video', Image, queue_size=10)

# Open the webcam and start capturing frames
video_capture = cv2.VideoCapture(0)
bridge = CvBridge()

while not rospy.is_shutdown():
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    message = bridge.cv2_to_imgmsg(frame, encoding='passthrough')
    frame = cv2.resize(frame, (640, 480))

    # Convert the frame to a ROS image message
    image_message = Image()
    image_message.header.stamp = rospy.Time.now()
    image_message.data = cv2.imencode('.png', frame)[1].tobytes()

    # Publish the image message
    pub.publish(message)

# Release the webcam
video_capture.release()
