import os    

def load_archive(archive):
    with open(archive) as file:
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


def add_file(archive, file):
    archive_map = load_archive(archive)
    with open(archive, "w") as af:
        pos = af.read(4)
        size = os.path.getsize(file)
        with open(file) as f:
            af.seek(pos, os.SEEK_SET)
            af.write(f.read())
        for fn in archive_map:
            pos = archive_map[fn][0]
            size = archive_map[fn][1]
            af.write(fn + '\0')
            af.write(pos.to_bytes(4, byteorder='big'))
            af.write(size.to_bytes(4, byteorder='big'))
        af.write(file + '\0')
        af.write(pos.to_bytes(4, byteorder='big'))
        af.write(size.to_bytes(4, byteorder='big'))
    return True


def extract_file(archive, file_name, file_path):
    archive_map = load_archive(archive)
    if file_name not in archive_map:
        print("ERROR: ", file_name, " doesn't exist in archive")
        return False
    
    with open(archive) as file:
        pos = archive_map[file_name][0]
        size = archive_map[file_name][1]
        with open(file_path + file_name, "w") as new_file:
            file.seek(pos, os.SEEK_SET)
            new_file.write(file.read(size))

    return True


def list_files(archive):
    archive_map = load_archive(archive)
    for file_name in archive_map:
        print(file_name, ", ", archive_map[file_name][1], " bytes")