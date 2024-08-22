from setuptools import find_packages, setup

package_name = 'robots_nav_contr'

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
    maintainer='winicon',
    maintainer_email='winicon@live.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={

        'console_scripts': [
            "robots_nav_controller = robots_nav_contr.robotsnavcontroller:main", 
            "robot_command_receiver = robots_nav_contr.nav_commands_receiver:main",
            "robots_serial_commands = robots_nav_contr.raspberry_arduinoSerial:main",
            "redeye_commands = robots_nav_contr.redeye_nav_commands_receiver:main",
        ],
    },
)
