import os
import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.eventhub import EventHubManagementClient

# Setup logging
logging.basicConfig(level=logging.INFO)

def check_dlq_size(subscription_id, resource_group_name, namespace_name, event_hub_name):
    """Checks the dead-letter queue size for an Event Hub."""
    
    try:
        credential = DefaultAzureCredential()
        client = EventHubManagementClient(credential, subscription_id)
        
        # DLQ is often a separate entity within the same namespace
        dlq_path = f"{event_hub_name}/$DeadLetterQueue"
        
        # Get runtime info for the Event Hub (which includes the DLQ)
        eh_info = client.event_hubs.get(resource_group_name, namespace_name, event_hub_name)
        
        # This is a conceptual check; the actual metric might be different
        # A more robust approach uses Azure Monitor Metrics API
        dlq_size = get_dlq_size_from_metrics(subscription_id, resource_group_name, namespace_name, event_hub_name)
        
        if dlq_size > 50:
            logging.warning(f"URGENT: Dead-letter queue for '{event_hub_name}' has grown to {dlq_size} messages. Manual intervention is required.")
        else:
            logging.info(f"Dead-letter queue for '{event_hub_name}' is healthy with {dlq_size} messages.")

    except Exception as e:
        logging.error(f"Failed to check DLQ size: {e}")

def get_dlq_size_from_metrics(sub_id, rg_name, ns_name, eh_name):
    """
    Conceptual function to get DLQ size from Azure Monitor Metrics.
    In a real scenario, this would involve the azure.mgmt.monitor library.
    """
    # Replace with real API call
    return 65 

if __name__ == "__main__":
    check_dlq_size(
        os.getenv("AZURE_SUBSCRIPTION_ID"),
        "FinTechRG",
        "FinTechEventHubsNamespace",
        "trade-execution-hub"
    )