import shutil
import os

def move_file(src="sample.txt", dst_dir="test_dir"):
    if os.path.exists(src):
        shutil.move(src, os.path.join(dst_dir, src))
        print(f"{src} moved to {dst_dir}")
    else:
        print(f"{src} not found!")

def copy_file(src="test_dir/sample.txt", dst_dir="test_dir/sub_dir"):
    if os.path.exists(src):
        shutil.copy(src, os.path.join(dst_dir, os.path.basename(src)))
        print(f"{src} copied to {dst_dir}")
    else:
        print(f"{src} not found!")

if __name__ == "__main__":
    move_file()
    copy_file()