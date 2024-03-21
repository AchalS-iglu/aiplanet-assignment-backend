import os
import PyPDF4
import datetime
import random
import string

class PDFFile:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        # Sets the last accessed time to the current time
        self.last_accessed = datetime.datetime.now()
        # Set the file name
        self.file_name = file_path.split('/')[-1]
    
    def remove_file(self):
        # Remove the file from the directory
        os.remove(self.file_path)
    
    def extract_text(self, pdfReader):
        # Reset the last accessed time
        self.last_accessed = datetime.datetime.now()
        # Extract the text from the pdf
        return [pdfReader.getPage(i).extractText() for i in range(pdfReader.numPages)]
    

class _PDFHandler:
    def __init__(self, directory_path):
        # Set the directory path
        self.directory_path = directory_path
        # Get all the files in the directory and make their objects
        self.files = {}
        for file in os.listdir(self.directory_path):
            self.files[file] = PDFFile(os.path.join(self.directory_path, file))
        # Get the pdf reader object
        self.pdfReader = PyPDF4.PdfFileReader
    
    def add_file(self, bytes, file_name):
        # Check for duplicates
        if file_name in self.files:
            # Generate a random string of 5 characters
            random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
            # Add the random string to the file name
            file_name = f'{random_string}_{file_name}'
        # Create a new file in the directory
        with open(os.path.join(self.directory_path, f"{file_name}.pdf"), 'wb') as file:
            file.write(bytes)
        # Create a new file object
        self.files[file_name] = PDFFile(os.path.join(self.directory_path, file_name))
        return file_name
    
    def remove_file(self, file_name):
        # Get the file object
        file = next(file for file in self.files if file.id == file_name)
        # Remove the file from the directory
        file.remove_file()
        # Remove the file object
        del self.files[file_name]
    
    def get_file(self, file_name):
        # Get the file object
        file = next(file for file in self.files if file.id == file_name)
        # Return the file object
        return file

# Check if pdfs dir exists
if not os.path.exists('pdfs'):
    # Create the directory
    os.mkdir('pdfs')
# Create a new PDFHandler object
PDFHandler = _PDFHandler('pdfs')