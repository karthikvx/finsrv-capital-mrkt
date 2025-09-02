-- Identify top 10 most expensive queries in the last 24 hours
-- This helps in performance tuning and cost control
SELECT
  query_text,
  execution_time / 1000 AS execution_time_seconds,
  credits_used_cloud_services,
  user_name,
  warehouse_name
FROM
  snowflake.account_usage.query_history
WHERE
  start_time >= DATEADD(day, -1, CURRENT_TIMESTAMP())
ORDER BY
  credits_used_cloud_services DESC
LIMIT 10;

-- Suspend a warehouse if it's not active to save costs
-- This is a common task for maintenance
ALTER WAREHOUSE ANALYTICS_WH SUSPEND;

-- Resume a warehouse
ALTER WAREHOUSE ANALYTICS_WH RESUME;

-- List all tasks and their status
-- Helps in monitoring the ETL/ELT pipeline
SHOW TASKS;