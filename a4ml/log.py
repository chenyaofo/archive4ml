import argparse
import os
import argparse
from common.config import get_storage_dir
from common.utils import deal_archive_file
from common.custom_uuid import CustomUUID

parser = argparse.ArgumentParser()

parser.add_argument('item')

args = parser.parse_args()


if __name__ == "__main__":
    print(deal_archive_file(strorage_dir=get_storage_dir(), 
                        id_=CustomUUID(args.item),
                        filename=None, extract_dir=None, op="log"
                        ))


