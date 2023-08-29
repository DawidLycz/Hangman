from setuptools import setup, find_packages
import glob

data_files = glob.glob('hangman\\data\\**\\*', recursive=True)
selected_files = [file.removeprefix("hangman\\") for file in data_files] 

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f]
setup(
    description='Simple but popular game in hangman',
    name='hangman',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/DawidLycz/Hungman',
    package_data={
    'hangman': selected_files},
    license='MIT',
    author='Dawid Lycz',
    author_email='mamnie986@gmail.com',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
