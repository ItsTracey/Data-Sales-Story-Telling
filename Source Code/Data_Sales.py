import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the dataset
df = pd.read_csv("sales_data_storytelling.csv", delimiter=";")

# Convert Month to datetime format
df["Month"] = pd.to_datetime(df["Month"])

###################################### Question 1 ######################################
# Group by month and sum the revenue
monthly_revenue = df.groupby(pd.Grouper(key="Month", freq="M"))["Revenue"].sum()

# Identify peak and low-performing months
peak_month = monthly_revenue.idxmax()
low_month = monthly_revenue.idxmin()
peak_value = monthly_revenue.max()
low_value = monthly_revenue.min()

# Plot the revenue trend

plt.plot(monthly_revenue.index, monthly_revenue.values, marker="*", linestyle="dotted", color="#008B8B", label="Revenue")
plt.scatter(peak_month, peak_value, color="green", marker="o", s=100, label="Peak Month")
plt.scatter(low_month, low_value, color="red", marker="o", s=100, label="Low Month")
plt.axhline(peak_value, color="green", linestyle="dashed", alpha=0.6)
plt.axhline(low_value, color="red", linestyle="dashed", alpha=0.6)
plt.xticks(monthly_revenue.index, monthly_revenue.index.strftime("%B"), rotation=45)
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.title("Revenue Trend with Peak and Low-Performing Months")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("Question1.png")
plt.show()

print(f"Peak Month: {peak_month.strftime('%B')}, Lowest Month: {low_month.strftime('%B')}")


###################################### Question 2 ######################################
# Group data by product and calculate average revenue
revenue_per_product = df.groupby("Product")["Revenue"].mean().sort_values(ascending=False)

colors = plt.cm.Set3(np.linspace(0, 1, len(revenue_per_product)))
# Plot bar chart
plt.barh(revenue_per_product.index, revenue_per_product.values, color=colors)
plt.xlabel("Average Revenue")
plt.ylabel("Product")
plt.title("Average Revenue per Product")
plt.gca().invert_yaxis()
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.savefig("Question2.png")
plt.show()

# Identify best-selling product
best_selling = revenue_per_product.idxmax()
print(f"Best-selling product: {best_selling}")

###################################### Question 3######################################
# Calculate total revenue per product
revenue_per_product = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)

# Identify the top product
top_product_index = 0  # The first product in sorted order is the highest
explode_values = [0.1 if i == top_product_index else 0 for i in range(len(revenue_per_product))]  # Explode top product

# Plot pie chart with the largest sales contribution highlighted
plt.figure(figsize=(8, 8))
plt.pie(
    revenue_per_product.values,
    labels=revenue_per_product.index,
    autopct='%1.1f%%',
    colors=plt.cm.Set3.colors,
    explode=explode_values,  # Separate the top product
    shadow=True,
    startangle=140
)
plt.title("Sales Contribution of Each Product Over the Year")
plt.savefig("Question3.png")
plt.show()

# Print the top-selling product
top_product = revenue_per_product.idxmax()
print(f"Largest Sales Contribution: {top_product}")


###################################### Question 4 ######################################

avg_revenue = monthly_revenue.mean()
std_dev = monthly_revenue.std()

upper_bound = avg_revenue + (1.0 * std_dev)
lower_bound = avg_revenue - (1.0 * std_dev)

anomalies = monthly_revenue[(monthly_revenue > upper_bound) | (monthly_revenue < lower_bound)]

plt.plot(monthly_revenue.index, monthly_revenue.values, marker="o", linestyle="dotted", color="#008B8B", label="Revenue")
plt.scatter(anomalies.index, anomalies.values, color="red", label="Anomalies", zorder=3)
plt.axhline(avg_revenue, color="gray", linestyle="dashed", label="Avg Revenue")

# Fix x-axis labels to display full month names
plt.xticks(monthly_revenue.index, monthly_revenue.index.strftime("%B"), rotation=45)

plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.title("Revenue Trend with Anomalies")
plt.legend()
plt.grid(True)
plt.savefig("Question4.png")
plt.show()

print("Anomaly Months:\n", anomalies)
