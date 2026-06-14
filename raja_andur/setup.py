from setuptools import setup

package_name = 'raja_andur'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='student@tktk.ee',
    description='Raja andurite lugemine lidariga',
    license='MIT',
    entry_points={
        'console_scripts': [
            'raja_andur = raja_andur.raja_andur:main',
        ],
    },
)
