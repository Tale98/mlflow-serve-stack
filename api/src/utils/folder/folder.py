import os
import shutil
BASE_PATH = os.getcwd()
class TempFolder:
    def __init__(self, folder_name: str):
        self.folder_name = folder_name
        self.path = f"{BASE_PATH}/temp/{self.folder_name}"

    def create(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    def create_subfolder(self, *args):
        subfolder_path = os.path.join(self.path, *args)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        return subfolder_path
    def delete(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)