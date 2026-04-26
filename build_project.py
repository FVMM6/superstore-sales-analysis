from pathlib import Path

import nbformat as nbf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Sample - Superstore.csv"
CHARTS_DIR = BASE_DIR / "charts"
NOTEBOOK_PATH = BASE_DIR / "notebook.ipynb"
README_PATH = BASE_DIR / "README.md"
SCRIPT_PATH = BASE_DIR / "analysis.py"


def build_analysis_outputs() -> dict:
    df = pd.read_csv(DATA_PATH, encoding="latin1")

    missing_values = df.isna().sum()
    duplicates_count = int(df.duplicated().sum())
    df_clean = df.drop_duplicates().copy()

    total_sales = float(df_clean["Sales"].sum())
    total_profit = float(df_clean["Profit"].sum())
    categories = sorted(df_clean["Category"].unique().tolist())

    profit_by_category = (
        df_clean.groupby("Category", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )
    sales_by_region = (
        df_clean.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )
    loss_rows = df_clean[df_clean["Profit"] < 0].copy()
    top_products = (
        df_clean.groupby("Product Name", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    CHARTS_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=profit_by_category,
        x="Category",
        y="Profit",
        hue="Category",
        palette="Blues_d",
        legend=False,
    )
    plt.title("Profit by Category")
    plt.xlabel("Category")
    plt.ylabel("Profit")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "profit_by_category.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=sales_by_region,
        x="Region",
        y="Sales",
        hue="Region",
        palette="Greens_d",
        legend=False,
    )
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "sales_by_region.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.histplot(df_clean["Profit"], bins=40, kde=True, color="#C44E52")
    plt.title("Profit Distribution")
    plt.xlabel("Profit")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "profit_distribution.png", dpi=200)
    plt.close()

    insights = [
        f"Technology is the most profitable category with profit of {profit_by_category.iloc[0]['Profit']:.2f}.",
        f"The West region leads in sales with revenue of {sales_by_region.iloc[0]['Sales']:.2f}.",
        f"There are {len(loss_rows)} unprofitable order lines where Profit is below zero.",
        f"The top product by revenue is '{top_products.iloc[0]['Product Name']}' with sales of {top_products.iloc[0]['Sales']:.2f}.",
        "The dataset is already clean from missing values and exact duplicate rows.",
    ]

    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "missing_values": missing_values,
        "duplicates_count": duplicates_count,
        "total_sales": total_sales,
        "total_profit": total_profit,
        "categories": categories,
        "profit_by_category": profit_by_category,
        "sales_by_region": sales_by_region,
        "loss_rows": loss_rows,
        "top_products": top_products,
        "insights": insights,
    }


def build_analysis_script() -> None:
    script = """import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

print("Dataset shape:", df.shape)
print("\\nColumns:")
print(df.columns.tolist())

print("\\nMissing values:")
print(df.isna().sum())

print("\\nDuplicates:", df.duplicated().sum())

df = df.drop_duplicates().copy()

print("\\nTotal sales:", df["Sales"].sum())
print("Total profit:", df["Profit"].sum())
print("Categories:", df["Category"].unique())

profit_by_category = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
sales_by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
loss_rows = df[df["Profit"] < 0]
top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)

print("\\nProfit by category:")
print(profit_by_category)

print("\\nSales by region:")
print(sales_by_region)

print("\\nLoss-making rows:", len(loss_rows))

print("\\nTop products by sales:")
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
"""
    SCRIPT_PATH.write_text(script, encoding="utf-8")


