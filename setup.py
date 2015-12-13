from setuptools import setup

packages = [
    'plugin',
    'gui',
]
# packages=packages,
package_dir = {
    'plugin': 'status_plugin',
    'gui': 'status_gui',
},

setup(
    name='pytest_gui_status',
    version='0.0.1',
    description='Show pytest status in gui',
    author='Abhas Bhattacharya',
    author_email='abhasbhattacharya2@gmail.com',
    # url='http://github.com/joeyespo/pytest-watch',
    packages=packages,
    package_dir=package_dir,
    license='MIT',
    platforms='any',
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        # 'pytest11': [
            # 'pytest_gui_status = pytest_gui_status.main',
        # ]
    },
)
