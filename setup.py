from setuptools import setup, find_packages

setup(
    name='easy-commit',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'groq',
        'openai',
        'anthropic',
        'together',
        'cohere',
        'argparse',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'easy-commit=easy_commit.cli:main',
        ],
    },
    author='Pranav Kumar',
    author_email="pranavkumarnair@gmail.com",
    description='AI-powered Git commit message generator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PraNavKumAr01/easy_commit',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)