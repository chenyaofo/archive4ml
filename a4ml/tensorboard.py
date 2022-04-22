import argparse
import os
import argparse
import yaml
import random
import string

from common.config import get_storage_dir
from common.utils import deal_archive_file
from common.custom_uuid import CustomUUID

parser = argparse.ArgumentParser()

parser.add_argument('items')
parser.add_argument('port')

args = parser.parse_args()

length=6

letters = string.ascii_lowercase

RANDOMLETTERS=''.join(random.choice(letters) for i in range(length))

TMPDIR = f"/tmp/a4ml-{RANDOMLETTERS}"

if __name__ == "__main__":
    if not os.path.exists(args.items):
        raise ValueError(f"Can not open list file {args.items}")
    
    with open(args.items, "r") as stream:
        archive_dict = yaml.safe_load(stream)
        if not isinstance(archive_dict, dict):
            raise ValueError(f"Can not load config {args.items} as dict, get {type(archive_dict)}:\n{archive_dict}")

    for k, v in archive_dict.items():
        current_extracted_dir = os.path.join(TMPDIR, v)
        os.makedirs(current_extracted_dir, exist_ok=True)
        deal_archive_file(strorage_dir=get_storage_dir(), 
                            id_=CustomUUID(k),
                            filename=None, extract_dir=current_extracted_dir, op="extract"
                            )
        print(f"Temporarily extract {k} in {current_extracted_dir}")

    print(f"Run tensorboard in {TMPDIR} ...")
    
    os.system(f"tensorboard --bind_all --port {args.port} --logdir {TMPDIR}")


