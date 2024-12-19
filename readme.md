# Global Electronics Data Analysis Project

This project involves SQL-based data analysis for the **Global Electronics** dataset. The analysis aims to enhance customer satisfaction, optimize operations, and drive business growth through actionable insights.

---

## Table of Contents
1. [MySQL Query Analysis](#mysql-query-analysis)
2. [Customer Analysis](#customer-analysis)
3. [Sales Analysis](#sales-analysis)
4. [Product Analysis](#product-analysis)
5. [Store Analysis](#store-analysis)
6. [Query Analysis](#query-analysis)

---

## MySQL Query Analysis
**Database Used:** `global_electronics`

```sql
ALTER TABLE sales
MODIFY COLUMN Order Number BIGINT,
MODIFY COLUMN Line Item BIGINT,
MODIFY COLUMN Order Date DATETIME,
MODIFY COLUMN Delivery Date DATETIME,
MODIFY COLUMN CustomerKey BIGINT,
MODIFY COLUMN StoreKey BIGINT,
MODIFY COLUMN ProductKey BIGINT,
MODIFY COLUMN Quantity BIGINT,
MODIFY COLUMN Currency Code VARCHAR(10),
MODIFY COLUMN Gender VARCHAR(10),
MODIFY COLUMN Name VARCHAR(255),
MODIFY COLUMN City VARCHAR(255),
MODIFY COLUMN State Code VARCHAR(50),
MODIFY COLUMN State_x VARCHAR(255),
MODIFY COLUMN Zip Code VARCHAR(20),
MODIFY COLUMN Country_x VARCHAR(255),
MODIFY COLUMN Continent VARCHAR(255),
MODIFY COLUMN Birthday DATE,
MODIFY COLUMN Product Name VARCHAR(255),
MODIFY COLUMN Brand VARCHAR(255),
MODIFY COLUMN Color VARCHAR(50),
MODIFY COLUMN Unit Cost USD DOUBLE,
MODIFY COLUMN Unit Price USD DOUBLE,
MODIFY COLUMN SubcategoryKey BIGINT,
MODIFY COLUMN Subcategory VARCHAR(255),
MODIFY COLUMN CategoryKey BIGINT,
MODIFY COLUMN Category VARCHAR(255),
MODIFY COLUMN Country_y VARCHAR(255),
MODIFY COLUMN State_y VARCHAR(255),
MODIFY COLUMN Square Meters DOUBLE,
MODIFY COLUMN Open Date DATETIME,
MODIFY COLUMN Date DATETIME,
MODIFY COLUMN Exchange DOUBLE;
```

---

## Customer Analysis
### 1. Demographic Distribution
- **1.1 Gender Distribution**
```sql
SELECT Gender, COUNT(CustomerKey) AS CustomerCount
FROM sales_table
GROUP BY Gender
ORDER BY CustomerCount DESC;
```

- **1.2 Age Distribution**
```sql
SELECT 
    CASE 
        WHEN Age BETWEEN 0 AND 18 THEN '0-18'
        WHEN Age BETWEEN 19 AND 35 THEN '19-35'
        WHEN Age BETWEEN 36 AND 50 THEN '36-50'
        WHEN Age > 50 THEN '50+'
    END AS AgeGroup,
    COUNT(CustomerKey) AS CustomerCount
FROM (
    SELECT CustomerKey, TIMESTAMPDIFF(YEAR, Birthday, CURDATE()) AS Age
    FROM sales_table
    WHERE Birthday IS NOT NULL
) AS AgeData
GROUP BY AgeGroup
ORDER BY CustomerCount DESC;
```

- **1.3 Location Distribution**
```sql
SELECT 
    Continent, 
    Country_x, 
    State_x, 
    COUNT(CustomerKey) AS CustomerCount
FROM sales_table
GROUP BY Continent, Country_x, State_x
ORDER BY CustomerCount DESC;
```

### 2. Purchase Patterns
- **2.1 Average Order Value**
```sql
SELECT 
    AVG(OrderTotal) AS AvgOrderValue
FROM (
    SELECT 
        Order Number, 
        SUM(Quantity * Unit Price USD) AS OrderTotal
    FROM sales_table
    GROUP BY Order Number
) AS OrderData;
```

- **2.2 Purchase Frequency**
```sql
SELECT 
    CustomerKey, 
    COUNT(Order Number) AS PurchaseFrequency
FROM sales_table
GROUP BY CustomerKey
ORDER BY PurchaseFrequency DESC;
```

### 3. Customer Segmentation
- **3.1 RFM Analysis**
```sql
SELECT 
    R.CustomerKey, 
    DATEDIFF(CURDATE(), R.LastPurchaseDate) AS Recency, 
    F.PurchaseFrequency, 
    M.TotalSpent
FROM (
    SELECT CustomerKey, MAX(Order Date) AS LastPurchaseDate FROM sales_table GROUP BY CustomerKey
) AS R
JOIN (
    SELECT CustomerKey, COUNT(Order Number) AS PurchaseFrequency FROM sales_table GROUP BY CustomerKey
) AS F ON R.CustomerKey = F.CustomerKey
JOIN (
    SELECT CustomerKey, SUM(Quantity * Unit Price USD) AS TotalSpent FROM sales_table GROUP BY CustomerKey
) AS M ON R.CustomerKey = M.CustomerKey
ORDER BY Recency ASC, PurchaseFrequency DESC, TotalSpent DESC;
```

- **3.2 Demographic-Based Segmentation**
```sql
SELECT 
    Continent, 
    Country_x, 
    Gender, 
    COUNT(CustomerKey) AS CustomerCount
FROM sales_table
GROUP BY Continent, Country_x, Gender
ORDER BY CustomerCount DESC;
```

---

## Sales Analysis
### 1. Overall Sales Performance (Trends & Seasonality)
```sql
SELECT 
    DATE_FORMAT(Order Date, '%Y-%m') AS MonthYear, 
    SUM(Quantity * Unit Price USD) AS TotalSales
FROM sales_table
WHERE Order Date IS NOT NULL AND Order Date != '0000-00-00'
GROUP BY MonthYear
ORDER BY MonthYear;
```

### 2. Sales by Product (Top Performers by Quantity and Revenue)
```sql
SELECT 
    Product Name, 
    SUM(Quantity) AS TotalQuantitySold, 
    SUM(Quantity * Unit Price USD) AS TotalRevenue
FROM sales_table
GROUP BY Product Name
ORDER BY TotalRevenue DESC;
```

### 3. Sales by Store (Assessing Store Performance)
```sql
SELECT 
    StoreKey, 
    SUM(Quantity * Unit Price USD) AS TotalSales
FROM sales_table
GROUP BY StoreKey
ORDER BY TotalSales DESC;
```

### 4. Sales by Currency (Impact of Exchange Rates)
```sql
SELECT 
    Currency Code, 
    SUM(Quantity * Unit Price USD * Exchange) AS TotalSalesInCurrency
FROM sales_table
GROUP BY Currency Code
ORDER BY TotalSalesInCurrency DESC;
```

---

## Product Analysis
### 1. Product Popularity
```sql
SELECT 
    Product Name, 
    SUM(Quantity) AS TotalQuantitySold
FROM sales_table
GROUP BY Product Name
ORDER BY TotalQuantitySold DESC;
```

---

## Store Analysis
### 1. Store Performance
```sql
SELECT 
    StoreKey, 
    SUM(Quantity * Unit Price USD) AS TotalSales, 
    AVG(Square Meters) AS AvgStoreSize,
    MIN(Open Date) AS StoreOpeningDate
FROM sales_table
GROUP BY StoreKey
ORDER BY TotalSales DESC;
```

---

## Query Analysis
### 1. Gender-Based Product Preferences
```sql
SELECT 
    Gender, 
    Product Name, 
    SUM(Quantity) AS TotalQuantitySold, 
    SUM(Quantity * Unit Price USD) AS TotalRevenue
FROM sales_table
GROUP BY Gender, Product Name
ORDER BY Gender, TotalQuantitySold DESC, TotalRevenue DESC;
```
---

#### 2. RFM Analysis
```sql
SELECT 
    R.CustomerKey, 
    DATEDIFF(CURDATE(), R.LastPurchaseDate) AS Recency, 
    F.PurchaseFrequency, 
    M.TotalSpent
FROM (
    SELECT CustomerKey, MAX(`Order Date`) AS LastPurchaseDate 
    FROM sales_table 
    GROUP BY CustomerKey
) AS R
JOIN (
    SELECT CustomerKey, COUNT(`Order Number`) AS PurchaseFrequency 
    FROM sales_table 
    GROUP BY CustomerKey
) AS F ON R.CustomerKey = F.CustomerKey
JOIN (
    SELECT CustomerKey, SUM(Quantity * `Unit Price USD`) AS TotalSpent 
    FROM sales_table 
    GROUP BY CustomerKey
) AS M ON R.CustomerKey = M.CustomerKey
ORDER BY Recency ASC, PurchaseFrequency DESC, TotalSpent DESC;
```

#### 3. Sales Performance by Country
```sql
SELECT 
    Country_x, 
    SUM(Quantity * `Unit Price USD`) AS TotalSales,
    COUNT(`Order Number`) AS TotalOrders
FROM sales_table
GROUP BY Country_x
ORDER BY TotalSales DESC, TotalOrders DESC;
```

#### 4. Average Order Value
```sql
SELECT 
    AVG(OrderTotal) AS AvgOrderValue
FROM (
    SELECT 
        `Order Number`, 
        SUM(Quantity * `Unit Price USD`) AS OrderTotal
    FROM sales_table
    GROUP BY `Order Number`
) AS OrderData;
```

#### 5. Unique Product Variety by Store
```sql
SELECT 
    StoreKey, 
    COUNT(DISTINCT `Product Name`) AS UniqueProducts
FROM sales_table
GROUP BY StoreKey
ORDER BY UniqueProducts DESC;
```

#### 6. Subcategory Profitability Analysis
```sql
SELECT 
    Subcategory, 
    SUM(Quantity * (`Unit Price USD` - `Unit Cost USD`)) AS TotalProfit, 
    AVG(`Unit Price USD` - `Unit Cost USD`) AS AvgProfitMargin
FROM sales_table
GROUP BY Subcategory
ORDER BY AvgProfitMargin DESC, TotalProfit DESC;
```

#### 7. Year-over-Year Growth Analysis
```sql
SELECT 
    YEAR(`Order Date`) AS Year, 
    SUM(Quantity * `Unit Price USD`) AS TotalSales,
    (SUM(Quantity * `Unit Price USD`) - LAG(SUM(Quantity * `Unit Price USD`)) OVER (ORDER BY YEAR(`Order Date`))) / LAG(SUM(Quantity * `Unit Price USD`)) OVER (ORDER BY YEAR(`Order Date`)) * 100 AS YoYGrowthPercentage
FROM sales_table
GROUP BY Year
ORDER BY Year;
```

#### 8. Customers by Total Revenue
```sql
SELECT 
    CustomerKey, 
    SUM(Quantity * `Unit Price USD`) AS TotalRevenue,
    COUNT(`Order Number`) AS TotalOrders
FROM sales_table
GROUP BY CustomerKey
ORDER BY TotalRevenue DESC, TotalOrders DESC;
```

#### 9. Top 10 Brands with Categories by Sales
```sql
SELECT 
    Brand, 
    Category, 
    SUM(Quantity * `Unit Price USD`) AS TotalSales, 
    SUM(Quantity) AS TotalQuantitySold
FROM sales_table
GROUP BY Brand, Category
ORDER BY TotalSales DESC, TotalQuantitySold DESC
LIMIT 10;
```

#### 10. Store Sales Performance by Profit
```sql
SELECT 
    StoreKey, 
    SUM(Quantity * (`Unit Price USD` - `Unit Cost USD`)) AS TotalProfit, 
    AVG(`Unit Price USD` - `Unit Cost USD`) AS AvgProfitMargin
FROM sales_table
GROUP BY StoreKey
ORDER BY TotalProfit DESC, AvgProfitMargin DESC;
```

--- 
