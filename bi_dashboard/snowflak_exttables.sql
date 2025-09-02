-- Snowflake SQL for Azure
-- First, create a storage integration for Azure
CREATE OR REPLACE STORAGE INTEGRATION azure_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = AZURE
  ENABLED = TRUE
  AZURE_TENANT_ID = '<your_azure_tenant_id>'
  STORAGE_ALLOWED_LOCATIONS = ('azure://<your_storage_account>.blob.core.windows.net/<your_container>/');

-- Then, create the external table pointing to ADLS
CREATE OR REPLACE EXTERNAL TABLE trades_ext (
  tradeId VARCHAR AS (VALUE:tradeId::VARCHAR),
  symbol VARCHAR AS (VALUE:symbol::VARCHAR),
  quantity INT AS (VALUE:quantity::INT),
  risk_score DOUBLE AS (VALUE:risk_score::DOUBLE)
)
WITH LOCATION = @trade_data_adls_stage/trades/
  FILE_FORMAT = (TYPE = PARQUET)
  AUTO_REFRESH = TRUE -- This automatically creates a notification integration in Azure
  -- Use the newly created storage integration
  STORAGE_INTEGRATION = azure_int;