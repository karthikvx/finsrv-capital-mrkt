-- Create a stream to track new files in the external table
CREATE OR REPLACE STREAM trades_ext_stream ON EXTERNAL TABLE trades_ext;

-- Create a materialized view for pre-aggregated data
CREATE OR REPLACE MATERIALIZED VIEW portfolio_risk_mv AS
SELECT
  portfolioId,
  AVG(risk_score) AS avg_risk_score,
  SUM(quantity) AS total_quantity
FROM trades_ext
GROUP BY 1;

-- Create a task to refresh the materialized view when new data arrives
CREATE OR REPLACE TASK refresh_risk_mv
  WAREHOUSE = 'ANALYTICS_WH'
  WHEN SYSTEM$STREAM_HAS_DATA('trades_ext_stream')
AS
  BEGIN
    -- This simply refreshes the materialized view.
    -- Snowflake handles the incremental update automatically.
    REFRESH MATERIALIZED VIEW portfolio_risk_mv;
  END;

-- Resume the task
ALTER TASK refresh_risk_mv RESUME;