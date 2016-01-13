from setuptools import setup

packages = [
    "pytest_gui_status",
    # 'pytest_gui_status.plugin',
    # 'pytest_gui_status.gui',
]
package_dir = {
    'pytest_gui_status': 'pytest_gui_status',
    # 'pytest_gui_status.plugin': 'status_plugin',
    # 'pytest_gui_status.gui': 'status_gui',
}

setup(
    name='pytest_gui_status',
    version='0.0.3',
    description='Show pytest status in gui',
    author='Abhas Bhattacharya',
    author_email='abhasbhattacharya2@gmail.com',
    # url='http://github.com/joeyespo/pytest-watch',
    packages=packages,
    package_dir=package_dir,
    license='MIT',
    platforms='any',
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        'pytest11': [
            'pytest_gui_status = pytest_gui_status.status_plugin.plugin',
        ],
        'console_scripts': [
            'pytest_gui_status = pytest_gui_status.status_gui.gui_frontend:main',
        ]
    },
)
