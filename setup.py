from setuptools import setup, find_packages
import glob
import os

print ('hangman', list(glob.glob('hangman/data/**/*', recursive=True)))
print (find_packages())
json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'text', 'polish_strings.json')
setup(
    description='Simple but popular game in hangman',
    name='hangman',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/DawidLycz/Hungman',
    package_data={
    'hangman': [
    'data/databases/scoreboard.db', 
    'data/databases/settings.db',
    'data/fonts/font.ttf',
    'data/images/background.jpg',
    'data/images/background_2.jpg',
    'data/images/button_1.png', 
    'data/images/button_2.png',
    'data/images/button_3.png', 
    'data/images/gallow_0.png',
    'data/images/gallow_1.png', 
    'data/images/gallow_10.png',
    'data/images/gallow_11.png', 
    'data/images/gallow_12.png',
    'data/images/gallow_2.png', 
    'data/images/gallow_3.png',
    'data/images/gallow_4.png', 
    'data/images/gallow_5.png',
    'data/images/gallow_6.png', 
    'data/images/gallow_7.png',
    'data/images/gallow_8.png', 
    'data/images/gallow_9.png',
    'data/images/gallow_background.jpg', 
    'data/images/intro_background.jpg',
    'data/images/menu_background.jpg',
    'data/resolutions/1200_800.json', 
    'data/resolutions/1280_720.json',
    'data/resolutions/1920_1080.json', 
    'data/resolutions/800_600.json',
    'data/soundeffects/beep.mp3', 
    'data/soundeffects/correct.mp3',
    'data/soundeffects/error.mp3', 
    'data/soundeffects/game_over.mp3',
    'data/soundeffects/intro.mp3', 
    'data/soundeffects/music.mp3',
    'data/soundeffects/outro.mp3', 
    'data/soundeffects/success.mp3',
    'data/soundeffects/wrong.mp3',
    'data/text/english_key_words.json', 
    'data/text/english_strings.json',
    'data/text/polish_key_words.json', 
    'data/text/polish_strings.json'
    ]},
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
#$ pip install dist\Hangman-0.1-py3-none-any.whl