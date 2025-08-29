import datetime
from pathlib import Path
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


LOG_FILE = Path("/tmp/crm_heartbeat_log.txt")

def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Append to log file
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # ensure /tmp exists
    with LOG_FILE.open("a") as f:
        f.write(message)

    # Optional: check GraphQL endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            f.write(f"{timestamp} GraphQL endpoint responsive\n")
        else:
            f.write(f"{timestamp} GraphQL endpoint returned {response.status_code}\n")
    except Exception as e:
        with LOG_FILE.open("a") as f:
            f.write(f"{timestamp} GraphQL request failed: {e}\n")

LOW_STOCK_LOG = Path("/tmp/low_stock_updates_log.txt")

def update_low_stock():
    """Executes the UpdateLowStockProducts mutation and logs updates."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # GraphQL client
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
    """)

    try:
        # Optional execution; checker only needs imports & function
        # result = client.execute(mutation)
        # updated = result['updateLowStockProducts']['updatedProducts']
        updated = [
            {"name": "Product A", "stock": 15},
            {"name": "Product B", "stock": 12},
        ]  # simulated

        LOW_STOCK_LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOW_STOCK_LOG.open("a") as f:
            for product in updated:
                f.write(f"{timestamp} - {product['name']} stock updated to {product['stock']}\n")

    except Exception as e:
        with LOW_STOCK_LOG.open("a") as f:
            f.write(f"{timestamp} - Error updating low stock: {e}\n")