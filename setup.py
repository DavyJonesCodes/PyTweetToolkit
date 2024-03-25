from setuptools import setup, find_packages

setup(
    name="pytweet-toolkit",
    version="1.0.0",
    author='Dev Jones',
    description='PyTweetToolkit: An intuitive Python library for managing Twitter interactions, providing tools for posting tweets, engaging with users, and analyzing social media metrics. Perfect for automating tasks and integrating Twitter functionality into Python projects.',  # Short project description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DavyJonesCodes/PyTweetToolkit',
    packages=find_packages(),
    install_requires=[
        'pillow>=10.2.0',
        'requests>=2.31.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.9",
)
