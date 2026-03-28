import os

def create_nested_dirs(path="test_dir/sub_dir"):
    os.makedirs(path, exist_ok=True)
    print(f"Nested directories {path} created.")

def list_dir(path="test_dir"):
    print(f"Contents of {path}: {os.listdir(path)}")

if __name__ == "__main__":
    create_nested_dirs()
    list_dir()