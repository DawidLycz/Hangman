from setuptools import setup, find_packages

setup(
    description='Simple but popular game in hangman',
    name='Hangman',
    version='0.1',
    packages=find_packages(),
    scripts=['Hangman.py', 'Hangman_text_handler.py', "Hangman_numbers_loader.py"],
    url='https://github.com/TwojeKonto/NazwaRepozytorium',
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

