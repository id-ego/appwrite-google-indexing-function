import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


def send_indexing_request(google_key, url_to_index):
    # 서비스 계정 정보로 Credentials 객체 생성
    info = json.loads(google_key)
    credentials = service_account.Credentials.from_service_account_info(
        info, scopes=SCOPES
    )
    credentials.refresh(Request())

    # Google Indexing API 호출
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json",
    }
    payload = {"url": url_to_index, "type": "URL_UPDATED"}
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    return response
