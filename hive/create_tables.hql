CREATE EXTERNAL TABLE IF NOT EXISTS sentiment_results (
  text STRING,
  sentiment STRING
)
STORED AS PARQUET
LOCATION '/data/outputs/sentiment_results';