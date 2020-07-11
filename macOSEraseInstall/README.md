## macOSEraseInstall

Imports a DMG containing a macOS installer app into a munki_repo.

### Usage

1. Clone my repo - https://github.com/autopkg/apizz-recipes.git
2. Create an override of the desired macOSEraseInstall import recipe.
3. Use a tool like [installinstallmacos.py](https://github.com/munki/macadmin-scripts) to create a compressed DMG of the desired macOS installer.
4. Copy/move the DMG into a desired location which your autopkg instance can access.
5. Specify the full path to your macOS DMG in the recipe's `PATH` variable. The DMG file name must contain the major macOS version (ex. 10.14; 10.15).
6. Run the recipe.
7. Profit.