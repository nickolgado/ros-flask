# coding:utf-8
import sys
import traceback

import cv2
import numpy as np
import rospy
import sensor_msgs.msg
import kivy
from cv_bridge import CvBridge, CvBridgeError
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as kvImage
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from sensor_msgs.msg import Image as senImage
from kivy.graphics import *
from kivy.properties import NumericProperty, ObjectProperty

# print(dir(kivy))
# print(kivy.Modules.list())

class KivyCamera(Widget):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.newtexture = ObjectProperty(2)

        self.bridge = CvBridge()

        self.new_shape_x = 0
        self.new_shape_y = 0
        self.img = bytes()

        # # create a 64x64 texture, defaults to rgba / ubyte
        # texture = Texture.create(size=(640, 480))
        # texture.blit_buffer(bytes([int(x / 255) % 255 for x in range((640*480*3))]), colorfmt='rgb')
        # with self.canvas:
        #     Rectangle(texture=texture, size_hint=(1,1), size=(640, 480))

        clk = Clock.schedule_interval(self.update_texture, 0.25)
        # clk.start()

    def update(self, msg):
        print("new msg ")
        try:
            cv2_img = self.bridge.imgmsg_to_cv2(img_msg=msg, desired_encoding='passthrough')

            new_img = cv2_img
            self.new_shape_x = np.shape(cv2_img)[1]
            self.new_shape_y = np.shape(cv2_img)[0]
            # img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            # print(np.shape(img))
            
            self.img = cv2.flip(new_img, 0).tobytes()

        except Exception as e:
            print(traceback.format_exc())
            # print(sys.exc_info()[2])
            print(f"ERROR: \n{Exception}\n{e}")

    def update_texture(self, dt):
        print("new texture")
        try:
            camera_texture = Texture.create(size=(self.new_shape_x, self.new_shape_y))
            camera_texture.blit_buffer(self.img, colorfmt='rgb')

            with self.canvas:
                Rectangle(texture = camera_texture, size = (640, 480))
        except Exception as e:
            print(traceback.format_exc())
            # print(sys.exc_info()[2])
            print(f"ERROR: \n{Exception}\n{e}")

class CamApp(App):
    def build(self):
        # self.content = BoxLayout(orientation = 'vertical', size_hint = (1,1))

        self.my_camera = KivyCamera(size_hint=(1,1))

        # self.content.add_widget(self.my_camera)
        return self.my_camera

if __name__ == '__main__':
    # Window.size = (700, 700)
    app = CamApp()
    app.build()
    print("setting up ros")
    rospy.init_node("kivy_cam")
    rospy.Subscriber('/webcam_video', senImage, app.my_camera.update)
    print('running gui')
    app.run()
