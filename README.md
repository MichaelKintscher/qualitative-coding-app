# Qualitative Coding App
This desktop application supports researchers and students performing qualitative coding analysis on videos.

## Requirements
- Python >= 3.7
- PySide6

## How to set up and run the application
1. Ensure the Python >= 3.7 requirement is met.  
If python needs to be updated or installed, the following guide can be followed: https://wiki.python.org/moin/BeginnersGuide/Download  

2. Clone the repository and change your current directory to the project directory.  
`git clone https://github.com/MichaelKintscher/qualitative-coding-app.git && cd qualitative-coding-app`

3. We recommend setting up a virtual environment.  
Unix/macOS: `python3 -m venv env`  
Windows: `py -m venv env`  

4. Activate the virtual environment.  
Unix/macOS: `source env/bin/activate`  
Windows: `.\env\Scripts\activate.bat`  

5. Install PySide6 to your virtual environment using the pip package manager.  
Unix/macOS: `python3 -m pip install PySide6`  
Windows: `py -m pip install PySide6`  

6. Install superqt to your virtual environment using the pip package manager.  
Unix/macOS: `python3 -m pip install superqt`  
Windows: `py -m pip install superqt`  

7. Run the application  
Unix/macOS: `python3 main.py`  
Windows: `py main.py`  

## Development Set up
Any text-editor or IDE, preferably with python support, can be used to develop the project. The previous steps will manually set up the project,
however most IDEs should have support for facilitating the process described above. We recommend the PyCharm IDE for development.

## Known Bugs
1. When saving a button definition, the name must be globally unique.
2. Does not support the load video feature on macOS due to a bug.
3. User Settings are saved if there is text in any of the fields when User Settings is closed.
The User Settings will then be applied the next time any session is opened.
4. If a button is created with x columns pre-defined and executed on a table with columns
less than x, the data will spill over to the next row.
5. When creating a new button, the user cannot define columns fields for any unnamed columns.

## Limitations
1. The user can set a minimum cell height for the table, but cannot manually adjust as they can with table cell width.
2. Column names are not exported when the table data is exported to a csv file.