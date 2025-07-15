#!/bin/bash
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="/var/log/customer_cleanup_log.txt"
DELETE_COUNT = python manage.py shell >> $LOG_FILE 2>&1 <<EOF(
from crm.models import Customer
from datetime import timedelta
from django.utils import timezone

# This script deletes inactive customers from the CRM database.
out_off_date = timezone.now() - timedelta(days=365)  # Define inactive as no activity in the last 365 days
inactive_customers = Customer.objects.filter(is_active=False)
count = inactive_customers.count()

if count > 0:
    print(f"Deleting {count} inactive customers.")
    delete_count = inactive_customers.delete()
    print(f"Deleted {delete_count[0]} inactive customers.")
else:
    print("No inactive customers found.")
echo "Cleaning inactive customers at $TIMESTAMP" >> $LOG_FILE