import pandas as pd

def read_planning_data(file_path):
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name='ANNEE 2023')  # Adjust the sheet name if needed
    return df

def extract_week_data(df, week_number):
    # Convert week number to column range
    # Adjust the calculation based on the week number to column index mapping we previously determined
    start_col_index = 273 + (week_number - 39) * 7
    end_col_index = start_col_index + 6

    # Define the row range for Samuel Murez
    # Adjusted to include a broader range for capturing multiple entries
    start_row_index = 546 - 10  # Expanding the range to capture more rows
    end_row_index = 550 + 10

    # Extract data for the specified week
    week_data = df.iloc[start_row_index:end_row_index, start_col_index:end_col_index]

    # Extract project codes and customer names
    project_info = {}
    for col in week_data.columns:
        for row in week_data[col].dropna().unique():
            if ' ' in row:  # Assuming the format is 'ProjectCode CustomerName'
                project_code, customer_name = row.split(' ', 1)
                project_info[project_code] = customer_name

    return project_info

def main():
    file_path = 'path_to_your_excel_file.xlsx'  # Replace with your actual file path
    df = read_planning_data(file_path)

    # Prompt user for a week number
    week_number = int(input("Enter the week number: "))

    # Extract and display project information
    project_info = extract_week_data(df, week_number)
    print("Project Codes and Customer Names for Week", week_number, ":", project_info)

if __name__ == "__main__":
    main()