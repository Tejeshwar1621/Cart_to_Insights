# Cart2Insights – E-Commerce Data Analytics

## 1. Project Overview

Cart2Insights is an end-to-end e-commerce data analytics project developed to transform raw e-commerce datasets into a structured, cleaned, analyzed, and visualized business solution.

The project combines Python, Pandas, MySQL, SQL, statistical analysis, and Streamlit to understand sales performance, customer behavior, seller performance, product performance, delivery operations, and customer experience.

The project follows a complete analytics workflow:

```text
Raw Data
   ↓
Business Problem Understanding
   ↓
Dataset & ER Diagram Understanding
   ↓
Data Loading
   ↓
Data Quality Analysis
   ↓
Data Cleaning & Preprocessing
   ↓
Feature Engineering
   ↓
MySQL Database Integration
   ↓
SQL Business Analysis
   ↓
EDA
   ↓
Statistical Analysis
   ↓
Streamlit Dashboard
   ↓
Business Insights & Recommendations
```

---

## 2. Project Objective

The objective of Cart2Insights is to build a complete, data-driven e-commerce analytics solution that:

- Understands multiple related e-commerce datasets.
- Cleans and validates raw data.
- Creates meaningful analytical features.
- Stores cleaned and engineered data in a SQL database.
- Performs business analysis using SQL.
- Performs exploratory data analysis.
- Applies appropriate statistical methods.
- Builds an interactive Streamlit dashboard.
- Converts analytical findings into business insights and recommendations.

---

## 3. Business Problem

The project focuses on understanding e-commerce business performance across multiple areas:

- Revenue and order performance
- Customer distribution and spending
- Repeat customer behavior
- Seller performance
- Product and category performance
- Regional sales performance
- Delivery time and delays
- Customer review scores
- Relationship between delivery performance and customer satisfaction

The analysis is designed to answer business questions related to sales, customers, sellers, products, delivery operations, and customer experience.

---

# 4. Project Setup

## 4.1 Project Folder Structure

The project was organized into separate folders for raw/cleaned data, analytical notebooks, and the Streamlit application.

```text
Cart_to_Insights/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── notebooks/
│   ├── data_cleaning_cleaned.ipynb
│   ├── feature_engineering_cleaned.ipynb
│   ├── sql_analysis.ipynb
│   ├── eda_analysis.ipynb
│   ├── statistical_analysis.ipynb
│   └── .env
│
└── streamlit/
    └── app.py
```

The notebooks contain the individual stages of the analytical workflow, while the Streamlit application presents the final business analysis interactively.

---

## 4.2 Python Environment

Python was used as the main programming language for data loading, cleaning, transformation, feature engineering, exploratory analysis, statistical analysis, and dashboard development.

The main libraries used include:

- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- SciPy
- SQLAlchemy
- PyMySQL
- python-dotenv
- Streamlit

---

## 4.3 Database Setup

A MySQL database named `cart2insights` was used to store the cleaned and feature-engineered data.

The database connection was configured using environment variables in:

```text
notebooks/.env
```

The connection configuration follows this structure:

```text
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=cart2insights
```

The database password is kept outside the source code using the `.env` file.

Python connects to MySQL using SQLAlchemy and PyMySQL.

---

## 4.4 Raw Dataset Setup

The raw CSV files were placed inside:

```text
data/raw/
```

The project works with the following related datasets:

- Customers
- Geolocation
- Sellers
- Products
- Orders
- Order Items
- Order Payments
- Order Reviews
- Category Translation

The relationships between these tables were studied using the dataset structure and ER diagram before performing the analysis.

---

# 5. Project Workflow

## Step 1 – Understand the Business Problem

The project began by identifying the business context and the main analytical objectives.

The analysis was designed to answer questions such as:

- How is revenue changing over time?
- Which categories and products contribute to sales?
- Which customers generate higher value?
- How do repeat customers behave?
- Which sellers perform strongly?
- How does delivery performance vary?
- Are delivery delays associated with customer satisfaction?
- How do review scores vary across categories and delivery outcomes?

---

## Step 2 – Understand the Dataset and Relationships

The structure of all available tables was examined.

The analysis included:

