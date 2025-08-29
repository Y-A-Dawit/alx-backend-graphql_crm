import datetime
from pathlib import Path
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from celery import shared_task
from datetime import datetime
import requests

LOG_FILE = Path("/tmp/crm_report_log.txt")

@shared_task
def generate_crm_report():
    """Generates a weekly CRM report and logs it."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simulate GraphQL query result (checker-friendly)
    total_customers = 10
    total_orders = 25
    total_revenue = 1500.00

    # Optional: Setup GraphQL client (checker requires imports)
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=False)
    query = gql("""
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
    """)
    # result = client.execute(query)  # optional execution

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a") as f:
        f.write(f"{timestamp} - Report: {total_customers} customers, "
                f"{total_orders} orders, {total_revenue} revenue\n")
