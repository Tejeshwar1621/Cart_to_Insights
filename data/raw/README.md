# Raw Data

This folder contains the original source CSV files used in the Cart2Insights e-commerce analytics project.

## Source Tables

The raw dataset contains the following nine related tables:

- Customers
- Geolocation
- Sellers
- Products
- Orders
- Order Items
- Order Payments
- Order Reviews
- Category Translation

## Purpose

The raw files are used as the starting point of the project workflow:

```text
Raw CSV Files
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
Business Analysis
```

The raw data should remain unchanged. Cleaning, transformation, and feature creation are performed through the project notebooks.

## Repository Note

The raw CSV files are excluded from Git because of their size and to keep the repository lightweight. Place the original dataset files in this folder when running the project locally.
