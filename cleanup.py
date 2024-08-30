import os
import glob

folder_path = 'images'

files = glob.glob(os.path.join(folder_path, '*'))

for file in files:
    try:
        os.remove(file)
        print(f"Deleted: {file}")
    except Exception as e:
        print(f"Error deleting {file}: {e}")

