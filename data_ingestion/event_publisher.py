import os
from azure.eventhub import EventHubProducerClient, EventData
import json
import uuid

# Get connection string from environment variables
CONNECTION_STR = os.environ["EVENT_HUBS_CONNECTION_STR"]
EVENTHUB_NAME = os.environ["EVENT_HUB_NAME"]

def publish_trade_event(trade_data: dict):
    """Publishes a trade event to Azure Event Hubs."""
    
    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        eventhub_name=EVENTHUB_NAME
    )
    
    with producer:
        # Create a batch
        event_data_batch = producer.create_batch()
        
        # Serialize data to JSON and add to the batch
        payload = json.dumps(trade_data)
        event_data_batch.add(EventData(payload))
        
        # Send the batch of events to the event hub
        producer.send_batch(event_data_batch)
    
    print(f"Published trade event with data: {trade_data['tradeId']}")

# Example usage
if __name__ == "__main__":
    sample_trade = {
        "tradeId": "TRD-12345",
        "symbol": "AAPL",
        "quantity": 100,
        "price": 150.75,
        "portfolioId": "PORT-987",
        "timestamp": "2025-09-02T10:00:00Z"
    }
    publish_trade_event(sample_trade)