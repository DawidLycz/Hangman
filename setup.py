from setuptools import setup, find_packages
import glob

package_data={
        'hangman': list(glob.glob('hangman/data/**/*', recursive=True))
    },

setup(
    description='Simple but popular game in hangman',
    name='Hangman',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/DawidLycz/Hungman',
    package_data={
        'hangman': list(glob.glob('hangman/data/**/*', recursive=True))
    },
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


#setup(...,
    #   data_files=[('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
    #               ('config', ['cfg/data.cfg']),
    #  )


#$ python setup.py bdist_wheel