import argparse
import os
import argparse
from common.config import get_storage_dir
from common.utils import remove_archive
from common.custom_uuid import CustomUUID

parser = argparse.ArgumentParser()

parser.add_argument('item')

args = parser.parse_args()


if __name__ == "__main__":
    remove_archive(strorage_dir=get_storage_dir(), id_=CustomUUID(args.item))


