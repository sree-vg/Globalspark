import pandas as pd
import os

# Load datasets
customers = pd.read_csv(r'C:\Global\DataSet\Customers.csv', encoding='latin')
products = pd.read_csv(r'C:\Global\DataSet\Products.csv', encoding='latin')
sales = pd.read_csv(r'C:\Global\DataSet\Sales.csv', encoding='latin')
stores = pd.read_csv(r'C:\Global\DataSet\Stores.csv', encoding='latin')
currency = pd.read_csv(r'C:\Global\DataSet\Exchange_Rates.csv', encoding='latin')

# Step 1: Handle missing 'State Code' based on 'State'
state_to_code = {
    'California': 'CA',
    'Texas': 'TX',
    'Florida': 'FL',
    'New York': 'NY',
    'Napoli': 'NA',
    'Italy': 'IT'
}

# Update 'State Code' based on 'State'
customers['State Code'] = customers.apply(
    lambda row: state_to_code.get(row['State'], row['State Code']), axis=1
)

# Handle missing values in 'sales' dataset
sales['Order Date'] = pd.to_datetime(sales['Order Date'])
sales['Delivery Date'] = pd.to_datetime(sales['Delivery Date'], errors='coerce')  # Coerce invalid dates to NaT

# Calculate median delivery time and fill missing delivery dates
median_delivery_time = (sales['Delivery Date'] - sales['Order Date']).median()
sales['Delivery Date'] = sales['Delivery Date'].fillna(sales['Order Date'] + median_delivery_time)

stores['Open Date'] = pd.to_datetime(stores['Open Date'], errors='coerce')

# Handle missing values in 'stores' dataset
stores['Square Meters'] = stores['Square Meters'].fillna(stores['Square Meters'].median())

# Convert 'Birthday' column to datetime format in 'customers' dataset
customers['Birthday'] = pd.to_datetime(customers['Birthday'], errors='coerce')

# Convert 'Unit Cost USD' and 'Unit Price USD' to numeric by removing dollar signs and converting to float
products['Unit Cost USD'] = products['Unit Cost USD'].replace('[\$,]', '', regex=True).astype(float)
products['Unit Price USD'] = products['Unit Price USD'].replace('[\$,]', '', regex=True).astype(float)

# Ensure that ProductKey, SubcategoryKey, and CategoryKey are integers
products['ProductKey'] = products['ProductKey'].astype(int)
products['SubcategoryKey'] = products['SubcategoryKey'].astype(int)
products['CategoryKey'] = products['CategoryKey'].astype(int)

# Handle missing values in 'products' by filling with the median
products['Unit Cost USD'] = products['Unit Cost USD'].fillna(products['Unit Cost USD'].median())
products['Unit Price USD'] = products['Unit Price USD'].fillna(products['Unit Price USD'].median())

currency['Date'] = pd.to_datetime(currency['Date'], errors='coerce')

# Check unique values in the 'Currency' column before cleaning
print("\nUnique values in the 'Currency' column before cleaning:")
print(currency['Currency'].unique())

# Standardize currency column by stripping extra spaces and converting to uppercase
currency['Currency'] = currency['Currency'].str.strip().str.upper()

# Verify cleaned 'Currency' values
print("\nUnique values in the 'Currency' column after cleaning:")
print(currency['Currency'].unique())

# Step 6: Check for duplicates in each dataset
print("\nDuplicates in customers:")
print(customers[customers.duplicated()])

print("Duplicates in products:")
print(products[products.duplicated()])

print("Duplicates in sales:")
print(sales[sales.duplicated()])

print("Duplicates in stores:")
print(stores[stores.duplicated()])

print("Duplicates in currency:")
print(currency[currency.duplicated()])

# Step 7: Check for duplicates based on 'CustomerKey' in 'customers' and 'Order Number' in 'sales'
duplicates_customers_key = customers[customers.duplicated(subset=['CustomerKey'])]
print("\nDuplicates based on 'CustomerKey' in customers:")
print(duplicates_customers_key)

duplicates_sales_order = sales[sales.duplicated(subset=['Order Number'])]
print("\nDuplicates based on 'Order Number' in sales:")
print(duplicates_sales_order)

# Step 8: Remove duplicates and reassign cleaned datasets
customers = customers.drop_duplicates()
products = products.drop_duplicates()
sales = sales.drop_duplicates()
stores = stores.drop_duplicates()
currency = currency.drop_duplicates()

# Step 9: Clean the Sales Data (drop duplicates based on `Order Number` and `Line Item`)
unique_sales = sales.drop_duplicates(subset=['Order Number', 'Line Item'])
print("\nUnique sales after dropping duplicates based on Order Number and Line Item:")
print(unique_sales.head())

# Step 10: Aggregate sales by 'Order Number'
aggregated_sales = sales.groupby('Order Number').agg({
    'Order Date': 'first',
    'Delivery Date': 'first',
    'CustomerKey': 'first',
    'StoreKey': 'first',
    'Quantity': 'sum',  # Sum quantities for the same order
    'Currency Code': 'first'  # Assuming one currency per order
}).reset_index()
print("\nAggregated sales data (one row per order):")
print(aggregated_sales.head())

