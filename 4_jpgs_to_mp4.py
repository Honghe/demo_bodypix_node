# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import sys


def main(root_dir):
    mp4_file = os.path.join(root_dir, 'masked.mp4')
    jpgs_dir = os.path.join(root_dir, 'masked_jpgs')
    os.makedirs(jpgs_dir, exist_ok=True)
    args = ['ffmpeg', '-y', '-i', '{}/%4d.jpg'.format(jpgs_dir), '-vcodec', 'libx264', '-r', '25', mp4_file]
    print(' '.join(args))
    process = subprocess.Popen(
        args, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
    _, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception('ffmpeg return error.')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        logging.error('Need run with: {} <dir>'.format(os.path.basename(sys.argv[0])))
    else:
        root_dir = os.path.abspath(sys.argv[1])
        main(root_dir)
