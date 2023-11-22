import os
from glob import glob
from setuptools import setup

package_name = 'multi_wheel_control_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'),glob(os.path.join('launch','*launch.*'))),
        (os.path.join('share',package_name,'urdf'),glob(os.path.join('urdf/*'))),
        (os.path.join('share',package_name,'worlds'),glob(os.path.join('world/*'))),
        (os.path.join('share',package_name,'rviz'),glob(os.path.join('rviz/*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hirai',
    maintainer_email='hr28jwicpq302g@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'multi_motor_controller=multi_wheel_control_py.multi_wheel_control_drive:main',
        ],
    },
)
