from app.models import Web
import requests
from flask import request

def forward_request(web_id, path, method, headers, body, query):
    web = Web.query.filter_by(id=web_id).first()
    if not web:
        return b"Web ID not found", 404, {}

    url = f"{web.url.rstrip('/')}/{path}"
    if query:
        url += f"?{query}"

    headers = {key: value for key, value in headers.items() if key not in [
        'Cookie', 'Postman-Token', 'Accept-Encoding', 'Connection', 'Host']}
    print(f"🔗 Forwarding to: {url}")
    print(f"📩 Headers: {headers}")

    response = requests.request(method, url, headers=headers, data=body)
    return response.content, response.status_code, response.headers.items()
