import os
import shutil
import time


class Store_Move_Delete:

    def __init__(self, directory):

        self.folder = "Recycle_bin"
        self.directory = directory

    def store_file_move_file(self):

        # Change directory
        os.chdir(self.directory)

        # Create recycle bin folder
        os.makedirs(self.folder, exist_ok=True)

        # All files
        files = os.listdir(self.directory)

        # Only mp3 files
        mp3_files = []

        for file in files:

            if file.endswith(".mp3"):

                source_path = os.path.join(
                    self.directory,
                    file
                )

                if os.path.isfile(source_path):

                    mp3_files.append(file)

        print(f"\n🎵 Total files found: {len(mp3_files)}\n")

        # Move files one by one
        for file in mp3_files:

            source_path = os.path.join(
                self.directory,
                file
            )

            destination_path = os.path.join(
                self.directory,
                self.folder,
                file
            )

            # Copy file
            shutil.copy2(
                source_path,
                destination_path
            )

            # Delete original
            os.remove(source_path)

            print(f"✅ {file} moved successfully.")

            time.sleep(0.2)

    def clear_recycle_bin(self):

        print(
            "\n♻️ Do you want to clear recycle bin? yes or no"
        )

        user = input(":- ")

        if user.lower() == "yes":

            recycle_path = os.path.join(
                self.directory,
                self.folder
            )

            # Delete recycle bin directly
            shutil.rmtree(recycle_path)

            print("\n🗑️ Recycle bin cleared successfully.")

        else:

            print(
                f"\n📁 Files are inside '{self.folder}'"
            )


# Read path from txt file
with open("/storage/emulated/0/path.txt", "r") as file:

    path = file.read().strip()


# Validate path
if not path:

    print("❌ path.txt is empty.")
    exit(1)

if not os.path.isdir(path):

    print(f"❌ Directory does not exist: {path}")
    exit(1)


# Create object
file_manager = Store_Move_Delete(path)

# Move files
file_manager.store_file_move_file()

# Clear recycle bin
file_manager.clear_recycle_bin()
      
