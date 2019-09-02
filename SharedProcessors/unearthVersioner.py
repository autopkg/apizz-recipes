#!/usr/bin/env python

from __future__ import absolute_import

import os.path
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["unearthVersioner"]

class unearthVersioner(Processor):
    description = ("Gets the unearth executable version. ")
    input_variables = {
        "source_path": {
            "required": False,
            "description": "Full path to unearth executable. Defaults to %pkgroot%/usr/local/bin/unearth/unearth. "
        }
    }
    output_variables = {
        "version": {
            "description": "The unearth executable version"
        }
    }

    __doc__ = description

    def main(self):
        if not self.env['source_path']:
            self.env['source_path'] = os.path.join(self.env['pkgroot'], "/usr/local/bin/unearth/unearth")

        self.output("unearth path: %s" % self.env['source_path'])

        if os.path.exists(self.env['source_path']):
            self.output("Found unearth executable at %s" % self.env['source_path'])
            try:
                cmd = subprocess.check_output(['/usr/bin/python', self.env['source_path'], '-v'])
                self.env['version'] = cmd.replace('\n', '')
                self.output("Version: %s" % self.env['version'])
            except OSError:
                raise ProcessorError("Can't find %s" % (self.env['source_path']))
        else:
            raise ProcessorError("Could not find unearth executable at %s" % (self.env['source_path']))

if __name__ == '__main__':
    processor = unearthVersioner()
    processor.execute_shell()
