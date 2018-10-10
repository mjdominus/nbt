#!/usr/bin/python3

import struct
from sys import stderr

class pixmap():
    def __init__(self, default_pixel=(127,127,127)):
        self.xmin = None
        self.xmax = None
        self.ymin = None
        self.ymax = None
        self.default_pixel = default_pixel
        self.p = {}

    def key(self, x, y):
        return f'{x},{y}'
        
    def set(self, x, y, color):
#        print(f'set({x},{y}) = {color}', file=stderr)
        self.p[self.key(x,y)] = color
        self.adjust_bounds(x, y)

    def get(self, x, y):
        k = self.key(x, y)
        if k in self.p:
            return self.p[k]
        else:
            return self.default_pixel

    def adjust_bounds(self, x, y):
        if self.xmin is None or x < self.xmin: self.xmin = x
        if self.xmax is None or x > self.xmax: self.xmax = x
        if self.ymin is None or y < self.ymin: self.ymin = y
        if self.ymax is None or y > self.ymax: self.ymax = y

    def loop(self, callback):
        for y in range(self.ymin, self.ymax+1):
            for x in range(self.xmin, self.xmax+1):
                callback.__call__(x, y, self.get(x,y))

    def columns(self):
        return self.xmax - self.xmin + 1

    def rows(self):
        return self.ymax - self.ymin + 1

    def dump_ppm(self, fh):
        print(f'P6\n{self.rows()} {self.columns()}\n255\n',
              file=fh, end="")
        fh.flush()
        self.loop(lambda x, y, pix:
                    fh.buffer.write(struct.pack(">BBB", *pix)))

