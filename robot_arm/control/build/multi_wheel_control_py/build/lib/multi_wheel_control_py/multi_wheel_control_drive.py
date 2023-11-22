#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from sensor_msgs.msg import JointState
import math

class MultiMotorController(Node):

    def __init__(self):
        super().__init__('multi_motor_controller')
        self.joint_state_publisher=self.create_publisher(
                JointState,
                '/joint_states',
                10
        )
        self.twist_subscription=self.create_subscription(
                Twist,
                'cmd_vel',
                self.twist_callback,
                10
        )
        self.integral=0.0
        self.previous_error=0.0

    def twist_callback(self,msg):
        #Twistメッセージからモータの電流制御に変換する処理を実装した。
        left_motor_id = 1
        right_motor_id = 2
        left_angular_vel = get_multi_motor_angular_vel(left_motor_id)
        right_angular_vel = get_multi_motor_angular_vel(right_morot_id)

        left_motor_current = pid_control(left_angular_vel,left_motor_id)
        right_motor_current = pid_control(right_angular_vel,right_motor_id)
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = self.get_clock().now().to_msg()
        joint_state_msg.name = ["joint1", "joint2"]  # これに合わせてロボットのジョイント名を指定
        joint_state_msg.position = [0.0, 0.0]  # ジョイントの位置を適切に設定
        joint_state_msg.velocity = [msg.linear.x, msg.angular.z]  # ジョイントの速度をcmd_velから取得
        self.joint_state_publisher.publish(joint_state_msg)
        
    def pid_control(self,angular_vel,motor_id):
        # PID制御のパラメータ
        Kp = 1.0
        Ki = 0.0
        Kd = 0.0

        # エンコーダの分解能
        n = 4196

        # 目標角速度
        target_angular_vel = 10.0

        # エンコーダの値から現在の角速度を計算する
        current_angular_vel = get_motor_angular_vel(motor_id)

        # PID制御によってモーターの電流を決定する
        error = target_angular_vel - current_angular_vel
        integral = integral + error
        derivative = error - previous_error
        motor_current = Kp * error + Ki * integral + Kd * derivative

        # 前回のエラーを更新する
        previous_error = error

        return motor_current

    def get_motor_angular_vel(self,motor_id):
    # エンコーダの分解能
        n = 4196

    # エンコーダの値を読み取る
        # encoder_value = read_encoder_value(motor_id)
        encode_value = 1.0
    # エンコーダの値から現在の角速度を計算する
        angular_vel = (encoder_value / n) * 2.0 * math.pi

        return angular_vel
    

def main(args =None):
    rclpy.init(args=args)
    node=MultiMotorController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
