import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the file path (use raw string to avoid issues with backslashes)
file_path = r"C:\Users\ELITEBOOK 755 G5\OneDrive\Documents\Auto Sales Data.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Display first few rows
print(df.head())

# 1. Remove duplicates
df.drop_duplicates(inplace=True)

# 2. Handle missing values
df.dropna(subset=['ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'SALES', 'ORDERDATE'], inplace=True)
df.fillna({'DAYS_SINCE_LASTORDER': 0, 'POSTALCODE': 'Unknown'}, inplace=True)

# 3. Convert data types
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], format="%d/%m/%Y", errors='coerce')
# Convert to datetime
df['QUANTITYORDERED'] = pd.to_numeric(df['QUANTITYORDERED'], errors='coerce')  # Convert to numeric
df['PRICEEACH'] = pd.to_numeric(df['PRICEEACH'], errors='coerce')
df['SALES'] = pd.to_numeric(df['SALES'], errors='coerce')

# 4. Standardize text columns
text_columns = ['STATUS', 'PRODUCTLINE', 'CUSTOMERNAME', 'CITY', 'COUNTRY', 'CONTACTLASTNAME', 'CONTACTFIRSTNAME']
for col in text_columns:
    df[col] = df[col].str.strip().str.title()  # Remove extra spaces and capitalize

# 5. Remove invalid data (e.g., negative prices or sales)
df = df[(df['PRICEEACH'] >= 0) & (df['SALES'] >= 0)]

# 6. Save the cleaned dataset
cleaned_file_path = r"C:\Users\ELITEBOOK 755 G5\OneDrive\Documents\Cleaned_Auto_Sales_Data.csv"
df.to_csv(cleaned_file_path, index=False)

# Display cleaned dataset
print("\nCleaned Data:")
print(df.head())

# Define cleaned data file path
cleaned_file_path = r"C:\Users\ELITEBOOK 755 G5\OneDrive\Documents\Cleaned_Auto_Sales_Data.csv"

# Load the cleaned dataset
df = pd.read_csv(cleaned_file_path)

# Convert ORDERDATE to datetime format
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], format="%d/%m/%Y", errors='coerce')

### ---  SALES PERFORMANCE ANALYSIS --- ###

# Total Sales
total_sales = df['SALES'].sum()
print(f"Total Sales: ${total_sales:,.2f}")

#  Sales Trend Over Time
df['YEAR_MONTH'] = df['ORDERDATE'].dt.to_period('M')
monthly_sales = df.groupby('YEAR_MONTH')['SALES'].sum()

plt.figure(figsize=(10, 5))
sns.lineplot(x=monthly_sales.index.astype(str), y=monthly_sales.values, marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend")
plt.xlabel("Year-Month")
plt.ylabel("Total Sales ($)")
#plt.grid(True)
#plt.show()

#  Top-Selling Products
top_products = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False)
print("\nTop-Selling Products:\n", top_products)

#  Sales by Country
sales_by_country = df.groupby('COUNTRY')['SALES'].sum().sort_values(ascending=False)
print("\nSales by Country:\n", sales_by_country.head(10))

### ---  CUSTOMER BEHAVIOR ANALYSIS --- ###

#  Average Order Value (AOV)
aov = df.groupby('ORDERNUMBER')['SALES'].sum().mean()
print(f"\nAverage Order Value: ${aov:,.2f}")

#  Customer Retention (Time Between Orders)
df['DAYS_SINCE_LASTORDER'] = pd.to_numeric(df['DAYS_SINCE_LASTORDER'], errors='coerce')
avg_days_between_orders = df['DAYS_SINCE_LASTORDER'].mean()
print(f"\nAverage Days Between Orders: {avg_days_between_orders:.2f} days")

#  High-Value Customers
top_customers = df.groupby('CUSTOMERNAME')['SALES'].sum().sort_values(ascending=False).head(10)
print("\nTop 10 High-Value Customers:\n", top_customers)

### ---  PRODUCT PERFORMANCE ANALYSIS --- ###

#  Quantity Ordered per Product Line
qty_by_product = df.groupby('PRODUCTLINE')['QUANTITYORDERED'].sum().sort_values(ascending=False)
print("\nQuantity Ordered per Product Line:\n", qty_by_product)

#  Revenue vs. MSRP
df['MSRP'] = pd.to_numeric(df['MSRP'], errors='coerce')
avg_discount = (df['MSRP'] - df['PRICEEACH']).mean()
print(f"\nAverage Discount Given per Product: ${avg_discount:.2f}")

#  Seasonal Sales Pattern
df['MONTH'] = df['ORDERDATE'].dt.month
seasonal_sales = df.groupby('MONTH')['SALES'].sum()

plt.figure(figsize=(8, 5))
sns.barplot(x=seasonal_sales.index, y=seasonal_sales.values, palette="Blues")
plt.title("Sales by Month")
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")
#plt.grid(True)
#plt.show()

### ---  OPERATIONAL ANALYSIS --- ###

#  Order Processing Efficiency (Status Analysis)
order_status_counts = df['STATUS'].value_counts()
print("\nOrder Status Breakdown:\n", order_status_counts)

#  Order Line Analysis (Average Products per Order)
avg_order_line = df.groupby('ORDERNUMBER')['ORDERLINENUMBER'].count().mean()
print(f"\nAverage Number of Products per Order: {avg_order_line:.2f}")

#  Sales Forecasting (Basic Moving Average)
df['SALES_MA'] = df['SALES'].rolling(window=3).mean()

plt.figure(figsize=(10, 5))
sns.lineplot(x=df.index, y=df['SALES'], label="Actual Sales")
sns.lineplot(x=df.index, y=df['SALES_MA'], label="3-Period Moving Avg", linestyle="dashed")
plt.title("Sales Forecasting with Moving Average")
plt.xlabel("Order Index")
plt.ylabel("Sales ($)")
plt.legend()
#plt.grid(True)
#plt.show()

### ---  MARKETING INSIGHTS --- ###

#  Order Size Distribution
order_sizes = df['DEALSIZE'].value_counts()

plt.figure(figsize=(7, 5))
sns.barplot(x=order_sizes.index, y=order_sizes.values, palette="viridis")
plt.title("Order Size Distribution")
plt.xlabel("Deal Size")
plt.ylabel("Number of Orders")
#plt.grid(True)
#plt.show()

#  Sales Impact on Promotions (Discount Impact)
df['DISCOUNT'] = df['MSRP'] - df['PRICEEACH']
discount_impact = df.groupby('DISCOUNT')['SALES'].sum()

plt.figure(figsize=(8, 5))
sns.scatterplot(x=discount_impact.index, y=discount_impact.values)
plt.title("Impact of Discounts on Sales")
plt.xlabel("Discount Amount ($)")
plt.ylabel("Total Sales ($)")
#plt.grid(True)
#plt.show()

print("\n All analyses completed successfully!")