python -m venv mysql_env
 ./mysql_env/Scripts/activate


# Calculate the delivery time delta (Order Date to Delivery Date)
sales['Order Date'] = pd.to_datetime(sales['Order Date'])
sales['Delivery Date'] = pd.to_datetime(sales['Delivery Date'], errors='coerce')

# Calculate the median delivery time difference (if not already calculated)
median_delivery_time = (sales['Delivery Date'] - sales['Order Date']).median()

# Fill missing Delivery Date based on the Order Date + median delivery time

sales['Delivery Date'] = sales['Delivery Date'].fillna(sales['Order Date'] + median_delivery_time)


# Fill missing Square Meters in stores with the median value (fixing inplace warning)
stores['Square Meters'] = stores['Square Meters'].fillna(stores['Square Meters'].median())

# Verify again after handling missing values
print("After handling missing values:")

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



customers.drop_duplicates(subset=['CustomerKey'], inplace=True)
# Check for duplicates based on 'Order Number' (for 'sales')
duplicates_sales_order = sales[sales.duplicated(subset=['Order Number'])]
print("Duplicates based on 'Order Number' in sales:")
print(duplicates_sales_order)

# Step 1: Merge the sales and exchange_rates datasets based on 'Currency Code' and 'Currency'
merged_data = pd.merge(sales, exchange_rates, how='inner', left_on='Currency Code', right_on='Currency')

# Step 2: Merge the resulting data with customers, products, and stores datasets
merged_data = pd.merge(merged_data, customers, how='inner', on='CustomerKey')
merged_data = pd.merge(merged_data, products, how='inner', on='ProductKey')
merged_data = pd.merge(merged_data, stores, how='inner', on='StoreKey')

# Step 3: Feature Engineering - Calculate Profit
merged_data['Profit'] = (merged_data['Unit Price USD'] - merged_data['Unit Cost USD']) * merged_data['Quantity']

# Step 4: Aggregation - Calculate total sales and profit per store
store_sales = merged_data.groupby('StoreKey').agg({
    'Quantity': 'sum',
    'Profit': 'sum',
    'Unit Price USD': 'mean',
    'Unit Cost USD': 'mean'
}).reset_index()

# Display aggregated store sales data
print(store_sales)

# Step 5: Save the final merged dataset
output_path = r'C:\Global\DataSet\Cleaned\Final_Merged_Data.csv'
merged_data.to_csv(output_path, index=False)
print("Final merged data saved successfully!")


print("\nSummary of missing values after merging:")
print(merged_data.isnull().sum())
output_dir = r'C:\Global\DataSet\Merged'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

merged_data.to_csv(f'{output_dir}/Final_Merged_Dataset.csv', index=False)
print("Final merged dataset saved successfully!")