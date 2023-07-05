#!/usr/bin/env python3
# -*-coding:utf-8 -*-
'''
    This file extract video from Quark netdisk backuped live photo.
    Under MIT licence you can do whatever you want.
    从夸克网盘备份的实况照片中提取视频。
'''
import os
import sys
import struct


class Photo():
    def __init__(self, path) -> None:
        self.path = path
        self.path_without_ext = os.path.splitext(self.path)[0]

        self.path = path
        with open(path, 'rb') as f:
            self.data = f.read()
            self.file_size = f.tell()

    def is_live_photo(self):
        tail = self.data[-12:]
        if tail[:-8] == b'livp':  # livp....
            self.video_size, = struct.unpack("<i", tail[-4:])
            self.image_size = self.file_size-self.video_size-12
            return True
        else:
            return False

    def seperate_image_video(self):
        with open(self.path, 'wb') as f:
            f.write(self.data[:self.image_size])
        with open(self.path_without_ext+'.MOV', 'wb') as f:
            f.write(self.data[self.image_size:self.file_size-12])


if __name__ == "__main__":
    folder = sys.argv[1]
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".JPG"):
                full_path = os.path.join(root, file)
                p = Photo(full_path)
                if p.is_live_photo():
                    p.seperate_image_video()
