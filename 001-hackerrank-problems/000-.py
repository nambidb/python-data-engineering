from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum
from pyspark.sql.types import IntegerType

spark = SparkSession.builder.appName("ETL_Pipeline").getOrCreate()

# --------------------------------------------------------
# Step 1: Local file paths
# --------------------------------------------------------

orders_path = "orders.csv"
products_path = "products.csv"

# (Optional) Use absolute paths if needed
# orders_path = r"C:\Users\jnamb\PycharmProjects\PythonProject1\orders.csv"
# products_path = r"C:\Users\jnamb\PycharmProjects\PythonProject1\products.csv"

# --------------------------------------------------------
# Step 2: Read CSV using Spark
# --------------------------------------------------------

orders_df = spark.read.csv(orders_path, header=True, inferSchema=True)
products_df = spark.read.csv(products_path, header=True, inferSchema=True)

# --------------------------------------------------------
# Step 3: Cleaning
# --------------------------------------------------------

orders_df = orders_df.fillna({"quantity": 1})
orders_df = orders_df.withColumn("quantity", col("quantity").cast(IntegerType()))

products_df = products_df.fillna({"category": "unknown"})

# --------------------------------------------------------
# Step 4: Join
# --------------------------------------------------------

merged_df = orders_df.join(products_df, on="product_id", how="inner")

# --------------------------------------------------------
# Step 5: Derived column
# --------------------------------------------------------

merged_df = merged_df.withColumn("revenue", col("quantity") * col("price"))

# --------------------------------------------------------
# Step 6: Aggregation
# --------------------------------------------------------

agg_df = (
    merged_df.groupBy("category")
    .agg(spark_sum("revenue").alias("total_revenue"))
    .orderBy(col("total_revenue").desc())
)

# --------------------------------------------------------
# Step 7: Output
# --------------------------------------------------------

agg_df.show(truncate=False)
