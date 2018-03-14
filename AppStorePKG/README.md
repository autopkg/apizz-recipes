## Requirements

- mas-cli (https://github.com/mas-cli/mas)
- AppStoreExtractor.sh (https://github.com/maxschlapfer/MacAdminHelpers/tree/master/AppStoreExtract)

## Process

1. Open two Terminal windows
2. In one Terminal window, get MAS app ID for desired app(s)
<pre>mas search "[NAMEOFAPP]"</pre>
3. In the other Terminal window, run AppStoreExtrator.sh
<pre>sh /path/to/AppStoreExtractor.sh</pre>
4. Download and install the app.  If any of the MAS apps are already installed, add <code>--force</code> to the command
<pre>mas install [MASAPPID1] [MASAPPID2] ...</pre>
5. Once all downloads and installs have completed go back to the window running AppStoreExtractor.sh and enter any key.
6. When prompted, type <code>y</code> to indicate you wish to finalize the packages.  This renames the PKG to <code>APPNAME_VERSION.pkg</code> and puts it in a DMG with the same name structure.
7. Run autopkg munki recipes in this repo to import the DMGs into your munki repo

## To-do

* Write script to automatically download and (re)install MAS apps w/ mas-cli and run associated autopkg recipes
  * Option to feed list of MAS app IDs
  * Option to forcibly install
  * Option to upgrade installed apps only