- Table names
- Column names
- Data types
- Primary keys
- Foreign keys
- Relationships between tables
- Business meaning of important columns

The main relationships include:

```text
Customers
    ↓
Orders
    ↓
Order Items
    ↓
Products
    ↓
Category Translation

Orders
    ↓
Order Payments

Orders
    ↓
Order Reviews

Order Items
    ↓
Sellers

Customers / Sellers
    ↓
Geolocation
```

This relationship understanding was used throughout the cleaning, SQL, feature engineering, and dashboard stages.

---

## Step 3 – Load the Raw Data

The raw CSV files were loaded using Pandas.

Initial checks were performed for:

- Number of rows
- Number of columns
- Column names
- Data types
- Missing values
- Duplicate records

The raw datasets were then prepared for the data-quality stage.

---

# 6. Data Cleaning and Preprocessing

Data quality analysis was performed before creating business features.

The following checks were completed:

- Missing-value analysis
- Duplicate analysis
- Data-type validation
- Primary-key uniqueness checks
- Invalid-value checks
- Date/time validation
- Categorical-value consistency
- Potential outlier identification

Examples from the cleaned datasets include:

| Dataset | Rows | Columns | Missing Values |
|---|---:|---:|---:|
| Customers | 99,441 | 5 | 0 |
| Geolocation | 738,332 | 5 | 0 |
| Orders | 99,441 | 8 | 5,103 |
| Order Items | 112,650 | 7 | 0 |
| Order Payments | 103,886 | 5 | 0 |
| Order Reviews | 99,224 | 7 | 0 |
| Products | 32,951 | 9 | 0 |
| Sellers | 3,095 | 4 | Checked |

The identified data-quality issues were handled during preprocessing before the data was used for downstream analysis.

---

# 7. Feature Engineering

After cleaning, business-oriented features were created to support analysis.

## 7.1 Order Features

The order-level analytical dataset includes features such as:

- Total order value
- Delivery days
- Delivery delay days
- Delivery status
- Purchase year
- Purchase month
- Purchase date-related fields

The resulting `order_features` dataset contains approximately 99,441 orders and 34 analytical columns.

---

## 7.2 Customer Features

Customer-level features were created to measure customer value and behavior.

Important features include:

- Customer order count
- Customer total spending
- Customer average order value
- Repeat customer indicator

The `customer_features` dataset contains approximately 96,096 customers.

---

## 7.3 Seller Features

Seller performance was summarized using:

- Seller revenue
- Seller order count
- Seller item count
- Seller unique products
- Seller average item price

The resulting `seller_features` dataset contains approximately 3,095 sellers.

---

## 7.4 Product Features

Product-level features include:

- Product revenue
- Product order count
- Product item count
- Product average price

The resulting `product_features` dataset contains approximately 32,951 products.

---

## 7.5 Category Features

Category-level features were created to support:

- Category revenue analysis
- Category order-value analysis
- Product/category performance comparison

---

# 8. MySQL Database Integration

After cleaning and feature engineering, the analytical datasets were stored in the MySQL database.

The main analytical tables include:

```text
order_features
customer_features
seller_features
product_features
category_features
business_kpis
```

Python was connected to MySQL using SQLAlchemy and PyMySQL.

The SQL analysis was then performed directly against the database tables.

---

# 9. SQL Business Analysis

The SQL analysis was designed around business questions rather than only technical queries.

The project uses:

- JOIN
- GROUP BY
- Aggregations
- CTEs
- Subqueries
- HAVING
- Window functions

Business analyses include:

- Overall business KPIs
- Monthly revenue
- Revenue by category
- Top products
- Sales by state/location
- Customer distribution
- Customer spending
- Repeat customers
- High-value customers
- Seller performance
- Seller ratings
- Delivery status
- Delivery performance by location
- Delivery delay and review analysis
- Review distribution
- Reviews by category
- Payment outcomes
- Seller revenue ranking
- Products performing above average

---

# 10. Exploratory Data Analysis

EDA was performed to identify patterns and relationships in the business data.

The analysis covered:

### Sales

- Revenue trends
- Category performance
- Product performance
- Regional sales

### Customers

