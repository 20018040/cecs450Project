"""
    CSULB Student Admission Data
    https://www.csulb.edu/institutional-research-analytics/student-admission-data

    First-Time Freshmen Vs Transfer Students
    Demographics

    FTF Head Count by Race/Ethnicity as well as College and Department
    at time of application viewable by Sex, First-Generation and Minority Status.

    Transfer Head Count by Race/Ethnicity as well as College and Department
    at time of application viewable Sex, First-Generation and Minority Status.
"""

# Comparative Analysis: Compare the characteristics of first-time freshmen with transfer students.

import csv
import os   # for JOINing path folder and file
import pandas as pd
import plotly.graph_objects as go


# Folder where your CSV files are located
file_folder = r'C:\Users\obliv\Desktop\CECS 450 Project\Demographics'  # Use Raw Strings: Prefix your string with r to make it a raw string, which tells Python to ignore escape characters:

# List of your CSV file names
file_names = ['SP 23 FTF Applicant by Sex.csv',
              'SP 23 FTF Applicant by Sex.csv', 'SP 23 TRAN Applicant by Sex.csv',
              'FA 22 FTF Applicant by Sex.csv', 'FA 22 TRAN Applicant by Sex.csv',

              'SP 22 FTF Applicant by Sex.csv', 'SP 22 TRAN Applicant by Sex.csv',
              'FA 21 FTF Applicant by Sex.csv', 'FA 21 TRAN Applicant by Sex.csv',

              'SP 21 FTF Applicant by Sex.csv', 'SP 21 TRAN Applicant by Sex.csv',
              'FA 20 FTF Applicant by Sex.csv', 'FA 20 TRAN Applicant by Sex.csv']

print("SP-Spring | FA-Fall | FTF-First time Freshmen | TRAN-Transfer Applicants\n")

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

# Total applicants per semester
def total_app_per_semester():
    totals = []
    labels = []
    total_applicants = 0

    # Loop through each file name
    for file_name in file_names:
        # Construct the full file path
        file_path = os.path.join(file_folder, file_name)

        # Read the CSV file
        df = pd.read_csv(file_path, encoding='utf-16', delimiter='\t')

        # Assuming the total number of applicants are in the last row, excluding the first cell
        # Convert all to integers after removing commas, and sum them up
        total_for_file = df.iloc[-1, 1:].apply(lambda x: int(x.replace(',', ''))).sum()

        total_applicants += total_for_file
        print(f"Total applicants in {file_name}: {total_for_file}\n")

        totals.append(total_for_file)
        labels.append(file_name[:-4])  # Remove '.csv' from the file name for labeling

    labels = ["SP 23 Freshmen", "SP 23 Transfer", "FA 22 Freshmen", "FA 22 Transfer"]
    print(f"\nOverall total applicants across all semesters: {total_applicants}")

    # Create a bar chart
    fig = go.Figure(data=[go.Bar(x=labels, y=totals)])
    fig.update_layout(title='Total Number of Applicants by File',
                      xaxis_title='File',
                      yaxis_title='Total Applicants')

    # Show the plot
    fig.show()

def total_by_gender():
    # Initialize a dictionary to hold the totals for each gender/sex
    totals_by_gender = {}

    for file_name in file_names:
        file_path = os.path.join(file_folder, file_name)

        # Read the CSV file
        df = pd.read_csv(file_path, encoding='utf-16', delimiter='\t')

        # Assuming gender/sex categories are in the columns starting from the second column
        genders = df.columns[1:]

        # Sum up the totals for each gender/sex, skipping the first two rows
        for gender in genders:
            if gender not in totals_by_gender:
                totals_by_gender[gender] = 0
            # Sum the values from the third row onwards, converting to integers
            total_for_gender = df[gender][2:].apply(
                lambda x: int(x.replace(',', '')) if isinstance(x, str) else x).sum()
            totals_by_gender[gender] += total_for_gender

    # Prepare data for plotting
    labels = list(totals_by_gender.keys())
    totals = [totals_by_gender[gender] for gender in labels]

    labels = ['Male', 'Female', 'Other']

    # Create a bar chart
    fig = go.Figure(data=[go.Bar(x=labels, y=totals)])
    fig.update_layout(title='Total Number of Applicants by Gender/Sex',
                      xaxis_title='Gender/Sex',
                      yaxis_title='Total Applicants')

    # Show the plot
    fig.show()

# Total applicants per semester
def applicants_gender_grouped_by_semester():
    all_data = []

    for file_name in file_names:
        file_path = os.path.join(file_folder, file_name)
        df = pd.read_csv(file_path, encoding='utf-16', delimiter='\t', header=None)

        # Extract the row with actual counts (now assumed to be the fourth row)
        counts_row = df.iloc[3]
        counts_row[0] = file_name[:-4]  # Replace the first cell with the semester/file name

        # Check if the 'Unknown' column is missing and add it if necessary
        if len(counts_row) == 4 and counts_row[3] == '':  # Assuming columns are ['Semester', 'Female', 'Male', 'Unknown']
            counts_row[3] = 0  # Add a default value for 'Unknown'

        all_data.append(counts_row)

    # Concatenate all data into a single DataFrame
    concatenated_df = pd.DataFrame(all_data)

    # Set the first row as header
    concatenated_df.columns = ['Semester', 'Female', 'Male', 'Unknown']
    concatenated_df = concatenated_df[1:]

    # Convert columns to numeric
    for col in concatenated_df.columns[1:]:  # Exclude the 'Semester' column
        concatenated_df[col] = pd.to_numeric(
            concatenated_df[col].astype(str).str.replace(',', '').str.extract('(\d+)', expand=False), errors='coerce')

    # Print the DataFrame after conversion to check
    print(concatenated_df)

    # Group by 'Semester' and sum
    aggregated_data = concatenated_df.groupby('Semester').sum()

    # Print the aggregated data to check
    print(aggregated_data)

    # Prepare data for plotting
    colors = {'Female': 'red', 'Male': 'blue', 'Unknown': 'gray'}

    # Create traces for each gender
    fig = go.Figure()
    for gender in aggregated_data.columns:
        fig.add_trace(go.Bar(
            x=aggregated_data.index,
            y=aggregated_data[gender],
            name=gender,
            marker_color=colors.get(gender, 'black')  # Default to black if gender not found
        ))

    # Update layout
    fig.update_layout(
        barmode='group',
        title='Total Number of Applicants by Gender/Sex per Semester',
        xaxis_title='Semester',
        yaxis_title='Total Applicants',
        legend_title='Gender/Sex'
    )

    # Show the plot
    fig.show()


#read_file()
#total_app_per_semester()
#total_by_gender()
applicants_gender_grouped_by_semester()

