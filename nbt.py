#!/usr/bin/python3

import struct
import sys

class nbt():
    def __init__(self, file=None, verbose=False):
        if file:
            self.filename = file
            self.fh = open(file, 'rb')
            self.pos = 0
            self.depth = 0
            self.verbose = verbose
            self.contents = self.read_whole_tag()

    def read_whole_tag(self):
        (tag_type, tag_name) = self.read_tag_header()
        data = self.read_tag_data(tag_type)
        return { "type": tag_type, "name": tag_name, "data": data }

    def read_tag_data(self, tag_type):
        if tag_type == 0: return None
        elif tag_type == 1: return self.get_byte()
        elif tag_type == 2: return self.get_short()
        elif tag_type == 3: return self.get_int()
        elif tag_type == 4: return self.get_long()
        elif tag_type == 5: return self.get_float()
        elif tag_type == 6: return self.get_double()
        elif tag_type == 7: return self.read_byte_array()
        elif tag_type == 8: return self.read_string()
        elif tag_type == 9: return self.read_list()
        elif tag_type == 10: return self.read_compound_data()

    def read_byte_array(self):
        payload_size = self.get_int()
        bytes = self.read(payload_size)
        self.diag("Read array of %d bytes" % payload_size)
        return bytes
        
    def read_string(self):
        payload_size = self.get_short()
        string = self.read(payload_size, decode=True)
        return string

    def read_list(self):
        subtype = self.get_byte()
        payload_size = self.get_int()
        data = []
        for i in range(payload_size):
            data.append(self.read_tag_data(subtype))
        self.diag("Read list of %d items of subtype %d" % (payload_size, subtype))
        return data

    def read_compound_data(self):
        contents = {}
        self.depth += 1
        while True:
            next = self.read_whole_tag()
            if next["type"] == 0: self.depth -= 1; return contents
            else:
                contents.__setitem__(next["name"], next["data"])
        
    def read_tag_header(self):
        ttype = self.get_byte()
        if ttype == 0: return (0, None) # tag_END has no name
        
        length = self.get_short()
        tname = self.read(length, decode=True)
        self.diag("Started reading tag (type %d) '%s'" % (ttype, tname))
        return (ttype, tname)

    def get_byte(self):
        return self.get(1, ">b")

    def get_short(self):
        return self.get(2, ">h")

    def get_int(self):
        return self.get(4, ">i")

    def get(self, nbytes, format):
        bytes = self.read(nbytes)
        self.diag("Unpacking %d bytes into format '%s'" % (len(bytes), format))
        (res,) = struct.unpack(format, bytes)
        self.diag("  Result: %s" % repr(res))
        return res
    
    def read(self, nbytes, decode=False):
        if nbytes == 0: return b''
        bytes = self.fh.read(nbytes)
        self.pos += nbytes
        if decode:
            return bytes.decode("utf-8")
        else:
            return bytes

    def nul_check(self):
        b = self.get_byte()
        if b != 0:
            raise Exception("Expected tag_END at position %d; got %u instead"
                            % (self.pos, b))

    def diag(self, msg):
        if self.verbose:
            print(" |" * self.depth, end="")
            print(msg)
