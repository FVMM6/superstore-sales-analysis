import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicates:", df.duplicated().sum())

df = df.drop_duplicates().copy()

print("\nTotal sales:", df["Sales"].sum())
print("Total profit:", df["Profit"].sum())
print("Categories:", df["Category"].unique())

profit_by_category = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
sales_by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
loss_rows = df[df["Profit"] < 0]
top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)

print("\nProfit by category:")
print(profit_by_category)

print("\nSales by region:")
print(sales_by_region)

print("\nLoss-making rows:", len(loss_rows))

print("\nTop products by sales:")
print(top_products)

sns.set_theme(style="whitegrid")

plt.figure(figsize=(8, 5))
sns.barplot(x=profit_by_category.index, y=profit_by_category.values, hue=profit_by_category.index, palette="Blues_d", legend=False)
plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.barplot(x=sales_by_region.index, y=sales_by_region.values, hue=sales_by_region.index, palette="Greens_d", legend=False)
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(df["Profit"], bins=40, kde=True, color="#C44E52")
plt.title("Profit Distribution")
plt.xlabel("Profit")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
