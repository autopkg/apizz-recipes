#!/usr/bin/env python

from __future__ import absolute_import


import os
import shutil
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["GunZipper"]

EXTNS = {
    "gzip": ["gzip", "gz"],
}

class GunZipper(Processor):
    description = ("Gets the version of an executable file collected by FileFinder. ")
    input_variables = {
        "archive_path": {
            "required": False,
            "description": "Path to an archive. Defaults to contents of the "
            "'pathname' variable, for example as is set by "
            "URLDownloader.",
        },
        "destination_path": {
            "required": False,
            "description": (
                "Directory where archive will be unpacked, created "
                "if necessary. Defaults to RECIPE_CACHE_DIR/NAME."
            ),
        },
        "purge_destination": {
            "required": False,
            "description": "Whether the contents of the destination directory "
            "will be removed before unpacking.",
        },
        "archive_format": {
            "required": False,
            "description": (
                "The archive format. Currently supported: 'zip', "
                "'tar_gzip', 'tar_bzip2', 'tar'. If omitted, the "
                "file extension is used to guess the format."
            ),
        },
    }
    output_variables = {}

    __doc__ = description

    def get_archive_format(self, archive_path):
        """Guess archive format based on filename extension"""
        # pylint: disable=no-self-use
        for format_str, extns in EXTNS.items():
            for extn in extns:
                if archive_path.endswith(extn):
                    return format_str
        # We found no known archive file extension if we got this far
        return None

    def main(self):
        """Unarchive a file"""
        # handle some defaults for archive_path and destination_path
        archive_path = self.env.get("archive_path", self.env.get("pathname"))
        if not archive_path:
            raise ProcessorError(
                "Expected an 'archive_path' input variable but none is set!"
            )
        destination_path = self.env.get(
            "destination_path",
            os.path.join(self.env["RECIPE_CACHE_DIR"], self.env["NAME"]),
        )

        # Create the directory if needed.
        if not os.path.exists(destination_path):
            try:
                os.makedirs(destination_path)
            except OSError as err:
                raise ProcessorError(
                    "Can't create %s: %s" % (destination_path, err.strerror)
                )
        elif self.env.get("purge_destination"):
            for entry in os.listdir(destination_path):
                path = os.path.join(destination_path, entry)
                try:
                    if os.path.isdir(path) and not os.path.islink(path):
                        shutil.rmtree(path)
                    else:
                        os.unlink(path)
                except OSError as err:
                    raise ProcessorError("Can't remove %s: %s" % (path, err.strerror))

        fmt = self.env.get("archive_format")
        if fmt is None:
            fmt = self.get_archive_format(archive_path)
            if not fmt:
                raise ProcessorError(
                    "Can't guess archive format for filename %s"
                    % os.path.basename(archive_path)
                )
            self.output(
                "Guessed archive format '%s' from filename %s"
                % (fmt, os.path.basename(archive_path))
            )
        elif fmt not in EXTNS.keys():
            raise ProcessorError(
                "'%s' is not valid for the 'archive_format' variable. "
                "Must be one of %s." % (fmt, ", ".join(EXTNS.keys()))
            )

        if fmt == "gzip":
            cmd = [
                "/usr/bin/gzip",
                "-d",
                "-k",
                archive_path,
            ]
        elif fmt.endswith("gzip","gz"):
            cmd = ["/usr/bin/gzip", "-d", "-k", archive_path]

        # Call command.
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (_, stderr) = proc.communicate()
        except OSError as err:
            raise ProcessorError(
                "%s execution failed with error code %d: %s"
                % (os.path.basename(cmd[0]), err.errno, err.strerror)
            )
        if proc.returncode != 0:
            raise ProcessorError(
                "Unarchiving %s with %s failed: %s"
                % (archive_path, os.path.basename(cmd[0]), stderr)
            )

        self.output("Unarchived %s" % (archive_path))
            

if __name__ == '__main__':
    processor = GunZipper()
    processor.execute_shell()
