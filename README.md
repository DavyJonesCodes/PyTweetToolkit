# PyTweetToolkit

<p align="center">
  <img src="https://raw.githubusercontent.com/DavyJonesCodes/PyTweetToolkit/main/assets/logo.png" alt="Logo" height="128px">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
  <img src="https://img.shields.io/badge/X-%23000000.svg?style=for-the-badge&logo=X&logoColor=white"/>
  <img src="https://img.shields.io/github/license/DavyJonesCodes/PyTweetToolkit?style=for-the-badge"/>
</p>

**PyTweetToolkit** is an intuitive Python library designed to simplify Twitter interactions, offering tools for posting tweets, engaging with followers, analyzing social media metrics, and automating various Twitter-related tasks. It's perfect for developers looking to integrate Twitter functionality into Python projects or automate their social media presence with ease.

## ✨ Features

- 🐦 **Tweet Posting**: Easily create and post tweets directly from your Python scripts.
- 🤝 **User Engagement**: Automate following, unfollowing, blocking, and muting operations.
- 📊 **Analytics**: Analyze tweet performance, follower growth, and engagement metrics.
- 🗓️ **Content Automation**: Schedule tweets and manage your content strategy programmatically.

## 🚀 Installation

You can easily install PyTweetToolkit via pip from [PyPI](https://pypi.org/project/PyTweetToolkit/):

```bash
pip install PyTweetToolkit
```

### Install the latest development version

If you prefer to use the latest development version, you can install it directly from our GitHub repository:

```bash
pip install git+https://github.com/DavyJonesCodes/PyTweetToolkit.git
```

## 🐍 Supported Python Versions

PyTweetToolkit is compatible with Python versions 3.9 and above. Make sure you have Python 3.9 or higher installed on your system:

```bash
python --version
```

If you need to install a newer version of Python, visit the [official Python website](https://www.python.org/downloads/) for installation instructions.

## 🔐 Obtaining Authentication Cookies

To use PyTweetToolkit, you'll need to obtain authentication cookies from Twitter's website using your browser's developer tools. Follow these steps:

1. **Login to Twitter**: Log in to your Twitter account in your web browser.
2. **Open Developer Tools**: Right-click on the page and select "Inspect" to open the developer tools.
3. **Navigate to Application Tab**: Go to the "Application" or "Storage" tab in the developer tools.
4. **Find Twitter Cookies**: Look for the cookies associated with Twitter (`https://twitter.com`), especially `auth_token` and `ct0`.
5. **Extract Cookie Values**: Copy the values of `auth_token` and `ct0`.
6. **Use Cookie Values as Tokens**: Use these values as `auth_token` and `csrf_token` in your Python script.

For detailed usage instructions, refer to the [Quick Start](#quick-start) section below.

## ⚡ Quick Start

Here's a quick example to get you started with PyTweetToolkit:

```python
from PyTweetToolkit import PyTweetClient

# Initialize the client with your credentials
client = PyTweetClient(auth_token="YOUR_AUTH_TOKEN", csrf_token="YOUR_CSRF_TOKEN")

# Post a tweet
client.post_tweet("Hello, world! #MyFirstTweet")

# Follow a user
client.follow("python_community")
```

## 📚 Documentation

For detailed documentation, including setup guides, examples, and API references, please visit our [documentation page](https://github.com/DavyJonesCodes/PyTweetToolkit/wiki/1.-Home).

## 🤝 Contributions

Contributions are welcome! 🎉 If you'd like to contribute to PyTweetToolkit, feel free to fork the repository and submit a pull request. If you have any questions or need guidance, don't hesitate to contact me at [devjonescodes@gmail.com](mailto:devjonescodes@gmail.com).

## 📄 License

This project is licensed under the MIT License. For more details, see the [LICENSE](./LICENSE) file.

## 📬 Support

If you have any questions, suggestions, or run into any issues, feel free to open an issue on our GitHub repository or reach out via email at [devjonescodes@gmail.com](mailto:devjonescodes@gmail.com). We're here to help! 😊
