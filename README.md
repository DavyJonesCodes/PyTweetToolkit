# PyTweetToolkit

PyTweetToolkit is an intuitive Python library designed to simplify Twitter interactions, offering tools for posting tweets, engaging with followers, analyzing social media metrics, and automating various Twitter-related tasks. Ideal for developers looking to integrate Twitter functionality into Python projects or automate their social media presence with ease.

## Features

- **Tweet Posting**: Easily create and post tweets directly from your Python scripts.
- **User Engagement**: Automate following, unfollowing, blocking, and muting operations.
- **Analytics**: Analyze tweet performance, follower growth, and engagement metrics.
- **Content Automation**: Schedule tweets and manage your content strategy programmatically.

## Installation

PyTweetToolkit can be installed using multiple methods. Choose the one that suits your setup the best.

### Install the latest version from PyPI

This is the easiest way to get PyTweetToolkit up and running. Use pip for installation:

```bash
pip install PyTweetToolkit
```

For more details, visit [PyTweetToolkit on PyPI](https://pypi.org/project/PyTweetToolkit/).

### Install the latest development version

If you prefer to use the bleeding-edge version, you can install directly from our GitHub repository. First, clone the repository:

```bash
git clone https://github.com/DavyJonesCodes/PyTweetToolkit.git
cd PyTweetToolkit
pip install .
```

Alternatively, you can install directly without cloning, using:

```bash
pip install git+https://github.com/DavyJonesCodes/PyTweetToolkit.git
```

## Supported Python Versions

PyTweetToolkit is compatible with Python versions 3.9 and above. This ensures the use of the latest features and improvements in the Python language, providing a better and more efficient experience for developers using PyTweetToolkit.

Make sure you have Python 3.9 or higher installed on your system to use PyTweetToolkit. You can check your Python version by running:

```bash
python --version
```

or, on some systems:

```bash
python3 --version
```

If you need to install a newer version of Python, visit the [official Python website](https://www.python.org/downloads/) for download links and installation instructions.

## Obtaining Authentication Cookies

To use PyTweetToolkit, you'll need to obtain authentication cookies from Twitter's website using your browser's developer tools. Follow these steps to retrieve the required cookies:

1. **Login to Twitter**: Log in to your Twitter account in your web browser.

2. **Open Developer Tools**: Once logged in, open the developer tools in your web browser. You can usually access this by right-clicking on the page and selecting "Inspect".

3. **Navigate to Application Tab**: In the developer tools, navigate to the "Application" or "Storage" tab. This tab contains information about cookies, local storage, and session storage.

4. **Find Twitter Cookies**: Look for the section that displays cookies. Find the cookies associated with the Twitter website (`https://twitter.com`). These cookies typically include `auth_token` and `ct0`, among others.

5. **Locating Cookie Values**: Locate the cookies associated with the Twitter website (`https://twitter.com`). Look for cookies named `auth_token` and `ct0`.

6. **Extract Cookie Values**: Double-click on the value of the `auth_token` cookie to copy it. Similarly, double-click on the value of the `ct0` cookie to copy it as well.

7. **Use Cookie Values as Tokens**: In your Python script or application, replace `YOUR_AUTH_TOKEN` with the value copied from the `auth_token` cookie and `YOUR_CSRF_TOKEN` with the value copied from the `ct0` cookie. These values will serve as your authentication token (`auth_token`) and Cross-Site Request Forgery (CSRF) token (`csrf_token`), respectively.

For detailed instructions on how to use PyTweetToolkit, refer to the [Quick Start](#quick-start) section below.

## Quick Start

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

## Documentation

For detailed documentation, including setup guides, examples, and API references, please visit our [documentation page](https://github.com/DavyJonesCodes/PyTweetToolkit/wiki/1.-Home).

## Contributing

We welcome contributions to PyTweetToolkit! If you'd like to contribute, please fork the repository and use a pull request to add your changes. For more detailed information, check out our CONTRIBUTING.md.

## Support

If you encounter any issues or have questions about using PyTweetToolkit, please submit an issue on our GitHub issue tracker.

## License

PyTweetToolkit is released under the MIT License.
