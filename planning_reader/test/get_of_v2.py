import pandas as pd

def read_planning_data(file_path):
    # Load the 'ANNEE 2023' sheet
    planning_df = pd.read_excel(file_path, sheet_name='ANNEE 2023')
    # Load the 'POINTAGE' sheet
    pointage_df = pd.read_excel(file_path, sheet_name='POINTAGE')
    return planning_df, pointage_df

def get_of_code_mappings(pointage_df):
    # Create a dictionary to map project codes to their OF codes (both 'INTERNE' and 'EXTERNE')
    of_code_mappings = {}
    for _, row in pointage_df.iterrows():
        affair_code = row['AFFAIRE']
        if pd.notna(affair_code):
            of_code_mappings[affair_code] = {
                'INTERNE': row['INTERNE'],
                'EXTERNE': row['EXTERNE']
            }
    return of_code_mappings

def extract_week_data(df, week_number, of_code_mappings):
    # Convert week number to column range
    start_col_index = 273 + (week_number - 39) * 7
    end_col_index = start_col_index + 6

    # Define the specific row range for Samuel Murez's data
    samuel_murez_row_range = (546, 550)

    # Extract data for the specified week and rows
    week_data = df.iloc[samuel_murez_row_range[0]:samuel_murez_row_range[1], start_col_index:end_col_index]

    # Extract project codes, customer names, and OF codes
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

def main():
    file_path = 'path_to_your_excel_file.xlsx'  # Replace with your actual file path
    planning_df, pointage_df = read_planning_data(file_path)

    # Get the OF code mappings from the 'POINTAGE' sheet
    of_code_mappings = get_of_code_mappings(pointage_df)

    # Prompt user for a week number
    week_number = int(input("Enter the week number: "))

    # Extract and display project information
    project_info = extract_week_data(planning_df, week_number, of_code_mappings)
    print("Project Codes, Customer Names, and OF Codes for Week", week_number, ":", project_info)

if __name__ == "__main__":
    main()