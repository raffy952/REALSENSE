import pyrealsense2 as rs
import numpy as np
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class Realsense_processing(Node):

    def __init__(self):
        super().__init__('realsense_processing')
        self.img_pub = self.create_publisher(Image,'/camera/depth/image_rect_raw',10)
        self.bridge = CvBridge()
        self.frequency = 1.0

        self.timer = self.create_timer(self.frequency, self.image_capturing)
        
        
    def image_capturing(self):
        pipeline = rs.pipeline()
        cfg = rs.config()

        #cfg.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
        cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)


        pipeline.start(cfg)

        while True:

            frame = pipeline.wait_for_frames()
            depth_frame = frame.get_depth_frame()
            #color_frame = frame.get_color_frame()

            depth_image = np.asanyarray(depth_frame.get_data())
            depth_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.5), cv2.COLORMAP_JET)
            #color_image = np.asanyarray(color_frame.get_data())
            #color_image= cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

            #cv2.imshow('depth', depth_image)
            #cv2.imshow('color', color_image)
            img_msg = self.bridge.cv2_to_imgmsg(depth_image)
            img_msg.header.stamp = self.get_clock().now().to_msg()
            img_msg.encoding = 'bgr8'

            self.img_pub.publish(img_msg)
            self.get_logger().info("Image published")



            if cv2.waitKey(1) == ord('q'):
                break

        pipeline.stop()

def main(args=None):
    rclpy.init(args=args)
    img = Realsense_processing()
    rclpy.spin(img)
    img.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()



