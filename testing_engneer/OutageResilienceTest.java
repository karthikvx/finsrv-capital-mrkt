// A conceptual code snippet showing how the Spring Boot app would handle the outage
// The code itself doesn't cause the outage, but shows the handling logic.
// The consumer client automatically manages reconnections.

import com.azure.messaging.eventhubs.EventHubConsumerClient;
import com.azure.messaging.eventhubs.models.EventPosition;

public class OutageResilienceTest {
    
    public void runTest() {
        // Setup consumer client with EventPosition.latest() to start from the end
        // This client has built-in retry logic.
        EventHubConsumerClient consumer = new EventHubClientBuilder()
            // ... client configuration ...
            .consumerGroup("$Default")
            .eventPosition(EventPosition.latest())
            .buildConsumerClient();

        System.out.println("Starting consumer. Now, trigger a network block to Event Hubs.");
        
        try {
            consumer.receive(
                partitionContext -> {
                    // Logic to process events
                    System.out.println("Event received!");
                },
                errorContext -> {
                    // This is where transient errors are handled.
                    // The client automatically retries connections.
                    System.err.println("Error occurred during event reception: " + errorContext.getThrowable().getMessage());
                });
        } catch (Exception e) {
            // This block would be for unrecoverable errors.
            System.err.println("Consumer failed with an unrecoverable error: " + e.getMessage());
        } finally {
            // This is crucial for cleanup
            consumer.close();
        }
    }
}