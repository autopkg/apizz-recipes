#!/usr/bin/env python

from __future__ import absolute_import

import os.path
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["ExecutableFileVersioner"]

class ExecutableFileVersioner(Processor):
    description = ("Gets the version of an executable file collected by FileFinder. ")
    input_variables = {
        "found_filename": {
            "required": True,
            "description": "Full path to the executable file collected by FileFinder. "
        },
        "interpreter_path": {
            "required": False,
            "default": "/usr/bin/python",
            "description": "Full path to the interpreter to call the executable file, if needed. "
        },
        "version_argument": {
            "required": True,
            "description": "Argument passed to executable file to collect its version. "
        }
    }
    output_variables = {
        "version": {
            "description": "The executable file version"
        }
    }

    __doc__ = description

    def main(self):
        if os.path.exists(self.env['found_filename']):
            self.output("Found executable at %s" % self.env['found_filename'])
            try:
                cmd = subprocess.check_output([ self.env['interpreter_path'], self.env['found_filename'], self.env['version_argument']])
                # Get version and remove offending new line at the end
                self.env['version'] = cmd.replace('\n', '')
                self.output("Version: %s" % self.env['version'])
            except OSError:
                raise ProcessorError("Can't find %s" % (self.env['found_filename']))
        else:
            raise ProcessorError("Could not find executable at %s" % (self.env['found_filename']))

if __name__ == '__main__':
    processor = ExecutableFileVersioner()
    processor.execute_shell()
