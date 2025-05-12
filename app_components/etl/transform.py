from db.db_conf import engine
"""
This module contains functions for transforming and cleaning data from various sources 
to prepare it for further analysis or storage in a database. The transformations include 
standardizing column names, cleaning invalid or incomplete data, mapping values to keys, 
and generating additional columns such as unique identifiers and email addresses.
Functions:
----------
1. generate_email(row):
    Generates an email address for a given row based on the customer's name or a predefined mapping.
2. transform_qarter():
    Includes operations such as renaming columns, removing invalid data, standardizing 
    phone numbers, and generating unique IDs.
3. assign_customer_key(code, cardcode_to_key):
    Maps a customer card code to a unique customer key using a predefined mapping.
4. assign_store_id(store_name, store_name_to_id):
    Maps a store name to a unique store ID using a predefined mapping.
5. transform_store(table_name, cardcode_to_key):
    Transforms and cleans data from a given store table. Includes operations such as 
    mapping customer keys, mapping store names to IDs, and cleaning address and date fields.
6. transform_dimdate(transformed_data):
    Generates a dimension table for dates based on the unique dates found in the transformed data. 
    Includes additional columns such as DateKey, Day, Month, Year, Quarter, and DayOfWeek.
Constants:
----------
1. CUSTOM_EMAILS:
    A dictionary mapping specific customer card codes to predefined email addresses.
2. STORE_NAME_MAPPING:
    A dictionary mapping raw store names to standardized store names.
Usage:
------
The module is designed to be executed as a script. It processes raw data tables, transforms them, 
and prepares them for loading into a database. The main entry point is the `__main__` block, 
which processes a list of raw tables and generates transformed data for each table.
"""

import pandas as pd
from loguru import logger
from faker import Faker

faker = Faker()

CUSTOM_EMAILS = {
    '2717041003249': 'narek_ghukasyan@edu.aua.am',
    '2717041003379': 'albert_simonyan@edu.aua.am',
    '2717041009432': 'gayane_hovsepyan@edu.aua.am',
    '2717041009876': 'mariam_mezhlumyan@edu.aua.am',
    '2717041011558': 'hayk_nalchajyan@edu.aua.am'
}

def generate_email(row):
    code = row['CustomerCardCode']
    if code in CUSTOM_EMAILS:
        return CUSTOM_EMAILS[code]
    else:
        name_slug = row['Name'].strip().lower().replace(' ', '.')[:30]
        return f"{name_slug}@example.com" if name_slug else faker.email()


