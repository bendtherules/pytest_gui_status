from setuptools import setup, find_packages

# packages = [
#     'pontoon',
#     'pontoon.cmd'
# ]
# packages=packages,
# package_dir={'pontoon': 'pontoon'},

setup(
    name='pytest_gui_status',
    version='0.0.1',
    description='Show pytest status in gui',
    author='Abhas Bhattacharya',
    author_email='abhasbhattacharya2@gmail.com',
    # url='http://github.com/joeyespo/pytest-watch',
    packages=["pytest_gui_status"],
    package_dir={'pytest_gui_status': 'pytest_gui_status'},
    license='MIT',
    platforms='any',
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        # 'pytest11': [
            # 'pytest_gui_status = pytest_gui_status.main',
        # ]
    },
)
