from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
today = datetime.now()
import logging
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

seven_days_ago = today - timedelta(days=7)

start_date = seven_days_ago.strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

transport = RequestsHTTPTransport(
    url='http://localhost:8000/graphql', verify =False, retries=3',
    timeout=10,
    use_json=True,
    headers={
        'Authorization'
        : 'Bearer YOUR_ACCESS_TOKEN'
    }
)
client = Client(transport=transport, fetch_schema_from_transport=True)
logging.basicConfig(
    filename='/var/log/customer_cleanup_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.info = 'This is a test log message'
logging.error = 'This is a test error message'
logging.warning = 'This is a test warning message'
 for order in orders:
    order_id = order['id']
    customer_id = order['customer']['id']
    customer_email = order['customer']['email']
    order_date = order['created_at']
    order_amount = order['amount']
    logger.info(f"Order ID: {order_id}, Customer email: {customer_id}, Order Date: {order_date}, Order Amount: {order_amount}")