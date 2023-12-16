import pandas as pd

def read_planning_data(file_path):
    planning_df = pd.read_excel(file_path, sheet_name='ANNEE 2023')
    pointage_df = pd.read_excel(file_path, sheet_name='POINTAGE')
    return planning_df, pointage_df

def get_of_code_mappings(pointage_df):
    of_code_mappings = {}
    for _, row in pointage_df.iterrows():
        project_code = row['Unnamed: 1']
        if pd.notna(project_code):
            project_code = ''.join(project_code.split())  # Remove spaces
            of_code_mappings[project_code] = {
                'INTERNE': row['Unnamed: 2'],
                'EXTERNE': row['Unnamed: 3']
            }
    return of_code_mappings

def extract_week_data(planning_df, week_number, of_code_mappings):
    start_col_index = 273 + (week_number - 39) * 7
    end_col_index = start_col_index + 6
    samuel_murez_row_range = (546, 550)

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

def read_timesheet_template(file_path, sheet_name):
    timesheet_df = pd.read_excel(file_path, sheet_name=sheet_name)
    return timesheet_df

def prefill_of_numbers(timesheet_df, project_info, start_row):
    for project_code, details in project_info.items():
        of_code = details['OF Codes']['INTERNE'] if details['OF Codes']['INTERNE'] else details['OF Codes']['EXTERNE']
        # Assuming that the OF codes need to be filled in the first empty row within the same column.
        next_empty_row = timesheet_df[timesheet_df['OF'].isnull()].index.min()
        timesheet_df.at[next_empty_row, 'OF'] = of_code
    return timesheet_df

def main():
    planning_file_path = 'Planning SAV.xlsx'
    timesheet_file_path = 'Feuille_pointage_.xlsx'

    # Load data from the planning file
    planning_df, pointage_df = read_planning_data(planning_file_path)
    of_code_mappings = get_of_code_mappings(pointage_df)

    # Prompt user for a week number
    week_number = int(input("Enter the week number: "))
    project_info = extract_week_data(planning_df, week_number, of_code_mappings)

    # Load the timesheet template and pre-fill the OF numbers
    sheet_name = 'S(45)'  # The sheet name for the week's timesheet
    timesheet_df = read_timesheet_template(timesheet_file_path, sheet_name)
    start_row = 10  # The row where the OF numbers start
    updated_timesheet_df = prefill_of_numbers(timesheet_df, project_info, start_row)

    # Save the updated timesheet to a new file
    updated_timesheet_path = 'updated_timesheet.xlsx'
    updated_timesheet_df.to_excel(updated_timesheet_path, index=False)
    print(f"Updated timesheet saved to '{updated_timesheet_path}'.")

if __name__ == "__main__":
    main()