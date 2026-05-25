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
                '-x', '-0.0005',
                '-y', '3.5',
                '-z', '0.02',
                '-Y', '-1.5708'
            ],
            output='screen'
        )
    ])
