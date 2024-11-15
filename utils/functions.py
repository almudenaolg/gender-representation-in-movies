## CLEANING DATA

# Function to unify and simplify column names
def standardize_column_names(df):
    """
    Standardizes column names by converting them to lowercase and 
    replacing spaces with underscores.

    Parameters:
    df (pd.DataFrame): The DataFrame whose columns are to be standardized.

    Returns:
    pd.DataFrame: The DataFrame with standardized column names.
    """
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df

# Function to filter movies released from 1990 to 2024
def filter_by_year(df, start_year=1990, end_year=2024):
    """
    Filters the dataframe for movies released between start_year and end_year.
    
    Parameters:
    df (DataFrame): The dataframe containing movie data.
    start_year (int): The starting year for the filter.
    end_year (int): The ending year for the filter.
    
    Returns:
    DataFrame: A filtered dataframe containing movies between the specified years.
    """
    # Filter for rows where `year` is between the dates specified
    df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    return df

# Function to fill missing values in `certificate` with a placeholder
def fill_certificate(df):
    df['certificate'] = df['certificate'].fillna('Unrated')
    return df

# Function to drop rows with missing values in relevant columns
def drop_null_year(df):
    df = df.dropna(subset=['year'])
    return df

# Main function to handle all NaN values in df_movies
def handle_missing_values(df):
    fill_certificate(df)
    drop_null_year(df)
    return df

# Function to add each person id to cast, director and writter dataframes
def relate_person_id(df, person_column, df_persongender):
    """
    This function merges a dataframe with the `df_persongender` dataframe 
    to add `person_id` based on the person's name, then returns a simplified dataframe.
    
    Parameters:
    - df: DataFrame to merge, containing a movie ID and a person name column.
    - person_column: The name of the column in `df` with person names (e.g., 'director', 'cast_member', 'writer').
    - df_persongender: DataFrame containing `person_name` and `person_id` columns.
    
    Returns:
    - DataFrame containing `movie_id` and `person_id` columns.
    """
    merged_df = df.merge(
        df_persongender[['person_name', 'person_id']], 
        left_on=person_column, 
        right_on='person_name', 
        how='left'
    )
    return merged_df[['movie_id', 'person_id']]


## GENDER EXTRACTION

# Function to predict gender using `gender-guesser`
def guess_gender_with_library(name):
    """
    Predicts the gender of a person based on their name using `gender-guesser`.
    
    Parameters:
    name (str): The name of the person to predict gender for.
    
    Returns:
    str: The predicted gender of the person, either "Male" or "Female".
    """
    if isinstance(name, str):
        first_name = name.split()[0]  # To select the first name
        gender_guess = d.get_gender(first_name)
        
        if gender_guess in ["male", "mostly_male"]:
            return "Male"
        elif gender_guess in ["female", "mostly_female"]:
            return "Female"
    return "Unknown"  # Return "Unknown" for non-string or unidentified names

# Function to predict gender using Genderize.io API with simple error handling
def guess_gender_with_api(name):
    """
    Predicts the gender of a person based on their name using Genderize.io API.
    
    Parameters:
    name (str): The name of the person to predict gender for.
    
    Returns:
    str: The predicted gender of the person, either "Male" or "Female".
    """
    if isinstance(name, str):
        first_name = name.split()[0]
        try:
            response = requests.get(f"https://api.genderize.io/?name={first_name}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'gender' in data and data['gender']:
                    return data['gender'].capitalize()  # Returns 'Male' or 'Female'
        except requests.exceptions.RequestException:
            pass  # If there's a connection issue, return "Unknown"
    return "Unknown"


## CHECK DATA

# Function to print dataframe details: first few rows and data types
def print_df_info(df, name):
    print(f"\nDataframe: {name}")
    print("First few rows:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
    print("-" * 40)