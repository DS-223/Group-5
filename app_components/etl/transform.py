from db.db_conf import engine
import pandas as pd
from loguru import logger

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
    7. Standardizes phone numbers by removing non-numeric characters.
    8. Moves phone numbers mistakenly stored in the "CustomerAddress" column to the "PhoneNumber" column
       and replaces the address with "Unknown".
    9. Replaces "None" values in the "CustomerAddress" column with "Unknown".
    10. Standardizes gender values, translating them from Russian to English and handling unknown values.
    11. Converts "BirthDate" and "RegistrationDate" columns to datetime format, handling errors gracefully.
    12. Adds a new "ID" column with unique identifiers starting from 1.
    After cleaning and transforming the data, the function prints the number of cleaned rows.
    Note:
    - This function assumes the presence of a valid database connection (`engine`) and the `pandas` library.
    - The input data is expected to have specific column names in Russian.
    Returns:
        None
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
    df = pd.read_sql(f'SELECT * FROM "{table_name}"', engine)

    # Drop unnecessary columns (ignore if they don't exist)
    df = df.drop(columns=['Discount Card', 'Unnamed: 1', 'Unnamed: 2', 
                          'Unnamed: 4', 'Phone', 'Date Created', 'Birthday', 'Gender'], errors='ignore')

    df['Name Surname'] = df['Name Surname'].fillna("No Cardholder")  
    df = df.rename(columns={'Adresss': 'Adress', 'Cardcode': 'Code'})

    # Fill missing codes with 0 and ensure string type
    df['Code'] = df['Code'].fillna(0).astype(str).str.strip()

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
        logger.warning(f"These store names could not be mapped to StoreID: {missing}")

    df = df.drop(columns=['Store'])

    return df


def transform_dimdate(transformed_data):
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