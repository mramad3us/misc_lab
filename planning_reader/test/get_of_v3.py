import pandas as pd

# Function to load planning data
def read_planning_data(file_path):
    planning_df = pd.read_excel(file_path, sheet_name='ANNEE 2023')
    pointage_df = pd.read_excel(file_path, sheet_name='POINTAGE')
    return planning_df, pointage_df

# Function to map project codes to OF codes
def get_of_code_mappings(pointage_df):
    of_code_mappings = {}
    for _, row in pointage_df.iterrows():
        project_code = row['Unnamed: 1']  # Adjust if the column title is different
        if pd.notna(project_code):
            project_code = ''.join(project_code.split())  # Remove spaces
            of_code_mappings[project_code] = {
                'INTERNE': row['Unnamed: 2'],  # Adjust if the column title is different
                'EXTERNE': row['Unnamed: 3']   # Adjust if the column title is different
            }
    return of_code_mappings

# Function to extract week data
def extract_week_data(planning_df, week_number, of_code_mappings):
    start_col_index = 273 + (week_number - 39) * 7  # This calculation may need adjustment
    end_col_index = start_col_index + 6
    samuel_murez_row_range = (546, 550)  # Adjust these indices based on where your name appears

    week_data = planning_df.iloc[samuel_murez_row_range[0]:samuel_murez_row_range[1], start_col_index:end_col_index]

    project_info = {}
    for col in week_data.columns:
        for row in week_data[col].dropna().unique():
            if ' ' in row:
                project_code, customer_name = row.split(' ', 1)
                of_codes = of_code_mappings.get(project_code, {'INTERNE': None, 'EXTERNE': None})
                project_info[project_code] = {
                    'Customer Name': customer_name,
                    'OF Codes': of_codes
                }
    return project_info

# Function to read the timesheet template
def read_timesheet_template(file_path, sheet_name):
    timesheet_df = pd.read_excel(file_path, sheet_name=sheet_name)
    return timesheet_df

# Function to pre-fill OF numbers in the timesheet
def prefill_of_numbers(timesheet_df, project_info, start_row_index):
    for project_code, details in project_info.items():
        of_code = details['OF Codes']['INTERNE'] if details['OF Codes']['INTERNE'] else details['OF Codes']['EXTERNE']
        # Assuming that the OF codes need to be filled in the first empty row within column J
        next_empty_row = timesheet_df.iloc[start_row_index:, 9].isnull().idxmax()  # Column J is at index 9
        timesheet_df.iat[next_empty_row, 9] = of_code  # Set the OF code in column J
    return timesheet_df

# Main function to run the script
def main():
    planning_file_path = 'Planning SAV.xlsx'  # Replace with your actual file path
    timesheet_file_path = 'Feuille_pointage_.xlsx'  # Replace with your actual file path
    sheet_name = 'S(45)'  # The sheet name for the timesheet

    # Load data and get mappings
    planning_df, pointage_df = read_planning_data(planning_file_path)
    of_code_mappings = get_of_code_mappings(pointage_df)

    # Prompt for week number
    week_number = int(input("Enter the week number: "))
    project_info = extract_week_data(planning_df, week_number, of_code_mappings)

    # Pre-fill timesheet
    timesheet_df = read_timesheet_template(timesheet_file_path, sheet_name)
    start_row_index = 10  # Row 11 is index 10 in zero-based indexing
    updated_timesheet_df = prefill_of_numbers(timesheet_df, project_info, start_row_index)

    # Save updated timesheet
    updated_timesheet_path = 'updated_timesheet.xlsx'
    updated_timesheet_df.to_excel(updated_timesheet_path, index=False)
    print(f"Updated timesheet saved to '{updated_timesheet_path}'.")

# Run the script
if __name__ == "__main__":
    main()