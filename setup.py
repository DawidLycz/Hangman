from setuptools import setup, find_packages
import glob

print ('hangman', list(glob.glob('hangman/data/**/*', recursive=True)))
print (find_packages())
setup(
    description='Simple but popular game in hangman',
    name='hangman',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/DawidLycz/Hungman',
    include_package_data=True,
    package_data={
    'hangman': [
    'hangman/data/databases/scoreboard.db', 
    'hangman/data/databases/settings.db',
    'hangman/data/fonts/font.ttf',
    'hangman/data/images/background.jpg',
    'hangman/data/images/background_2.jpg',
    'hangman/data/images/button_1.png', 
    'hangman/data/images/button_2.png',
    'hangman/data/images/button_3.png', 
    'hangman/data/images/gallow_0.png',
    'hangman/data/images/gallow_1.png', 
    'hangman/data/images/gallow_10.png',
    'hangman/data/images/gallow_11.png', 
    'hangman/data/images/gallow_12.png',
    'hangman/data/images/gallow_2.png', 
    'hangman/data/images/gallow_3.png',
    'hangman/data/images/gallow_4.png', 
    'hangman/data/images/gallow_5.png',
    'hangman/data/images/gallow_6.png', 
    'hangman/data/images/gallow_7.png',
    'hangman/data/images/gallow_8.png', 
    'hangman/data/images/gallow_9.png',
    'hangman/data/images/gallow_background.jpg', 
    'hangman/data/images/intro_background.jpg',
    'hangman/data/images/menu_background.jpg',
    'hangman/data/resolutions/1200_800.json', 
    'hangman/data/resolutions/1280_720.json',
    'hangman/data/resolutions/1920_1080.json', 
    'hangman/data/resolutions/800_600.json',
    'hangman/data/soundeffects/beep.mp3', 
    'hangman/data/soundeffects/correct.mp3',
    'hangman/data/soundeffects/error.mp3', 
    'hangman/data/soundeffects/game_over.mp3',
    'hangman/data/soundeffects/intro.mp3', 
    'hangman/data/soundeffects/music.mp3',
    'hangman/data/soundeffects/outro.mp3', 
    'hangman/data/soundeffects/success.mp3',
    'hangman/data/soundeffects/wrong.mp3',
    'hangman/data/text/english_key_words.json', 
    'hangman/data/text/english_strings.json',
    'hangman/data/text/polish_key_words.json', 
    'hangman/data/text/polish_strings.json'
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