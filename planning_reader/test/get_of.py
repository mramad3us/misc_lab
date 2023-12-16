import pandas as pd

def read_planning_data(file_path):
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name='ANNEE 2023')
    return df

def extract_week_data(df, week_number):
    # Convert week number to column range based on previous analysis
    start_col_index = 273 + (week_number - 39) * 7
    end_col_index = start_col_index + 6

    # Define the specific row range for Samuel Murez's data
    # Adjust the row range to exactly match the rows relevant to your tasks
    samuel_murez_row_range = (546, 550)  # Adjust this range based on actual data

    # Extract data for the specified week and rows
    week_data = df.iloc[samuel_murez_row_range[0]:samuel_murez_row_range[1], start_col_index:end_col_index]

    # Extract project codes and customer names
    project_info = {}
    for col in week_data.columns:
        for row in week_data[col].dropna().unique():
            if ' ' in row:  # Assuming the format 'ProjectCode CustomerName'
                project_code, customer_name = row.split(' ', 1)
                project_info[project_code] = customer_name

    return project_info

def main():
    file_path = 'Planning SAV.xlsx'  # Replace with your actual file path
    df = read_planning_data(file_path)

    # Prompt user for a week number
    week_number = int(input("Enter the week number: "))

    # Extract and display project information
    project_info = extract_week_data(df, week_number)
    print("Project Codes and Customer Names for Week", week_number, ":", project_info)

if __name__ == "__main__":
    main()