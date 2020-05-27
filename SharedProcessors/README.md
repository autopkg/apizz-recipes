## SharedProcessors

### ExecutableFileVersioner

#### Usage:

In my situation, I was acquiring an executable file from GitHub which was not available as a release and which did not have an easily acquirable version number. As a result, the only way to get the version was to call the executable file itself with the applicable version argument (ex. `-v`, `--version`, etc.).

Running this for `autopkg` manually would look like:

```
# (interpreter)   (executable file)  (argument)
/usr/bin/python /usr/local/bin/autopkg version
```

#### Requirements:

1. Meant to be used in conjunction with `FileFinder` to collect and assign the desired executable file path to the `found_filename` variable.
2. Supply a version argument to the `version_argument` variable.
3. If nothing is supplied for `interpreter_path`, defaults to /usr/bin/python

#### Examples:

In a recipe involving a python script where the version argument is `--version`:

```
<dict>
    <key>Arguments</key>
    <dict>
        <key>pattern</key>
        <string>%RECIPE_CACHE_DIR%/path/to/executable.py</string>
    </dict>
    <key>Processor</key>
    <string>FileFinder</string>
</dict>
<dict>
    <key>Arguments</key>
    <dict>
        <key>version_argument</key>
        <string>--version</string>
    </dict>
    <key>Processor</key>
    <string>ExecutableFileVersioner</string>
</dict>
```

In a recipe involving a shell script where the version argument is `version`:

```
<dict>
    <key>Arguments</key>
    <dict>
        <key>pattern</key>
        <string>%RECIPE_CACHE_DIR%/path/to/executable.sh</string>
    </dict>
    <key>Processor</key>
    <string>FileFinder</string>
</dict>
<dict>
    <key>Arguments</key>
    <dict>
        <key>interpreter_path</key>
        <string>/bin/sh</string>
        <key>version_argument</key>
        <string>version</string>
    </dict>
    <key>Processor</key>
    <string>ExecutableFileVersioner</string>
</dict>
```

Example output:

```
FileFinder
{'Input': {'pattern': u'/Users/<user>/Library/AutoPkg/Cache/com.github.apizz.pkg.unearth/unearth/usr/local/bin/unearth/unearth'}}
FileFinder: No value supplied for find_method, setting default value of: glob
FileFinder: Found file match: '/Users/<user>/Library/AutoPkg/Cache/com.github.apizz.pkg.unearth/unearth/usr/local/bin/unearth/unearth' from globbed '/Users/ap.orlebeke/Library/AutoPkg/Cache/com.github.apizz.pkg.unearth/unearth/usr/local/bin/unearth/unearth'
{'Output': {'found_filename': u'/Users/<user>/Library/AutoPkg/Cache/com.github.apizz.pkg.unearth/unearth/usr/local/bin/unearth/unearth'}}
ExecutableFileVersioner
{'Input': {'found_filename': u'/Users/<user>/Library/AutoPkg/Cache/com.github.apizz.pkg.unearth/unearth/usr/local/bin/unearth/unearth',
           'version_argument': u'-v'}}
ExecutableFileVersioner: No value supplied for interpreter_path, setting default value of: /usr/bin/python
ExecutableFileVersioner: Found executable at /Users/<user>/Library/AutoPkg/Cache/com.github.apizz.pkg.unearth/unearth/usr/local/bin/unearth/unearth
ExecutableFileVersioner: Version: 0.0.1
{'Output': {'version': '0.0.1'}}
```

--