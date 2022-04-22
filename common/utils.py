import os
import zipfile

from .custom_uuid import CustomUUID

def read_uuid_from_file(uuid_path:str):
    with open(uuid_path, "r") as f:
        return f.read()

def get_archive_path(strorage_dir:str,id_:CustomUUID):
    paths = id_.seperate_string
    return os.path.join(strorage_dir, *paths)

def get_archive_dir(strorage_dir:str,id_:CustomUUID):
    paths = id_.seperate_string
    return os.path.join(strorage_dir, *paths[:-1])

def is_archive_existed(strorage_dir:str,id_:CustomUUID):
    return os.path.exists(get_archive_path(strorage_dir=strorage_dir, id_=id_))

def add_archive(input_dir:str, strorage_dir:str):
    if not os.path.isdir(input_dir):
        raise ValueError(f"The path {input_dir} is not a directory (add archive).")
    
    uuid_path = os.path.join(input_dir, "uuid")
    if not os.path.exists(uuid_path):
        raise ValueError(f"The uuid {uuid_path} does not exist (add archive).")
    
    uuid_str = read_uuid_from_file(uuid_path)

    _add_archive(input_dir=input_dir, 
                strorage_dir=strorage_dir, 
                id_=CustomUUID(uuid_str))

def hanan_read_size(size:int):
    if size < 1024:
        return f"{size} B"
    elif size < 1024**2:
        return f"{size/(1024**1):.2f} K"
    elif size < 1024**3:
        return f"{size/(1024**2):.2f} M"
    else:
        return f"{size/(1024**3):.2f} G"

def _add_archive(input_dir:str, strorage_dir:str, id_:CustomUUID):
    os.makedirs(get_archive_dir(strorage_dir, id_), exist_ok=True)

    archive_path = get_archive_path(strorage_dir, id_)

    if is_archive_existed(strorage_dir=strorage_dir, id_=id_):
        size = os.path.getsize(archive_path) 
        print(f"Skip {input_dir}, has been compressed in {archive_path} (size={hanan_read_size(size)})")
        return
    
    with zipfile.ZipFile(archive_path, "w") as f:
        for root, dirs, files in os.walk(input_dir, topdown=False):
            for name in files:
                rel_root = os.path.relpath(root, input_dir)
                f.write(os.path.join(root, name), os.path.join(rel_root, name))
    size = os.path.getsize(archive_path) 
    print(f"{input_dir} => {archive_path} (size={hanan_read_size(size)})")

def remove_archive(strorage_dir:str, id_:CustomUUID):
    archive_path = get_archive_path(strorage_dir=strorage_dir, id_=id_)
    if not is_archive_existed(strorage_dir=strorage_dir, id_=id_):
        raise ValueError(f"Can not remove {archive_path} since it does not exist")
    else:
        os.remove(archive_path)
        print(f"remove {archive_path}")

def deal_archive_file(strorage_dir:str, id_:CustomUUID, filename:str, extract_dir:str, op:str):
    archive_path = get_archive_path(strorage_dir, id_)
    if not is_archive_existed(strorage_dir=strorage_dir, id_=id_):
        raise ValueError(f"Can not find {archive_path} since it does not exist")
    with zipfile.ZipFile(archive_path, "r") as zf:
        if op == "ls":
            for file in zf.namelist():
                print(file)
        elif op == "cat":
            with zf.open(filename, "r") as f:
                return f.read().decode("utf-8") 
        elif op == "extract":
            zf.extractall(extract_dir)
            print(f"extract {id_} to {extract_dir}")
        elif op == "log":
            logs_list = []
            for file in zf.namelist():
                if file.endswith(".log"):
                    logs_list.append(file)
            if len(logs_list) != 1:
                raise ValueError(f"Can not open log since len(log) == {len(logs_list)}\nlogs are {logs_list}")
            with zf.open(logs_list[0]) as f:
                return f.read().decode("utf-8") 