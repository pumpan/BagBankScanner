BagBankScanner
BagBankScanner is a World of Warcraft addon by Pumpan designed for version 1.12.1 (Vanilla WoW). It provides functionality to scan and track items stored in both player bags and the bank, allowing you to keep track of your items across sessions.
Installation
1. Download the addon files from GitHub.
2. Extract the contents of the zip file into your WoW Classic Interface\AddOns directory.
    Optionally, move the Generator folder to your preferred location.
Requirements
    Python
Generator Installation
1.Execute Pythoninstaller.bat (or install Python from the official website).
2.Execute StartGenerate.bat (you will be prompted to select a folder, and this is only needed once).
3. Select the SavedVariables folder, for example, with the default installation path:
    C:\Program Files (x86)\World Of Warcraft\WTF\Account\YourUsername\ServerName\YourBankCharacter
Now, a new file called "wow_items.html" should have been generated! Open or share it, and all your items should be listed there! Note: every time you want to update/generate/share your bank inventory, you have to execute StartGenerate.bat.
Usage
Automatic Scanning
BagBankScanner automatically scans your bag and bank contents under the following conditions:
    Whenever your bags are updated (e.g., looting, selling items).
    When bank slots change and the bank frame is open.
Manual Scanning
You can manually trigger scans using the /bbscan slash command followed by one of the following options:
    /bbscan bags: Scan only the player's bags.
    /bbscan bank: Scan only the bank (requires bank to be open).
    /bbscan all: Scan both bags and the bank.
Support
For any issues, feedback, or feature requests, please open an issue on the GitHub repository.
License
This addon is licensed under the MIT License. Feel free to modify and distribute it according to the terms of the license.
