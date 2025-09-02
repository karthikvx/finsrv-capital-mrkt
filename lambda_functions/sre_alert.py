# Azure Function (Python) triggered by an HTTP request from an Azure Monitor Alert
import logging
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
             "Please pass a JSON object in the request body",
             status_code=400
        )
    
    # Extract data from the Azure Monitor Alert payload
    alert_name = req_body.get('data', {}).get('essentials', {}).get('alertRule', '')
    alert_state = req_body.get('data', {}).get('essentials', {}).get('monitorCondition', '')
    
    message = f"Azure Monitor Alert '{alert_name}' has changed to state '{alert_state}'. A sudden spike in query latency has been detected in Snowflake. SRE team should investigate immediately."
    
    # You can now send this message to an Azure service like Logic Apps, Teams, or Service Bus
    # For a simple example, we'll just log it. In a real-world scenario, you'd integrate with a PagerDuty or Slack webhook.
    logging.warning(f"SRE Alert: {message}")
    
    return func.HttpResponse(f"Alert handled successfully!", status_code=200)