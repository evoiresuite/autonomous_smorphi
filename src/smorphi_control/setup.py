from setuptools import find_packages, setup
package_name = 'smorphi_control'
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alicia',
    maintainer_email='alicia@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'obstacle_avoidance = smorphi_control.obstacle_avoidance:main',
            'line_following = smorphi_control.line_following:main',
            'decision_node = smorphi_control.decision_node:main',
            'line_node = smorphi_control.line_node:main',
            'obstacle_node = smorphi_control.obstacle_node:main',
            'smorphi_driver_node = smorphi_control.smorphi_driver_node:main',
        ],
    },
)
