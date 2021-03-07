from setuptools import setup, find_packages

requires = [
    'requests',
    'argparse',
    'jinja2',
    'pytz',
    'tzlocal',
    'bs4'
]

dev_requires = [
    'pipreqs'
]

setup(
    name='dabplugin-rssfeed',
    version='0.0.1',
    author='Riley Raschke',
    author_email='riley@rrappsdev.com',
    scripts=['rssfeed-plugin.py'],
    packages=['dabplugin'],
    url='https://github.com/RileyR387/dabplugin-rssfeed',
    license='LICENSE',
    description='discord-alert-bot plugin for RSS feeds',
    long_description='A discord-alert-bot plugin for RSS feeds.',
    install_requires=requires,
    extras_require={
        'dev': dev_requires
    }
)

