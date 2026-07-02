from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():
    urdf_file = PathJoinSubstitution([
        FindPackageShare('smorphi_description'),
        'urdf',
        'smorphi.urdf'
    ])

    return LaunchDescription([
        ExecuteProcess(
            cmd=[
                'ros2', 'run', 'ros_gz_sim', 'create',
                '-file', urdf_file,
                '-name', 'smorphi',
                '-x', '3.8000',
                '-y', '0.9000',
                '-z', '0.02',
                '-Y', '0'
            ],
            output='screen'
        )
    ])
