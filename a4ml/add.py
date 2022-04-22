import argparse
import os
import argparse
from common.config import get_storage_dir
from common.utils import add_archive

parser = argparse.ArgumentParser()

parser.add_argument('dir')

args = parser.parse_args()


if __name__ == "__main__":
    for root, dirs, files in [[args.dir, [""], []]] + list(os.walk(args.dir, topdown=False)):
        for dir in dirs:
            crnt_dir = os.path.join(root, dir)
            if os.path.exists(os.path.join(crnt_dir, "uuid")):
                add_archive(input_dir=crnt_dir, strorage_dir=get_storage_dir())

