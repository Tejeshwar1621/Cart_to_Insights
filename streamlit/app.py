import os
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / "notebooks" / ".env")

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "cart2insights")

st.set_page_config(page_title="Cart2Insights", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    .subtitle {
        font-size: 18px;
        color: #64748B;
        margin-bottom: 30px;
        font-weight: 400;
    }
    .section-title {
        font-size: 28px;
        font-weight: 600;
        color: #0F172A;
        margin-top: 20px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #E2E8F0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def get_engine():
    url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    return create_engine(url, pool_pre_ping=True)

def render_insight(observation, interpretation, impact):
    st.info(f"**Observation**: {observation}\n\n**Interpretation**: {interpretation}\n\n**Business Impact**: {impact}", icon="💡")

st.markdown('<div class="main-title">Cart2Insights Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">E-Commerce Sales, Delivery, and Customer Experience Analytics</div>', unsafe_allow_html=True)

st.sidebar.title("Navigation")
section = st.sidebar.selectbox(
    "Choose Analysis View:",
    [
        "Business Overview",
        "Sales Analysis",
        "Customer Analysis",
        "Seller & Product Analysis",
        "Delivery Analysis",
        "Customer Experience"
    ]
)

engine = get_engine()

if section == "Business Overview":
    st.markdown('<div class="section-title">1. Business Overview</div>', unsafe_allow_html=True)
    
    query_overview = """
    SELECT
        (SELECT SUM(price + freight_value) FROM order_items) as total_revenue,
        (SELECT COUNT(DISTINCT order_id) FROM orders) as total_orders,
        (SELECT COUNT(DISTINCT customer_unique_id) FROM customers) as total_customers,
        (SELECT COUNT(DISTINCT seller_id) FROM sellers) as total_sellers,
        (SELECT SUM(price + freight_value) / COUNT(DISTINCT order_id) FROM order_items) as average_order_value,
        (SELECT AVG(review_score) FROM order_reviews) as average_review_score
    """
    overview_df = pd.read_sql(query_overview, engine)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"₹{overview_df['total_revenue'].iloc[0]:,.2f}")
    col2.metric("Total Orders", f"{overview_df['total_orders'].iloc[0]:,}")
    col3.metric("Total Customers", f"{overview_df['total_customers'].iloc[0]:,}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    col4.metric("Total Sellers", f"{overview_df['total_sellers'].iloc[0]:,}")
    col5.metric("Average Order Value", f"₹{overview_df['average_order_value'].iloc[0]:,.2f}")
    col6.metric("Average Review Score", f"{overview_df['average_review_score'].iloc[0]:.2f} / 5.0")
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_insight(
        "The platform generated over ₹15.8M in revenue across nearly 100k orders, maintaining a healthy 4.0+ average review score.",
        "While aggregate volume is high, the Average Order Value (AOV) is relatively modest at ₹160, pointing to a high-frequency, mass-market consumer base.",
        "Implement minimum-cart-value thresholds for free shipping and product bundling strategies to organically increase the AOV."
    )

elif section == "Sales Analysis":
    st.markdown('<div class="section-title">2. Sales Analysis</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Monthly Trend & Categories", "Top Products", "Sales by Location"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            query_monthly = """
            SELECT 
                DATE_FORMAT(o.order_purchase_timestamp, '%%Y-%%m') as Month,
                SUM(oi.price + oi.freight_value) as Revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.order_purchase_timestamp IS NOT NULL
            GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%%Y-%%m')
            ORDER BY Month
            """
            monthly_sales = pd.read_sql(query_monthly, engine)
            fig_monthly = px.line(monthly_sales, x="Month", y="Revenue", markers=True, title="Monthly Revenue Trend", line_shape="spline")
            st.plotly_chart(fig_monthly, use_container_width=True)
            
        with col2:
            query_category = """
            SELECT 
                COALESCE(ct.product_category_name_english, p.product_category_name) as Category,
                SUM(oi.price) as Revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            LEFT JOIN category_translation ct ON p.product_category_name = ct.product_category_name
            GROUP BY Category
            ORDER BY Revenue DESC
            LIMIT 10
            """
            category_sales = pd.read_sql(query_category, engine)
            fig_category = px.bar(category_sales, x="Revenue", y="Category", orientation='h', title="Revenue by Category").update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_category, use_container_width=True)
            
        render_insight(
            "Revenue shows sharp upward momentum towards the end of the year, driven heavily by lifestyle categories like Health & Beauty and Bed/Bath.",
            "Black Friday and Q4 holiday shopping are the primary drivers of annual revenue volume for lifestyle consumer goods.",
            "Ensure inventory caching, server capacity, and aggressive marketing campaigns are scaled specifically for the Q4 surge in top categories."
        )

    with tab2:
        query_top_prod = """
        SELECT product_id as 'Product ID', SUM(price) as Revenue
        FROM order_items
        GROUP BY product_id
        ORDER BY Revenue DESC
        LIMIT 15
        """
        top_products = pd.read_sql(query_top_prod, engine)
        top_products['Product ID'] = top_products['Product ID'].str[:8] + '...'
        fig_prod = px.bar(top_products, x="Product ID", y="Revenue", title="Top-Selling Products")
        st.plotly_chart(fig_prod, use_container_width=True)
        render_insight(
            "A small subset of specific SKUs generates a highly disproportionate amount of the platform's product revenue.",
            "Consumers are relying on the platform for specific 'hero' products rather than diverse cart building.",
            "Feature these top-selling SKUs prominently in acquisition ads to lower Customer Acquisition Cost (CAC)."
        )

    with tab3:
        query_location = """
        SELECT c.customer_state as State, SUM(oi.price + oi.freight_value) as Revenue
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY c.customer_state
        ORDER BY Revenue DESC
        """
        location_sales = pd.read_sql(query_location, engine)
        fig_loc = px.bar(location_sales, x="State", y="Revenue", title="Sales by Location")
        st.plotly_chart(fig_loc, use_container_width=True)
        render_insight(
            "A few major states (like SP and RJ) account for a disproportionately large share of total revenue.",
            "E-commerce penetration and customer density are heavily localized to primary urban and economic centers.",
            "Optimize logistics hubs and regional fulfillment centers near these top-performing states to reduce average freight costs and delivery times."
        )

elif section == "Customer Analysis":
    st.markdown('<div class="section-title">3. Customer Analysis</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Distribution & Spending", "Retention & VIPs"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            query_cust_dist = """
            SELECT customer_state as State, COUNT(DISTINCT customer_unique_id) as Customers
            FROM customers
            GROUP BY customer_state
            ORDER BY Customers DESC
            LIMIT 15
            """
            cust_dist = pd.read_sql(query_cust_dist, engine)
            fig_dist = px.bar(cust_dist, x="State", y="Customers", title="Customer Distribution")
            st.plotly_chart(fig_dist, use_container_width=True)
        with col2:
            query_spending = """
            SELECT c.customer_unique_id, SUM(oi.price + oi.freight_value) as Customer_Spending
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY c.customer_unique_id
            """
            customer_spending = pd.read_sql(query_spending, engine)
            fig_spend = px.histogram(customer_spending, x="Customer_Spending", nbins=50, title="Customer Spending", range_x=[0, 1000])
            st.plotly_chart(fig_spend, use_container_width=True)
            
        render_insight(
            "Customer lifetime spend is heavily right-skewed, with the vast majority spending under ₹200, matching the geographic concentration in SP.",
            "The platform attracts budget-conscious shoppers in major hubs, but struggles to generate high lifetime value per average user.",
            "Introduce tiered loyalty rewards (e.g., free shipping on next order) to incentivize customers in the ₹100-200 bracket to cross the ₹500 threshold."
        )

    with tab2:
        col1, col2 = st.columns([1, 2])
        with col1:
            query_repeat = """
            WITH OrderCounts AS (
                SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) as order_count
                FROM customers c
                JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_unique_id
            )
            SELECT 
                CASE WHEN order_count > 1 THEN 'Repeat' ELSE 'New' END as 'Type',
                COUNT(*) as Customers
            FROM OrderCounts
            GROUP BY CASE WHEN order_count > 1 THEN 'Repeat' ELSE 'New' END
            """
            repeat_data = pd.read_sql(query_repeat, engine)
            fig_repeat = px.pie(repeat_data, names="Type", values="Customers", hole=0.4, title="Repeat vs New Customers")
            st.plotly_chart(fig_repeat, use_container_width=True)
        with col2:
            query_top_cust = """
            SELECT 
                c.customer_unique_id as 'Customer ID',
                COUNT(DISTINCT o.order_id) as 'Orders',
                SUM(oi.price + oi.freight_value) as 'Total Spending',
                SUM(oi.price + oi.freight_value) / COUNT(DISTINCT o.order_id) as 'AOV'
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY c.customer_unique_id
            HAVING SUM(oi.price + oi.freight_value) > 0
            ORDER BY SUM(oi.price + oi.freight_value) DESC
            LIMIT 8
            """
            top_cust_df = pd.read_sql(query_top_cust, engine)
            st.markdown("##### Top Customers")
            st.dataframe(top_cust_df, use_container_width=True, hide_index=True)

        render_insight(
            "The customer base is composed almost entirely of new, one-time buyers, yet a microscopic segment of VIPs orders frequently and spends heavily.",
            "Customer acquisition is excellent, but post-purchase retention and brand loyalty are critical weaknesses.",
            "Implement automated post-purchase email flows with targeted discounts for second purchases to convert one-time buyers."
        )

elif section == "Seller & Product Analysis":
    st.markdown('<div class="section-title">4. Seller & Product Analysis</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Seller Performance", "Product Categories & Ratings"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            query_top_sellers = """
            SELECT seller_id as 'Seller ID', SUM(price) as Revenue
            FROM order_items
            GROUP BY seller_id
            ORDER BY Revenue DESC
            LIMIT 10
            """
            top_sellers = pd.read_sql(query_top_sellers, engine)
            top_sellers['Seller ID'] = top_sellers['Seller ID'].str[:8] + '...'
            fig_top_sellers = px.bar(top_sellers, x="Revenue", y="Seller ID", orientation='h', title="Top Sellers").update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_top_sellers, use_container_width=True)
            
        with col2:
            query_seller_rev = """
            SELECT seller_id as 'Seller ID', SUM(price) as Revenue
            FROM order_items
            GROUP BY seller_id
            """
            seller_rev = pd.read_sql(query_seller_rev, engine)
            fig_seller_rev = px.histogram(seller_rev, x="Revenue", nbins=40, title="Seller Revenue Distribution", range_x=[0, 20000])
            st.plotly_chart(fig_seller_rev, use_container_width=True)
            
        render_insight(
            "Platform revenue is highly concentrated among a small fraction of top-performing sellers.",
            "The Pareto principle heavily dictates marketplace success; the vast majority of registered sellers generate minimal traction.",
            "Offer exclusive contracts to top sellers to prevent churn to competitors, and implement training programs for mid-tier sellers."
        )

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            query_cat_perf = """
            SELECT 
                COALESCE(ct.product_category_name_english, p.product_category_name) as Category, 
                COUNT(oi.order_item_id) as Volume
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            LEFT JOIN category_translation ct ON p.product_category_name = ct.product_category_name
            GROUP BY Category
            ORDER BY Volume DESC
            LIMIT 10
            """
            cat_perf = pd.read_sql(query_cat_perf, engine)
            fig_cat_perf = px.bar(cat_perf, x="Category", y="Volume", title="Product/Category Performance (Volume)")
            st.plotly_chart(fig_cat_perf, use_container_width=True)
            
        with col2:
            query_seller_ratings = """
            SELECT 
                oi.seller_id as 'Seller ID',
                AVG(r.review_score) as 'Average Rating',
                COUNT(r.review_id) as 'Number of Reviews'
            FROM order_items oi
            JOIN order_reviews r ON oi.order_id = r.order_id
            GROUP BY oi.seller_id
            HAVING COUNT(r.review_id) >= 50
            ORDER BY AVG(r.review_score) DESC
            LIMIT 10
            """
            seller_ratings = pd.read_sql(query_seller_ratings, engine)
            seller_ratings['Seller ID'] = seller_ratings['Seller ID'].str[:8] + '...'
            fig_seller_ratings = px.bar(seller_ratings, x="Average Rating", y="Seller ID", orientation='h', title="Seller Ratings (>50 reviews)", range_x=[4.5, 5.0]).update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_seller_ratings, use_container_width=True)
            
        render_insight(
            "Top volume categories differ slightly from top revenue categories, while elite sellers maintain near 5.0 ratings at high volumes.",
            "High operational standards, fast fulfillment, and accurate product descriptions reliably drive top tier reviews.",
            "Create a 'Top Seller' programmatic boost to reward partners with >4.8 ratings with higher search visibility."
        )

elif section == "Delivery Analysis":
    st.markdown('<div class="section-title">5. Delivery Analysis</div>', unsafe_allow_html=True)
    
    query_avg_del = """
    SELECT AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)) as avg_delivery
    FROM orders
    WHERE order_delivered_customer_date IS NOT NULL
    """
    avg_delivery = pd.read_sql(query_avg_del, engine).iloc[0, 0]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Average Delivery Time", f"{avg_delivery:.2f} days")
        
        query_delivery_status = """
        WITH DeliveryDiff AS (
            SELECT 
                DATEDIFF(order_delivered_customer_date, order_estimated_delivery_date) as delay_days
            FROM orders
            WHERE order_delivered_customer_date IS NOT NULL
        )
        SELECT 
            CASE WHEN delay_days > 0 THEN 'Delayed' ELSE 'On Time' END as 'Status',
            COUNT(*) as Orders
        FROM DeliveryDiff
        GROUP BY CASE WHEN delay_days > 0 THEN 'Delayed' ELSE 'On Time' END
        """
        delivery_status = pd.read_sql(query_delivery_status, engine)
        fig_status = px.pie(delivery_status, names="Status", values="Orders", hole=0.4, title="On-time vs Delayed Orders", color="Status", color_discrete_map={"On Time":"#10B981", "Delayed":"#EF4444"})
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        query_loc_perf = """
        SELECT 
            c.customer_state as State,
            AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)) as 'Average Delivery Days'
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_delivered_customer_date IS NOT NULL
        GROUP BY c.customer_state
        ORDER BY 'Average Delivery Days' DESC
        """
        loc_perf = pd.read_sql(query_loc_perf, engine)
        fig_loc_perf = px.bar(loc_perf, x="State", y="Average Delivery Days", title="Delivery Performance by Location")
        st.plotly_chart(fig_loc_perf, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    
    query_delay_review = """
    SELECT 
        DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date) as delivery_delay_days,
        r.review_score as review_score
    FROM orders o
    JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_delivered_customer_date IS NOT NULL
    AND DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date) > 0
    """
    delay_review = pd.read_sql(query_delay_review, engine)
    fig_delay = px.scatter(delay_review, x="delivery_delay_days", y="review_score", title="Delivery Delay vs Review Score", opacity=0.3)
    fig_delay.update_layout(xaxis_title="Delivery Delay (Days)", yaxis_title="Review Score")
    st.plotly_chart(fig_delay, use_container_width=True)
    
    render_insight(
        "While 90%+ of orders arrive on time, states further from economic hubs suffer long transit times. Furthermore, as delays stretch, reviews plummet to 1 star.",
        "Customers harshly penalize late deliveries regardless of product quality, linking satisfaction directly to fulfillment reliability.",
        "Audit 3PL carrier SLAs in high-delay regions, flag at-risk shipments for proactive customer service recovery, and set dynamic, realistic shipping estimates."
    )

elif section == "Customer Experience":
    st.markdown('<div class="section-title">6. Customer Experience</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        query_score_dist = """
        SELECT review_score as 'Review Score', COUNT(*) as Orders
        FROM order_reviews
        GROUP BY review_score
        ORDER BY review_score
        """
        score_dist = pd.read_sql(query_score_dist, engine)
        fig_scores = px.bar(score_dist, x="Review Score", y="Orders", title="Review Score Distribution")
        st.plotly_chart(fig_scores, use_container_width=True)
        
        render_insight(
            "Reviews are highly polarized (mostly 5s, with a severe secondary spike at 1s).",
            "Customers typically only leave reviews when extremely satisfied or when experiencing a critical failure (like severe delay or damage).",
            "Incentivize reviews from the 'silent majority' to naturally dilute the impact of the 1-star extreme."
        )
        
    with col2:
        query_rating_del = """
        SELECT 
            r.review_score as 'Review Score',
            AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)) as 'Average Delivery Days'
        FROM orders o
        JOIN order_reviews r ON o.order_id = r.order_id
        WHERE o.order_delivered_customer_date IS NOT NULL
        GROUP BY r.review_score
        ORDER BY r.review_score
        """
        rating_delivery = pd.read_sql(query_rating_del, engine)
        fig_rating_del = px.line(rating_delivery, x="Review Score", y="Average Delivery Days", markers=True, title="Rating vs Delivery Performance")
        fig_rating_del.update_traces(line_color="#EF4444")
        st.plotly_chart(fig_rating_del, use_container_width=True)
        
        render_insight(
            "5-star reviews systematically correlate with the lowest average delivery times.",
            "Speed of delivery is a primary, overriding driver of positive customer sentiment.",
            "Optimize fulfillment workflows for faster turnaround times and consider subsidizing expedited shipping options for high-margin products."
        )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    query_cat_reviews = """
    WITH RankedCategories AS (
        SELECT 
            COALESCE(ct.product_category_name_english, p.product_category_name) as Category,
            AVG(r.review_score) as Avg_Rating,
            COUNT(r.review_id) as vol
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        LEFT JOIN category_translation ct ON p.product_category_name = ct.product_category_name
        JOIN order_reviews r ON oi.order_id = r.order_id
        GROUP BY Category
    )
    SELECT Category, Avg_Rating as 'Average Rating'
    FROM RankedCategories
    WHERE Category IS NOT NULL AND vol > 100
    ORDER BY Avg_Rating ASC
    LIMIT 15
    """
    cat_reviews = pd.read_sql(query_cat_reviews, engine)
    fig_cat_rev = px.bar(cat_reviews, x="Average Rating", y="Category", orientation='h', title="Reviews by Category (Bottom 15 by Rating, High Volume)", range_x=[3.0, 4.2]).update_yaxes(categoryorder="total descending")
    st.plotly_chart(fig_cat_rev, use_container_width=True)

    render_insight(
        "Certain high-volume categories like Office Furniture and Telephony consistently rate much lower than the platform average.",
        "Bulky, fragile, or complex products likely suffer from shipping damage or mismatched customer expectations upon assembly.",
        "Enforce stricter protective packaging guidelines for sellers in these categories and mandate clearer product description dimensions/assembly requirements."
    )