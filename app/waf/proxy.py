import requests
from flask import request

from app.models import Web


def forward_request(path, method, headers, body, query):
    # web_url = request.args.get("web_url")
    web_url = request.headers.get("X-Web-URL")

    print(f"🔍 web_url nhận được: {web_url}")

    if not web_url:
        return b"Missing web_url", 400, {}

    web = Web.query.filter_by(url=web_url).first()
    if not web:
        return b"Web URL not found", 404, {}

    url = f"{web.url.rstrip('/')}/{path}"
    if query:
        url += f"?{query}"

    headers = {key: value for key, value in headers.items() if key not in ['Cookie', 'Postman-Token', 'Accept-Encoding', 'Connection']}
    print(headers)
    response = requests.request(method, url, headers={'X-Web-Url': web_url}, data=body)
    return response.content, response.status_code, response.headers.items()
