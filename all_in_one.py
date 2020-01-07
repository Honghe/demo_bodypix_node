# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import sys

from functools import wraps
from time import time


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print('Elapsed time: {:.2f}'.format(end-start))
        return result
    return wrapper

@timing
def run_subprocess(args):
    print('run: {}'.format(' '.join(args)))
    process = subprocess.Popen(
        args, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
    _, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(stderr.decode('utf-8'))


def main(root_dir):
    # steps 1-4
    args = [['python3', '1_mp4_to_jpgs.py', root_dir],
            ['node', 'src/main.js', root_dir],
            ['python3', 'utils/visualize_masked_image.py', root_dir],
            ['python3', '4_jpgs_to_mp4.py', root_dir]]
    for v in args:
        run_subprocess(v)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        logging.error('Need run with: {} <dir>'.format(os.path.basename(sys.argv[0])))
    else:
        root_dir = os.path.abspath(sys.argv[1])
        main(root_dir)