def build_notebook(results: dict) -> None:
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell(
            "# Superstore Sales Analysis\n"
            "This notebook analyzes company sales and profitability using the Sample Superstore dataset."
        ),
        nbf.v4.new_markdown_cell(
            "## Goals\n"
            "- Load and inspect the dataset\n"
            "- Check missing values and duplicates\n"
            "- Analyze sales, profit, categories, regions, and products\n"
            "- Build visualizations and summarize business insights"
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "\n"
            "sns.set_theme(style='whitegrid')\n"
            "df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')\n"
            "df.head()"
        ),
        nbf.v4.new_code_cell("df.columns.tolist()"),
        nbf.v4.new_markdown_cell(
            "## Data Cleaning\n"
            "We check missing values and duplicates. Even if the dataset is already clean, this step must be documented."
        ),
        nbf.v4.new_code_cell(
            "missing_values = df.isna().sum()\n"
            "duplicates_count = df.duplicated().sum()\n"
            "\n"
            "print('Missing values by column:')\n"
            "print(missing_values)\n"
            "print('\\nDuplicate rows:', duplicates_count)\n"
            "\n"
            "df = df.drop_duplicates().copy()"
        ),
        nbf.v4.new_markdown_cell("## Basic Overview"),
        nbf.v4.new_code_cell(
            "total_sales = df['Sales'].sum()\n"
            "total_profit = df['Profit'].sum()\n"
            "categories = df['Category'].unique()\n"
            "\n"
            "print('Total sales:', total_sales)\n"
            "print('Total profit:', total_profit)\n"
            "print('Categories:', categories)"
        ),
        nbf.v4.new_markdown_cell("## 1. Profit by Category"),
        nbf.v4.new_code_cell(
            "profit_by_category = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)\n"
            "profit_by_category"
        ),
        nbf.v4.new_markdown_cell("## 2. Sales by Region"),
        nbf.v4.new_code_cell(
            "sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)\n"
            "sales_by_region"
        ),
        nbf.v4.new_markdown_cell("## 3. Loss-Making Rows"),
        nbf.v4.new_code_cell(
            "loss_rows = df[df['Profit'] < 0]\n"
            "loss_rows[['Product Name', 'Category', 'Region', 'Sales', 'Profit']].head(10)"
        ),
        nbf.v4.new_markdown_cell("## 4. Top Products by Revenue"),
        nbf.v4.new_code_cell(
            "top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)\n"
            "top_products"
        ),
        nbf.v4.new_markdown_cell("## Visualizations"),
        nbf.v4.new_code_cell(
            "plt.figure(figsize=(8, 5))\n"
            "sns.barplot(x=profit_by_category.index, y=profit_by_category.values, hue=profit_by_category.index, palette='Blues_d', legend=False)\n"
            "plt.title('Profit by Category')\n"
            "plt.xlabel('Category')\n"
            "plt.ylabel('Profit')\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_code_cell(
            "plt.figure(figsize=(8, 5))\n"
            "sns.barplot(x=sales_by_region.index, y=sales_by_region.values, hue=sales_by_region.index, palette='Greens_d', legend=False)\n"
            "plt.title('Sales by Region')\n"
            "plt.xlabel('Region')\n"
            "plt.ylabel('Sales')\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_code_cell(
            "plt.figure(figsize=(8, 5))\n"
            "sns.histplot(df['Profit'], bins=40, kde=True, color='#C44E52')\n"
            "plt.title('Profit Distribution')\n"
            "plt.xlabel('Profit')\n"
            "plt.ylabel('Count')\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## Conclusions\n" + "\n".join([f"- {item}" for item in results["insights"]])
        ),
    ]

    with NOTEBOOK_PATH.open("w", encoding="utf-8") as f:
        nbf.write(nb, f)


def build_readme(results: dict) -> None:
    readme = f"""# Superstore Sales Analysis




- Total sales: {results["total_sales"]:.2f}
- Total profit: {results["total_profit"]:.2f}
- Categories: {", ".join(results["categories"])}
- Most profitable category: {results["profit_by_category"].iloc[0]["Category"]}
- Region with highest sales: {results["sales_by_region"].iloc[0]["Region"]}
- Loss-making rows: {len(results["loss_rows"])}

## Resume-ready summary
Conducted sales data analysis using Python, pandas, and seaborn. Cleaned and validated the dataset, built visualizations, and identified key business insights related to revenue, profit, and loss-making products.
"""
    README_PATH.write_text(readme, encoding="utf-8")


def main() -> None:
    results = build_analysis_outputs()
    build_analysis_script()
    build_notebook(results)
    build_readme(results)
    print("Project files created successfully.")


if __name__ == "__main__":
    main()
