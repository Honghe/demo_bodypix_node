# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import sys


def main(root_dir):
    mp4_file = os.path.join(root_dir, '{}.mp4'.format(os.path.basename(root_dir)))
    jpgs_dir = os.path.join(root_dir, 'jpgs')
    os.makedirs(jpgs_dir, exist_ok=True)
    args = ['ffmpeg', '-y', '-i', mp4_file, '-r', '30', '{}/%4d.jpg'.format(jpgs_dir)]
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