- Customer distribution
- Customer spending
- Repeat purchasing
- High-value customers

### Sellers and Products

- Seller revenue
- Seller order volume
- Product performance
- Category performance
- Seller ratings

### Delivery

- Delivery duration
- Delivery status
- Delivery delays
- Regional delivery performance

### Customer Experience

- Review score distribution
- Category review performance
- Delivery performance versus review scores

---

# 11. Statistical Analysis

Statistical tests were selected according to the business questions and the characteristics of the data.

## Welch t-test

Used to compare review scores between delayed and on-time orders.

Results:

```text
Delayed orders mean review score: 2.5651
On-time orders mean review score: 4.2943
Difference: -1.7292
Welch t-statistic: -89.4341
Cohen's d: -1.4471
95% CI: -1.7671 to -1.6913
```

The result indicates a statistically significant difference in review scores between delayed and on-time orders.

---

## Welch ANOVA

Used to compare order values across product categories.

The original ANOVA showed:

```text
F-statistic: 154.1987
p-value: < 0.001
eta-squared: 0.1007
```

Because the variance assumption was not satisfied, the analysis was corrected to Welch ANOVA.

---

## Chi-square Test

Used to examine the relationship between payment method and delivery outcome.

Unknown payment methods were excluded before performing the test.

---

## Spearman Correlation

Used to examine the relationship between positive delivery delay and review score for delayed orders.

This was used because the analysis focused on the relationship between actual delay values and customer ratings.

---

## Pearson Correlation

Used to examine the relationship between basket size and order value.

Result:

```text
Correlation coefficient: 0.1973
p-value: < 0.001
```

This indicates a positive and statistically significant relationship between basket size and order value.

---

# 12. Streamlit Dashboard

The final analytical results were presented through a Streamlit dashboard.

The dashboard contains six main sections.

## 12.1 Business Overview

The dashboard displays:

- Total Revenue
- Total Orders
- Total Customers
- Total Sellers
- Average Order Value
- Average Review Score

## 12.2 Sales Analysis

The dashboard displays:

- Monthly revenue trend
- Revenue by category
- Top-selling products
- Sales by location

## 12.3 Customer Analysis

The dashboard displays:

- Customer distribution
- Customer spending
- Repeat vs new customers
- Top customers

## 12.4 Seller & Product Analysis

The dashboard displays:

- Top sellers
- Seller revenue
- Product/category performance
- Seller ratings

## 12.5 Delivery Analysis

The dashboard displays:

- Average delivery time
- On-time vs delayed orders
- Delivery performance by location
- Delivery delay vs review score

## 12.6 Customer Experience

The dashboard displays:

- Review score distribution
- Reviews by category
- Rating vs delivery performance

---

# 13. Key Business Findings

## Finding 1 – Delivery Delays and Customer Satisfaction

**Observation:** Delayed orders had an average review score of approximately 2.57, while on-time orders had an average review score of approximately 4.29.

**Interpretation:** Customer ratings are substantially lower for delayed orders.

**Business Impact:** Delivery reliability is an important part of the customer experience. Reducing delays can help improve customer satisfaction.

---

## Finding 2 – Delivery Performance Shows a Strong Relationship with Reviews

**Observation:** Delivery performance was analyzed against customer review scores using both group comparison and correlation analysis.

**Interpretation:** The analysis indicates that delivery performance is closely connected with customer experience.

**Business Impact:** Delivery monitoring should be treated as an important customer-experience metric.

---

## Finding 3 – Order Values Differ Across Categories

**Observation:** Order values were compared across product categories using Welch ANOVA.

**Interpretation:** Order-value distributions differ across categories.

**Business Impact:** Category-level performance should be monitored separately rather than treating all categories as having the same sales behavior.

---

## Finding 4 – Larger Baskets Are Associated with Higher Order Values

**Observation:** Pearson correlation between basket size and order value was approximately 0.1973 and statistically significant.

**Interpretation:** Orders containing more items tend to have higher order values, although basket size does not explain all variation in order value.

**Business Impact:** Increasing basket size can be considered when designing product-bundling or cross-selling strategies.

---

## Finding 5 – Customer Value Varies Across Customers

