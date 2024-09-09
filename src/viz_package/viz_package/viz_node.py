import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
import serial
import random

def read_sensor_value():
    serial_port = '/dev/ttyACM0'
    connection = serial.Serial(serial_port, 9600)




    while True:
        raw_data = connection.readline()
        # Decodificar los bytes leídos a una cadena UTF-8 y eliminar espacios en blanco
        decoded_data = raw_data.decode("utf-8", "ignore").strip()

        try:
            sensor_value = float(decoded_data)/10
            return sensor_value

        except ValueError:
            print("Error: Could not convert to float")
            continue
    # Cerrar la conexión serial
    connection.close()

class MarkerPublisher(Node):
    def __init__(self):
        super().__init__('marker_publisher')
        self.publisher_ = self.create_publisher(Marker, 'marker_topic', 10)
        timer_period = 1 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        marker = Marker()

        marker.header.frame_id = "/base_link"
        marker.header.stamp = self.get_clock().now().to_msg()

        # set shape, Arrow: 0; Cube: 1; Sphere: 2; Cylinder: 3
        marker.type = 1
        marker.id = 0
        # Set the scale of the marker
        marker.scale.x = 1.0
        marker.scale.y = 1.0
        marker.scale.z = 1.0

        # Set the color
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 0.5

        marker.lifetime.sec = 1

        # Set the pose of the marker
        marker.pose.position.x = read_sensor_value()
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.0
        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0

        self.publisher_.publish(marker)

def main(args=None):
    print('Hi from voz package.')

    rclpy.init(args=args)
    marker_publisher = MarkerPublisher()
    rclpy.spin(marker_publisher)

    # Destroy the node explicitly
    marker_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
