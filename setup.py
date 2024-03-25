from setuptools import setup, find_packages

setup(
    name="pytweet-toolkit",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        'pillow>=10.2.0',
        'requests>=2.31.0',
    ],
)
