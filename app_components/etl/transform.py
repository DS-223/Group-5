from db.db_conf import engine
import pandas as pd



print("Starting transformation of qarter...")

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
    
    print(f"Done! Cleaned {len(discount_cards)} rows.")
    return discount_cards


def transform_store(table_name):
    df = pd.read_sql(f'SELECT * FROM {table_name}', engine)

    df = df.drop(columns=['Discount Card', 'Unnamed: 1', 'Unnamed: 2', 
                          'Unnamed: 4', 'Phone', 'Date Created', 'Birthday', 'Gender'], errors='ignore')

    df['Name Surname'] = df['Name Surname'].fillna("No Cardholder")  
    df = df.rename(columns={'Adresss': 'Adress', 'Cardcode': 'Code'})

    # If Code missing, set to 0
    df['Code'] = df['Code'].apply(lambda x: x if pd.notna(x) else 0)
    df['Adress'] = df['Adress'].fillna("Unknown")

    # --- DATA TYPES ---
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
    df['Name Surname'] = df['Name Surname'].astype(str)
    df['Code'] = df['Code'].astype(str)  # must be string for matching
    df['Adress'] = df['Adress'].astype(str)
    df['Money Spent'] = df['Money Spent'].astype(float)

    # --- CUSTOMERKEY MAPPING ---

    # Get the dimension table only once per call
    dim_customer = transform_qarter()
    cardcode_to_key = dict(zip(dim_customer['CustomerCardCode'], dim_customer['ID']))

    def assign_customer_key(code):
        if code == '0' or pd.isna(code):
            return 0
        return cardcode_to_key.get(code, 0)

    df['CustomerKey'] = df['Code'].apply(assign_customer_key)

    return df

if __name__ == "__main__":
    transform_qarter()
    malatia_df = transform_store('shengavit')
    print(malatia_df.head())