def transform_qarter():
    """
    Cleans and transforms data from the "qarter" table into a standardized format.
    This function performs the following operations:
    1. Reads data from the "qarter" table using a SQL query.
    2. Renames columns from Russian to English for better readability.
    3. Drops the "DiscountCard" column as it is not required.
    4. Converts specific columns to string type for consistency.
    5. Removes rows with invalid or incomplete names (less than 5 characters).
    6. Filters out rows with invalid card codes (not exactly 13 characters long).
    7. Drops duplicate rows based on the "CustomerCardCode" column.
    8. Standardizes phone numbers by removing non-numeric characters.
    9. Moves phone numbers mistakenly stored in the "CustomerAddress" column to the "PhoneNumber" column
       and replaces the address with "Unknown".
    10. Replaces missing or invalid phone numbers with "Unknown".
    11. Replaces "None" values in the "CustomerAddress" column with "Unknown".
    12. Standardizes gender values, translating them from Russian to English and handling unknown values.
    13. Converts "BirthDate" and "RegistrationDate" columns to datetime format, handling errors gracefully.
    14. Removes rows with invalid dates, such as "RegistrationDate" earlier than "BirthDate" or before 2010.
    15. Adds a new "ID" column with unique identifiers starting from 1.
    16. Truncates string columns like "PhoneNumber" and "CustomerAddress" to a maximum length of 255 characters.
    17. Ensures "PhoneNumber" values are strings with a maximum length of 50 characters, replacing invalid values with "Unknown".
    18. Generates email addresses for each row using the `generate_email` function, based on customer names or predefined mappings.
    After cleaning and transforming the data, the function logs the number of cleaned rows.
    Note:
    - This function assumes the presence of a valid database connection (`engine`) and the `pandas` library.
    - The input data is expected to have specific column names in Russian.
    Returns:
        A cleaned and transformed DataFrame.
    """

    logger.info("Starting transformation of qarter...")

    discount_cards = pd.read_sql('SELECT * FROM qarter', engine)
    # discount_cards = discount_cards.loc[:, ~discount_cards.columns.str.contains('^Unnamed')]
    discount_cards = discount_cards.rename(columns={
    "Дисконтная карта": "DiscountCard",
    "Наименование": "Name",
    "Код карты": "CustomerCardCode",
    "Адрес покупателя": "CustomerAddress",
    "Карты телефон": "PhoneNumber",
    "Дата открытия": "RegistrationDate",
    "Дата рождения": "BirthDate",
    "Пол": "Gender"})

    discount_cards = discount_cards.drop(columns=["DiscountCard"])

    # Converting columns to string type
    discount_cards['Name'] = discount_cards['Name'].astype(str)
    discount_cards['CustomerCardCode'] = discount_cards['CustomerCardCode'].astype(str)
    discount_cards['CustomerAddress'] = discount_cards['CustomerAddress'].astype(str)
    discount_cards['PhoneNumber'] = discount_cards['PhoneNumber'].astype(str)
    discount_cards['Gender'] = discount_cards['Gender'].astype(str)


    # Getting rid of invalid names
    df_no_name = discount_cards[discount_cards['Name'].fillna('').str.len() < 5]
    discount_cards = discount_cards[~discount_cards.index.isin(df_no_name.index)]
    discount_cards['Name'] = discount_cards['Name'].str.slice(0, 50)

    # Getting rid of invalid card codes
    df_invalid_cardcode = discount_cards[discount_cards['CustomerCardCode'].astype(str).str.len() != 13]
    discount_cards = discount_cards[~discount_cards.index.isin(df_invalid_cardcode.index)]

    # Dropping duplicate rows
    discount_cards = discount_cards.drop_duplicates(subset=['CustomerCardCode'])

    # Standardizing phone numbers
    discount_cards['PhoneNumber'] = discount_cards['PhoneNumber'].apply(
        lambda x: ''.join(filter(str.isdigit, x)) if pd.notnull(x) else x
    )
    mask_phone_in_address = discount_cards['CustomerAddress'].str.match(r'^(\+?\d{5,})', na=False)

    # Move Address to PhoneNumber and replace address with 'Unknown'
    discount_cards.loc[mask_phone_in_address, 'PhoneNumber'] = discount_cards.loc[mask_phone_in_address, 'CustomerAddress']
    discount_cards.loc[mask_phone_in_address, 'CustomerAddress'] = 'Unknown'

    # Replace missing phone numbers with 'Unknown'
    discount_cards['PhoneNumber'] = discount_cards['PhoneNumber'].replace('', 'Unknown')
    discount_cards['PhoneNumber'] = discount_cards['PhoneNumber'].replace('None', 'Unknown')

    # Changing 'None' to 'Unknown' in CustomerAddress
    discount_cards['CustomerAddress'] = discount_cards['CustomerAddress'].replace('None', 'Unknown')


    # Standardizing unknown gender values and translating to English
    discount_cards['Gender'] = discount_cards['Gender'].fillna("unknown")
    discount_cards['Gender'] = discount_cards['Gender'].replace({
        "Женский": "Female",
        "Мужской": "Male"
    })

    # Changing the data type of BirthDate, RegistrationDate to datetime
    discount_cards['BirthDate'] = pd.to_datetime(discount_cards['BirthDate'], errors='coerce', dayfirst=True)
    discount_cards['RegistrationDate'] = pd.to_datetime(discount_cards['RegistrationDate'], errors='coerce', dayfirst=True)

    # Removing rows with invalid dates
    discount_cards.loc[(discount_cards['RegistrationDate'] < discount_cards['BirthDate']) | (discount_cards['RegistrationDate'].dt.year < 2010),
                       'RegistrationDate'] = pd.NaT
    discount_cards.loc[discount_cards['BirthDate'].dt.year < 1900, 'BirthDate'] = pd.NaT
    

    # Adding an ID column starting from 1
    discount_cards = discount_cards.reset_index(drop=True)
    
    discount_cards['ID'] = discount_cards.index + 1
    
    # Truncating string columns to a maximum length of 255 characters
    discount_cards['PhoneNumber'] = discount_cards['PhoneNumber'].str.slice(0, 255)
    discount_cards['CustomerAddress'] = discount_cards['CustomerAddress'].str.slice(0, 255)

    # Ensuring PhoneNumber is a string and has a maximum length of 50 characters, else just drop it altogether
    discount_cards['PhoneNumber'] = discount_cards['PhoneNumber'].apply(
    lambda x: x if pd.notnull(x) and len(str(x)) <= 50 else 'Unknown')

    discount_cards['Email'] = discount_cards.apply(generate_email, axis=1)    
    logger.info(f"Done! Cleaned {len(discount_cards)} rows.")
    return discount_cards

