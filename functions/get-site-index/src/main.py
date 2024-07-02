# src/main.py
import requests
import xml.etree.ElementTree as ET
from src.appwrite_api import AppData, Context
from src.app_types import ResponseType


def fetch_sitemap_urls(context, sitemap_url) -> list:
    """Sitemap URL에서 XML 데이터를 가져와 URL 목록을 반환합니다."""
    urls = []
    try:
        response = requests.get(sitemap_url)
        root = ET.fromstring(response.content)
        urls = [
            elem.text
            for elem in root.findall(
                ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            )
        ]

    except requests.exceptions.RequestException as e:
        context.log(f"Error fetching sitemap: {e}")

    except ET.ParseError as e:
        context.log(f"Error parsing sitemap: {e}")

    return urls


def main(context):
    _sites = AppData.list_documents(AppData.Id.SITE_ID)
    sites = [site for site in _sites if site["is_active"]]

    for site in sites:
        context.log(f"Updating {site['title']}...")

        if not (urls := fetch_sitemap_urls(context, site["sitemap"])):
            context.log(f"{site['title']} - No new URLs found.")
            continue

        indexed = list(set(site.get("indexed", [])))

        if not (not_indexed := [url for url in urls if url not in indexed]):
            context.log(f"{site['title']} - No new URLs found.")
            continue

        if set(not_indexed) == set(site["not_indexed"]):
            context.log(f"{site['title']} - No new URLs found.")
            continue

        AppData.update_document(
            AppData.Id.SITE_ID,
            site["$id"],
            {"not_indexed": not_indexed},
        )
        context.log(f"{site['title']} - Updating with {len(not_indexed)} new URLs.")

    resp = ResponseType(type="success", message=f"{len(sites)} sites updated.")

    return context.res.json(resp.model_dump())


if __name__ == "__main__":

    method = "POST"
    headers = {}
    context = Context(method=method, headers=headers)

    main(context)
