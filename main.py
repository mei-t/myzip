import os

def load_archive(archive):
    file = open(archive)
    map_pos = file.read(4)
    file.seek(0, os.SEEK_END)
    end_pos = file.tell()
    archive_map = dict()
    file.seek(map_pos, os.SEEK_SET)
    while file.tell() != end_pos:
        file_name = ""
        while True:
            c = file.read(1)
            if c == '\0':
                break
            file_name += str(c)
        
        pos = int.from_bytes(file.read(4), byteorder='big')
        size = int.from_bytes(file.read(4), byteorder='big')
        archive_map[file_name] = (pos, size)
    
    return archive_map