STORE_NAME_MAPPING = {
    'Մասիվ': 'Մասիվ 1',
    'Ագորա_խանութ': 'Մասիվ 5',
    '7Մասիվ': 'Մասիվ 7',
    'Ագորա ցենտր': 'Բանգլադեշ',
    'Մալաթիա': 'Մալաթիա',
    'Քանաքեռ': 'Քանաքեռ',
    'Ռայկոմ': 'Ռայկոմ',
    'Շենգավիթ': 'Շենգավիթ'
}

def assign_customer_key(code, cardcode_to_key):
    if code == '0' or pd.isna(code):
        return 0
    return cardcode_to_key.get(code, 0)

def assign_store_id(store_name, store_name_to_id):
    return store_name_to_id.get(store_name, None)

def transform_store(table_name, cardcode_to_key):
    """
    Transforms and processes data from a specified table and maps it to the required format.
    This function performs the following operations:
    - Reads data from the specified table in the database.
    - Drops unnecessary columns if they exist.
    - Cleans and standardizes column values, including handling missing data.
    - Renames columns for consistency.
    - Maps customer codes to customer keys using a provided mapping.
    - Maps store names to store IDs using data from the "DimStore" table.
    - Reports any store names that could not be mapped to a StoreID.
    Args:
        table_name (str): The name of the table to read data from.
        cardcode_to_key (dict): A dictionary mapping card codes to customer keys.
    Returns:
        pandas.DataFrame: A transformed DataFrame with cleaned and mapped data.
    """

    df = pd.read_sql(f'SELECT * FROM "{table_name}"', engine)

    # Drop unnecessary columns (ignore if they don't exist)
    df = df.drop(columns=['Discount Card', 'Unnamed: 1', 'Unnamed: 2', 
                          'Unnamed: 4', 'Phone', 'Date Created', 'Birthday', 'Gender'], errors='ignore')

    df['Name Surname'] = df['Name Surname'].fillna("No Cardholder")  
    df = df.rename(columns={'Adresss': 'Adress', 'Cardcode': 'Code'})

    # Fill missing codes with 0 and ensure string type
    df['Code'] = (df['Code'].fillna(0).astype(str).str.strip().str.replace(r"\.0$", "", regex=True))
    # Fill missing Store with empty string and strip whitespace
    df['Store'] = df['Store'].fillna('').astype(str).str.strip()

    # Replace using the STORE_NAME_MAPPING
    df['Store'] = df['Store'].replace(STORE_NAME_MAPPING)

    # Address cleanup
    df['Adress'] = df['Adress'].fillna("Unknown").astype(str)

    # Convert types
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
    df['Name Surname'] = df['Name Surname'].astype(str)
    df['Money Spent'] = df['Money Spent'].astype(float)

    # --- CUSTOMERKEY MAPPING ---
    df['CustomerKey'] = df['Code'].apply(lambda code: assign_customer_key(code, cardcode_to_key))

    # --- STOREKEY MAPPING ---
    # Get DimStore names and IDs
    store_df = pd.read_sql('SELECT * FROM "DimStore";', engine)
    store_name_to_id = dict(zip(store_df['Name'].str.strip(), store_df['StoreID']))

    # Map store names to StoreIDs
    df['StoreID'] = df['Store'].apply(lambda name: assign_store_id(name, store_name_to_id))

    # Report missing store mappings
    if df['StoreID'].isnull().any():
        missing = df[df['StoreID'].isnull()]['Store'].unique()
    df = df.drop(columns=['Store'])

    return df


