import csv
import os   # for JOINing path folder and file
import pandas as pd
import plotly.graph_objects as go


# Folder where your CSV files are located
file_folder = r'C:\Users\obliv\Desktop\CECS 450 Project\RaceEthnicity'  # Use Raw Strings: Prefix your string with r to make it a raw string, which tells Python to ignore escape characters:

# List of your CSV file names
file_names = ['FA 22 FTF ACAD.csv']

def read_file():
    # Loop through each file name
    for file_name in file_names:
        # Construct the full file path
        file_path = os.path.join(file_folder, file_name)

        try:
            # Open and read the CSV file
            with open(file_path, mode='r', encoding='utf-8') as file:
                # If you're printing out the rows of your CSV file and see something like 't' in front of the data use delimiter
                csv_reader = csv.reader(file, delimiter='\t')

                # Optionally, read the header
                header = next(csv_reader)
                print(f"Header for {file_name} with utf-8 encoding: {header}")

                # Read each row in the CSV file
                for row in csv_reader:
                    print(row)

        except UnicodeDecodeError:
            # Trying a different encoding like utf-16
            with open(file_path, mode='r', encoding='utf-16') as file:
                # If you're printing out the rows of your CSV file and see something like 't' in front of the data use delimiter
                csv_reader = csv.reader(file, delimiter='\t')

                # Optionally, read the header
                header = next(csv_reader)
                print(f"Header for {file_name} with utf-16 encoding: {header[1]}")

                # Read each row in the CSV file
                for row in csv_reader:
                    print(row)

        print(f"Finished reading {file_name}\n")

read_file()