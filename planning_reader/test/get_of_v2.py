import pandas as pd

def read_planning_data(file_path):
    # Load the 'ANNEE 2023' sheet and the 'POINTAGE' sheet
    planning_df = pd.read_excel(file_path, sheet_name='ANNEE 2023')
    pointage_df = pd.read_excel(file_path, sheet_name='POINTAGE')
    return planning_df, pointage_df

def get_of_code_mappings(pointage_df):
    # Map project codes to their 'INTERNE' and 'EXTERNE' OF codes, trimming spaces
    of_code_mappings = {}
    for _, row in pointage_df.iterrows():
        project_code = row['Unnamed: 1']
        if pd.notna(project_code):
            # Remove any spaces to match the project code format
            project_code = ''.join(project_code.split())
            of_code_mappings[project_code] = {
                'INTERNE': row['Unnamed: 2'],
                'EXTERNE': row['Unnamed: 3']
            }
    return of_code_mappings

# The rest of the script remains the same

def main():
    file_path = 'Planning SAV.xlsx'  # Replace with your actual file path
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