def transform_dimdate(transformed_data):
    """
    Transforms a collection of dataframes containing date information into a 
    dimension table for dates (dim_date).
    Args:
        transformed_data (dict): A dictionary where the values are pandas DataFrames 
                                 containing a 'Date' column.
    Returns:
        pandas.DataFrame: A DataFrame representing the date dimension table with the following columns:
            - Date: The unique dates.
            - DateKey: An integer key in the format YYYYMMDD.
            - Day: The day of the month.
            - Month: The month of the year.
            - Year: The year.
            - Quarter: The quarter of the year (1-4).
            - DayOfWeek: The day of the week (1=Monday, 7=Sunday).
            - DayName: The name of the day (e.g., "Monday").
            - MonthName: The name of the month (e.g., "January").
    """

    all_dates = pd.concat([df['Date'] for df in transformed_data.values()])
    unique_dates = pd.to_datetime(all_dates.dropna().unique())

    dim_date = pd.DataFrame({'Date': unique_dates})
    dim_date['DateKey'] = dim_date['Date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['Day'] = dim_date['Date'].dt.day
    dim_date['Month'] = dim_date['Date'].dt.month
    dim_date['Year'] = dim_date['Date'].dt.year
    dim_date['Quarter'] = dim_date['Date'].dt.quarter
    dim_date['DayOfWeek'] = dim_date['Date'].dt.dayofweek + 1  # Monday=1
    dim_date['DayName'] = dim_date['Date'].dt.day_name()
    dim_date['MonthName'] = dim_date['Date'].dt.month_name()

    dim_date = dim_date.sort_values('Date')
    dim_date = dim_date.drop_duplicates(subset=['DateKey'])

    return dim_date

if __name__ == "__main__":
    """
    Main execution block for transforming raw data tables into cleaned and standardized formats.
    This block performs the following steps:
    1. Defines a list of raw table names to be processed.
    2. Transforms the "qarter" table using the `transform_qarter` function and generates a mapping
        of customer card codes to unique customer keys.
    3. Iterates through each raw table in the list, transforms it using the `transform_store` function,
        and stores the resulting DataFrame in the `transformed_data` dictionary.
    4. Logs the progress and completion of each table transformation, including the number of rows processed.
    """
    raw_tables = ['1masiv', '5rd_masiv', '7rd_masiv', 
    'agoracenter', 'malatia', 'qanaqer', 
    'raykom', 'shengavit']

    transformed_data = {}

    discount_cards = transform_qarter()
    cardcode_to_key = dict(zip(discount_cards['CustomerCardCode'], discount_cards['ID']))

    for table in raw_tables:
        logger.info(f"Transforming table: {table}")
        df = transform_store(table, cardcode_to_key)
        transformed_data[table] = df
        logger.info(f"Finished transforming {table}. Rows: {len(df)}\n")