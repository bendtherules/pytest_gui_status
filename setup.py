from setuptools import setup

packages = [
    "pytest_gui_status",
    "pytest_gui_status.status_plugin",
    "pytest_gui_status.status_gui",
]
package_dir = {
    "pytest_gui_status": "pytest_gui_status",
    # "pytest_gui_status.status_plugin": "status_plugin",
    # "pytest_gui_status.status_gui": "status_gui",
}
package_data = {
    "pytest_gui_status.status_gui": ["tmpl/*"]
}

setup(
    name="pytest_gui_status",
    version="0.0.3",
    description="Show pytest status in gui",
    author="Abhas Bhattacharya",
    author_email="abhasbhattacharya2@gmail.com",
    # url="http://github.com/joeyespo/pytest-watch",
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    license="MIT",
    platforms="any",
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        "pytest11": [
            "pytest_gui_status = pytest_gui_status.status_plugin.plugin",
        ],
        "console_scripts": [
            "pytest_gui_status = pytest_gui_status.status_gui.gui_frontend:main",
        ]
    },
)
