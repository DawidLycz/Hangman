pip changes:

    To solidify the implementation of changes in the script, 
    after making modifications in the code, you should enter the following command in the terminal:

        python setup.py bdist_wheel

python to exe conversion:

    After building the wheel, you should export the project to the .exe extension. 
    There are multiple ways to do this, but I recommend using the "auto-py-to-exe" module.

    You can easily obtain it by installing it through pip: 

        pip install auto-py-to-exe
    
    After installation, you can run the converter by entering its name in the terminal:

        auto-py-to-exe

    Once the application window pops up, you just need to input the appropriate data and start the conversion process. 
    However, you can simplify this process significantly. The application provides pre-made conversion scripts.
    One such script has already been created and can be found in this folder. 
    Before it's ready to use, you'll need to make a few modifications. 
    Open the .json file and replace "[PATH TO FILE]" with the path to the repository.
    Next, in the application window, open the "Settings" tab. There is an option there to import a JSON file. 
    Use it to input the initial parameters. In the same tab, further up, you can input a custom output. 
    Then, all that's left is to initiate the conversion.

