import time
import requests


#Retry na api para caso de crash/timeout etc...
def get_with_retries(session, url, params=None, max_retries=3):
    backoff = 1
    for attempt in range(1, max_retries+1):
        resp = session.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            return resp
        if resp.status_code in (429, 500, 502, 503, 504):
            time.sleep(backoff)
            backoff *= 2
            continue
        resp.raise_for_status()
    raise Exception("Falha persistente ao acessar URL")
