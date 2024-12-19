# filename: app/utils/rate_limit.py
from collections import defaultdict
from time import time
from app.core.config import settings

rates = defaultdict(list)

def check_rate_limit(user_id: int) -> bool:
    now = time()
    rates[user_id] = [t for t in rates[user_id] if t > now - 60]
    if len(rates[user_id]) >= settings.RATE_LIMIT:
        return False
    rates[user_id].append(now)
    return True
