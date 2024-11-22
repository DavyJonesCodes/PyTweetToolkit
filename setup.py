from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="PyTweetToolkit",
    version="1.0.2",
    author='Dev Jones',
    author_email='yashdhankhar5656@gmail.com',
    description='PyTweetToolkit: An intuitive Python library for managing Twitter interactions, providing tools for posting tweets, engaging with users, and analyzing social media metrics. Perfect for automating tasks and integrating Twitter functionality into Python projects.',  # Short project description
    long_description=long_description,
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
