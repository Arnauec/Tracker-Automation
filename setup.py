from setuptools import setup, find_packages

setup(
    name='Tracker-Automation',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            # If you want to run the main function in the myanonamouse/login.py file, add this line
            'tracker-automation=myanonamouse.login:main',
        ],
    }
)