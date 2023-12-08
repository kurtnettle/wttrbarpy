from setuptools import find_packages, setup

print(find_packages())

setup(
    name="wttrbarpy",
    version="1.0.0",
    description="a highly customizable weather module for Waybar inspired by wttrbar",
    packages=['wttrbarpy'],
    include_package_data=True,
    entry_points={"console_scripts": ["wttrbarpy = wttrbarpy.__main__:main"]},
)
