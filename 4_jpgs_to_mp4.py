# -*- coding: utf-8 -*-
import os
import subprocess

root_dir = '/home/jack/Downloads/demo_bodypix/demo'
mp4_file = os.path.join(root_dir, 'demo_masked.mp4')
jpgs_dir = os.path.join(root_dir, 'masked_jpgs')
os.makedirs(jpgs_dir, exist_ok=True)
args = ['ffmpeg', '-y', '-i', '{}/%4d.jpg'.format(jpgs_dir), '-vcodec', 'libx264', mp4_file]
print(' '.join(args))
process = subprocess.Popen(
    args, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
_, stderr = process.communicate()
if process.returncode != 0:
    raise Exception('ffmpeg return error.')
