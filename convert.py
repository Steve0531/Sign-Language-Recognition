import os
import shutil
import string

# Define the parent directory containing source folders (0 to 25)
parent_source_folder = 'D:/Sign Language Recognization/asl_dataset'

# Define the parent destination folder (where 'A' to 'Z' folders will be created)
parent_destination_folder = 'D:/Sign Language Recognization/cov_data'

# Get list of destination folder names 'A' to 'Z'
destination_folders = list(string.ascii_uppercase)  # ['A', 'B', 'C', ..., 'Z']

# Iterate through source folders named '0' to '25'
for idx, folder_name in enumerate(os.listdir(parent_source_folder)):
    # Define the full source folder path
    source_folder_path = os.path.join(parent_source_folder, folder_name)

    # Define the destination folder (e.g., 'A', 'B', ..., 'Z')
    destination_folder_name = destination_folders[idx]
    destination_folder_path = os.path.join(parent_destination_folder, destination_folder_name)

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)

    # Copy and rename PNG images from the source to the destination
    for count, filename in enumerate(os.listdir(source_folder_path)):
        if filename.endswith('.jpeg'):  # Only consider PNG files
            # Create the new file name (e.g., 0.png, 1.png, ..., 99.png)
            new_filename = f'{count}.png'
            
            # Get the full path of the source file
            source_file = os.path.join(source_folder_path, filename)
            
            # Get the full path of the destination file
            destination_file = os.path.join(destination_folder_path, new_filename)
            
            # Copy the file from the source to the destination with the new name
            shutil.copy(source_file, destination_file)
            
            print(f"Copied {filename} to {new_filename} in folder {destination_folder_name}")

print("All PNG files copied and renamed successfully.")
