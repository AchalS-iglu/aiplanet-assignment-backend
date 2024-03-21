import os
import datetime
import random
import string
import fitz  # PyMuPDF    

class _PDFHandler:
    def __init__(self, directory_path):
        # Set the directory path
        self.directory_path = directory_path
        # Get all the files in the directory and make their objects
        self.files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.pdf')]
    
    def add_file(self, bytes, file_name):
        # Check for duplicates
        if file_name in self.files:
            # Generate a random string of 5 characters
            random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
            # Add the random string to the file name
            file_name = f'{random_string}_{file_name}'
        # Create a new file in the directory
        file_path = os.path.join(self.directory_path, f"{file_name}.pdf")
        with open(file_path, 'wb') as file:
            file.write(bytes)
        # Add the file to the list
        self.files.append(file_path)
        return file_name
    
    def remove_file(self, file_name):
        # Get the file object
        file = os.path.join(self.directory_path, file_name)
        if file:
            # Remove the file from the directory
            os.remove(file)
            # Remove the file from list
            self.files.remove(file)
        else:
            raise FileNotFoundError(f"File {file_name} not found")
    
    def get_file(self, file_name):
        file = next((file for file in self.files if file.endswith(file_name)), None)
        if file:
            # Return the file object
            return file
        else:
            raise FileNotFoundError(f"File {file_name} not found")

# Check if pdfs dir exists
if not os.path.exists('pdfs'):
    # Create the directory
    os.mkdir('pdfs')
# Create a new PDFHandler object
PDFHandler = _PDFHandler('pdfs')
