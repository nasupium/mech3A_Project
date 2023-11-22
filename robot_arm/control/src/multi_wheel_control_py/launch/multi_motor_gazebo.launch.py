# 例: multi_motor_gazebo.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch_ros.parameter_descriptions import ParameterValue
def generate_launch_description():
    
    package_dir = get_package_share_directory("multi_wheel_control_py")
    default_model_path = os.path.join(package_dir,"urdf","multi_wheel_control.urdf")
    default_rviz_config_path=os.path.join(package_dir,"rviz","urdf.rviz")
    world_file_path=os.path.join(package_dir,"worlds","basic.world")
    use_sim_time=LaunchConfiguration('use_sim_time',default='true')
    # 起動引数の宣言と追加
    gui_arg = DeclareLaunchArgument(name='gui', default_value='true', choices=['true', 'false'],
                                    description='Flag to enable joint_state_publisher_gui')
    #ld.add_action(gui_arg)
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                     description='Absolute path to rviz config file')
    #ld.add_action(rviz_arg)
    
    # 起動引数の追加
    model_arg = DeclareLaunchArgument(name='model', default_value=[str(default_model_path)],
                                       description='Path to robot urdf file relative to urdf_tutorial package')
    

    return LaunchDescription([
        model_arg,
        gui_arg,
        rviz_arg,
    # ROS 2ノードの起動 
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            #parameters = [{'robot_description': robot_description}],
            arguments=[default_model_path],
            output='screen'
            ),
 
    #ld.add_action(robot_state_publisher)
 
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            #parameters=[{'source_list':[default_model_path]}],
            arguments=[default_model_path],
            output='screen',
            ),
    #ld.add_action(joint_state_publisher)
    
    # RVizの起動ノードの追加
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', default_rviz_config_path],
            ),
    

    # Gazeboの起動
    #    Node(
    #       package='gazebo_ros',
    #       executable='/usr/bin/gazebo',
    #       name='gazebo_ros_factory',
    #       output='screen',
    #       arguments=[
    #           '--verbose', '-s', 'libgazebo_ros_factory.so'
    #       ],
    #       ),
    # ld.add_action(gazebo_ros_factory)
    
        ExecuteProcess(
            cmd=['gazebo','--verbose','-s','libgazebo_ros_factory.so'],
            ),
    # ld.add_action(gazebo)
    
    # ROS 2ノードの起動
    #multi_motor_controller = Node(
    #    package='multi_wheel_control_py',
    #    executable='multi_motor_controller',
    #    name='multi_motor_controller',
    #    output='screen',
    #   remappings=[('/joint_states', '/robot/joint_states')]
    #)
    #ld.add_action(multi_motor_controller)

    # URDFモデルのスポーン
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='urdf_spawner',
            output='screen',
            parameters=[{'use_sim_time':use_sim_time}],
            arguments=[
                "-entity" , "multi_wheel_control_robot", "-file" , default_model_path,
            ],
            ),
    #ld.add_action(spawn_entity)
    
    #return ld
    ])
