#!/bin/bash
# Script to delete inactive customers (no orders in the past year)

# Go to project root (adjust if needed)
cd "$(dirname "$0")/../.."

# Run Django shell command
deleted_count=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

cutoff_date = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff_date)
count = qs.count()
qs.delete()
print(count)
")

# Log result with timestamp
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $deleted_count\" >> /tmp/customer_cleanup_log.txt
