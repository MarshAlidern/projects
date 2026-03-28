import shutil
import os


shutil.copy("sample.txt", "sample_backup1.txt")
shutil.copy("sample.txt", "sample_backup2.txt")
print("File copied successfully!")

if os.path.exists("sample_backup1.txt"):
    os.remove("sample_backup1.txt")
    print("Backup deleted safely.")
else:
    print("File not found.")