**Observation:** Customer features were created for order count, total spending, average order value, and repeat-customer behavior.

**Interpretation:** Customer-level analysis allows the business to distinguish different levels of customer value and purchasing behavior.

**Business Impact:** Customer retention and high-value customer analysis can support targeted business strategies.

---

## Finding 6 – Seller Performance Varies

**Observation:** Seller revenue, order count, item count, product coverage, average item price, and ratings were analyzed.

**Interpretation:** Sellers contribute differently to overall business performance and customer experience.

**Business Impact:** Seller-level monitoring can help identify performance differences and areas for operational improvement.

---

## Finding 7 – Regional Performance Differs

**Observation:** Sales and delivery performance were analyzed across customer locations.

**Interpretation:** Customer demand and delivery performance vary by region.

**Business Impact:** Regional analysis can support sales planning and delivery operations.

---

## Finding 8 – Customer Reviews Provide an Important Experience Measure

**Observation:** Review scores were analyzed across orders, categories, and delivery performance.

**Interpretation:** Customer reviews provide a measurable indicator of customer experience.

**Business Impact:** Review monitoring can help identify products, categories, sellers, or operational areas that require attention.

---

# 14. Business Recommendations

Based on the completed analysis:

1. **Improve delivery reliability**
   - Monitor delayed orders and investigate operational causes of delays.
   - Track delivery performance alongside customer ratings.

2. **Monitor category-level performance**
   - Compare revenue and order-value behavior across categories.
   - Use category-level findings to support product and sales decisions.

3. **Focus on customer retention**
   - Identify repeat and high-value customers.
   - Monitor customer spending and purchasing frequency.

4. **Monitor seller performance**
   - Track seller revenue, order volume, product coverage, and ratings.
   - Investigate sellers with weaker customer-experience indicators.

5. **Monitor regional performance**
   - Compare sales and delivery performance across locations.
   - Use regional patterns to support operational planning.

6. **Use customer feedback for continuous improvement**
   - Monitor review scores by category, seller, and delivery performance.
   - Investigate areas associated with lower customer ratings.

---

# 15. How the Project Was Executed

The project was completed in stages rather than treating the dashboard as a standalone application.

```text
1. Business Problem
        ↓
2. Dataset Understanding & ER Relationships
        ↓
3. Raw Data Loading
        ↓
4. Data Quality Analysis
        ↓
5. Data Cleaning & Preprocessing
        ↓
6. Feature Engineering
        ↓
7. MySQL Database Storage
        ↓
8. SQL Business Analysis
        ↓
9. Exploratory Data Analysis
        ↓
10. Statistical Analysis
        ↓
11. Streamlit Dashboard
        ↓
12. Business Insights & Recommendations
```

Each stage uses the output of the previous stage so that the final dashboard and business findings are based on the cleaned and analyzed data.

---

# 16. Project Deliverables

The completed project includes:

- Python notebooks for data cleaning
- Python notebook for feature engineering
- SQL analysis notebook
- EDA notebook
- Statistical analysis notebook
- MySQL database integration
- `.env` database configuration
- Streamlit dashboard
- Business insights
- Business recommendations
- Project documentation

---

# 17. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data loading, cleaning and transformation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive dashboard charts |
| SciPy | Statistical testing |
| MySQL | Database storage and SQL analysis |
| SQLAlchemy | Python-SQL connectivity |
| PyMySQL | MySQL database driver |
| python-dotenv | Environment variable management |
| Streamlit | Interactive dashboard |
| Jupyter Notebook | Analytical development |

---

# 18. Conclusion

Cart2Insights demonstrates a complete end-to-end e-commerce analytics workflow.

The project starts with raw multi-table e-commerce data and progresses through data understanding, quality analysis, cleaning, feature engineering, SQL database integration, business analysis, EDA, statistical analysis, and dashboard development.

The final solution converts the raw data into meaningful business information covering sales, customers, sellers, products, delivery operations, and customer experience.

One of the strongest findings is the substantial difference in customer review scores between delayed and on-time orders, demonstrating the importance of delivery performance in the overall customer experience.

The project therefore combines technical implementation with statistical evidence and business interpretation to produce a complete data-driven e-commerce analytics solution.
