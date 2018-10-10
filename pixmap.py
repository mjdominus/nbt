#!/usr/bin/python3

import struct
from sys import stderr
from math import inf

class pixmap():
    def __init__(self, default_pixel=(127,127,127)):
        self.xmin = self.ymin =  inf
        self.xmax = self.ymax = -inf
        self.default_pixel = default_pixel
        self.p = {}

    def key(self, x, y):
        return f'{x},{y}'
        
    def set(self, x, y, color):
#        print(f'set({x},{y}) = {color}', file=stderr)
        self.p[self.key(x, y)] = color
        self.adjust_bounds(x, y)

    def get(self, x, y):
        k = self.key(x, y)
        if k in self.p:
            return self.p[k]
        else:
            return self.default_pixel

    def adjust_bounds(self, x, y):
        if x < self.xmin: self.xmin = x
        if x > self.xmax: self.xmax = x
        if y < self.ymin: self.ymin = y
        if y > self.ymax: self.ymax = y

    def loop(self, callback):
        for y in range(self.ymin, self.ymax+1):
            for x in range(self.xmin, self.xmax+1):
                callback.__call__(x, y, self.get(x,y))

    def columns(self):
        return self.xmax - self.xmin + 1

    def rows(self):
        return self.ymax - self.ymin + 1

    def dump_ppm(self, fh):
#        print(f'x from {self.xmin} to {self.xmax}', file=stderr)
#        print(f'y from {self.ymin} to {self.ymax}', file=stderr)
#        print(f' total pixels: {self.rows() * self.columns()}', file=stderr)
        print(f'P6\n{self.columns()} {self.rows()}\n255\n',
              file=fh, end="")
        fh.flush()
        self.loop(lambda x, y, pix:
                    fh.buffer.write(struct.pack(">BBB", *pix)))

