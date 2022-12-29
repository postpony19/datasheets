#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Creates a json file with information about all datasheet files in
given directory path.
The output file, named '{}' by default, is also stored into
given directory path.

Examples:
   {} path/to/directory
   {} -o file_name path/to/directory

"""
# file resides in .github/scripts
import argparse
import json
import os
import pathlib
import sys
import textwrap
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from collections import OrderedDict

DEFAULT_FILE_NAME = 'bahnhof.json'

if __name__ == '__main__':
    script_name = os.path.basename(sys.argv[0])
    args_parser = argparse. ArgumentParser(
        description=textwrap.dedent(__doc__.format(DEFAULT_FILE_NAME,
                                                   script_name,
                                                   script_name)),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    args_parser.add_argument(
        'ds_files',
        metavar='path/to/directory',
        nargs=1,
        help='Directory where files are stored')
    args_parser.add_argument(
        '-o',
        '--out-file',
        metavar='file-name',
        nargs='?',
        required=False,
        default=DEFAULT_FILE_NAME,
        help='File where result is stored to (default: "{}")'.format(
            DEFAULT_FILE_NAME))
    args = args_parser.parse_args()

    # provide given file as resolved absolute path
    ds_file = pathlib.Path(args.ds_files[0]).resolve()

    if not ds_file.exists():
        args_parser.error(
            'Given path "{}" does not exists.'.format(args.ds_files[0]))

    # given path must exist and a folder
    if not ds_file.is_dir():
        args_parser.error(
            'Given path "{}" is not a folder!'.format(args.ds_files[0]))

    _working_directory = ds_file.absolute()
    # outfile is stored in given directory; check if suffix json is present,
    # add if necessary
    out_file = pathlib.Path(_working_directory,
                            args.out_file).with_suffix('.json')

    all_in_one = OrderedDict()
    for ds_element in sorted(_working_directory.glob('*.xml')):
        root = ET.parse(ds_element).getroot()
        all_in_one[ds_element.stem] = OrderedDict(
            {'viewid': ds_element.stem,
             'name': root.find('./name').text,
             'kuerzel': root.find('./kuerzel').text,
             'typ': root.find('./typ').text,
             'zeit': int(ds_element.stat().st_mtime) * 1000}
        )
    if len(all_in_one) > 0:
        with open(out_file, 'w') as jsonfile:
            json.dump(all_in_one, jsonfile, separators=(',', ':'))
