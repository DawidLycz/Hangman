from setuptools import setup, find_packages
import glob
import os

data_files = glob.glob('hangman\\data\\**\\*', recursive=True)
selected_files = [file.split('hangman\\', 1)[-1] for file in data_files]

setup(
    description='Simple but popular game in hangman',
    name='hangman',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/DawidLycz/Hungman',
    package_data={
    'hangman': selected_files},
    license='MIT',
    author='Dawid Lycz',
    author_email='mamnie986@gmail.com',
    install_requires=[
        'pygame',
    ],
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


#$ python setup.py bdist_wheel
#$ pip install dist\Hangman-0.1-py3-none-any.whl