# Step 11: Final verification of cleaned data
print("\nFinal missing values after all cleaning steps:")
print("Missing values in 'customers.csv':")
print(customers.isnull().sum())
print("Missing values in 'products.csv':")
print(products.isnull().sum())
print("Missing values in 'sales.csv':")
print(sales.isnull().sum())
print("Missing values in 'stores.csv':")
print(stores.isnull().sum())
print("Missing values in 'currency.csv':")
print(currency.isnull().sum())

# Verify data types after cleaning
print("\nData types in customers dataset:")
print(customers.dtypes)

print("\nData types in products dataset:")
print(products.dtypes)

print("\nData types in sales dataset:")
print(sales.dtypes)

print("\nData types in stores dataset:")
print(stores.dtypes)

print("\nData types in currency dataset:")
print(currency.dtypes)

# Specify the output directory
output_dir = r'C:\Global\DataSet\Cleaned'

# Create the directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the cleaned datasets to CSV
customers.to_csv(f'{output_dir}/Cleaned_Customers.csv', index=False)
products.to_csv(f'{output_dir}/Cleaned_Products.csv', index=False)
sales.to_csv(f'{output_dir}/Cleaned_Sales.csv', index=False)
stores.to_csv(f'{output_dir}/Cleaned_Stores.csv', index=False)
currency.to_csv(f'{output_dir}/Cleaned_Exchange_Rates.csv', index=False)

print("Cleaned datasets saved successfully!")

import pandas as pd

# Load the cleaned data for all 5 datasets
customers = pd.read_csv(r'C:\Global\DataSet\Cleaned\Cleaned_Customers.csv')
products = pd.read_csv(r'C:\Global\DataSet\Cleaned\Cleaned_Products.csv')
sales = pd.read_csv(r'C:\Global\DataSet\Cleaned\Cleaned_Sales.csv')
stores = pd.read_csv(r'C:\Global\DataSet\Cleaned\Cleaned_Stores.csv')
exchange_rates = pd.read_csv(r'C:\Global\DataSet\Cleaned\Cleaned_Exchange_Rates.csv')

# Merge sales with customers using CustomerKey
merged_data = pd.merge(sales, customers, on='CustomerKey', how='left')

# Check the result
print("After merging sales with customers:")
print(merged_data.shape)
merged_data = pd.merge(merged_data, products, on='ProductKey', how='left')
print("After merging with products:")
print(merged_data.shape)
merged_data = pd.merge(merged_data, stores, on='StoreKey', how='left')
print("After merging with stores:")
print(merged_data.shape)
exchange_rates.rename(columns={'Currency': 'Currency Code'}, inplace=True)
merged_data = pd.merge(merged_data, exchange_rates, 
                       left_on=['Currency Code', 'Order Date'], 
                       right_on=['Currency Code', 'Date'], 
                       how='left')
print("After merging with exchange rates:")
print(merged_data.shape)
print("\nPreview of the merged dataset:")
print(merged_data.head())
state_to_code = {
    'California': 'CA',
    'Texas': 'TX',
    'Florida': 'FL',
    'New York': 'NY',
    'Napoli': 'NA',
    'Italy': 'IT'  # Assuming 'Italy' itself as a state is rare, default to 'IT'
}

# Update 'State Code' based on 'State_x'
merged_data['State Code'] = merged_data.apply(
    lambda row: state_to_code.get(row['State_x'], row['State Code']), axis=1
)
missing_after_update = merged_data[merged_data['State Code'].isnull()]
print("Rows with missing State Code after reapplying mapping:")
print(missing_after_update[['CustomerKey', 'State_x', 'Country_x']])

print(merged_data.isnull().sum())
print(merged_data[['Quantity', 'Unit Price USD', 'Exchange']].describe())
output_dir = r'C:\Global\DataSet\Merged'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

merged_data.to_csv(f'{output_dir}/Final_Merged_Dataset.csv', index=False)
print("Final merged dataset saved successfully!")

#___________________________________________DATABASE__________________________________________________________________#
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy import text

# Sample data loading (replace this with your own merged DataFrame)
merged_df4 = pd.read_csv(r'C:\Global\DataSet\Merged\Final_Merged_Dataset.csv')  # Adjust this path accordingly

# Create DB connection URL
myconn_url = sa.engine.URL.create(
    drivername='mysql+pymysql',  # Database driver
    username='root',             # Replace with your MySQL username
    password='09876',            # Replace with your MySQL password
    host='localhost',            # Your MySQL host, adjust if necessary
    port=3306,                   # Default MySQL port, change if needed
    database='global_electronics' # Replace with your database name
)

# Creating SQLAlchemy engine to connect to the MySQL Database
engine = create_engine(myconn_url)

# Storing the DataFrame to MySQL
merged_df4.to_sql('sales_table', engine, if_exists='replace', index=False)

# Optionally, print a success message
print("Data saved to MySQL database successfully!")

# Check how many rows were uploaded
with engine.connect() as connection:
    # Using the text() function to wrap the query string
    result = connection.execute(text('SELECT COUNT(*) FROM sales_table'))
    row_count = result.scalar()  # Gets the scalar value (count)
    
    print(f"Number of rows uploaded: {row_count}")
