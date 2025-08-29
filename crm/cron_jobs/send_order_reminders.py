#!/usr/bin/env python3
"""
Script to send order reminders using GraphQL
"""

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

LOG_FILE = "/tmp/order_reminders_log.txt"

def main():
    # GraphQL client setup
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Calculate 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # GraphQL query for orders within the last 7 days
    query = gql("""
        query ($date: DateTime!) {
            orders(orderDate_Gte: $date) {
                id
                customerEmail
            }
        }
    """)

    params = {"date": seven_days_ago}

    try:
        result = client.execute(query, variable_values=params)
        orders = result.get("orders", [])
    except Exception as e:
        print(f"Error querying GraphQL endpoint: {e}")
        return

    # Log reminders
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        for order in orders:
            line = f"{timestamp} - Order ID: {order['id']}, Customer: {order['customerEmail']}\n"
            f.write(line)

    print("Order reminders processed!")

if __name__ == "__main__":
    main()
