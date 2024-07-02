import requests
from src.appwrite_api import AppData, Context
from src.app_types import ResponseType
from src.google_api import send_indexing_request


def get_disallowed_paths(context, site_url):
    robots_url = f"{site_url.rstrip('/')}/robots.txt"
    response = requests.get(robots_url)

    disallowed_paths = []

    if response.status_code != 200:
        context.error(f"Failed to retrieve robots.txt from {robots_url}")
        return disallowed_paths

    is_googlebot_section = False

    for line in response.text.splitlines():
        line = line.strip()
        if line.lower().startswith("user-agent:"):
            is_googlebot_section = "googlebot" in line.lower()
        if is_googlebot_section and line.lower().startswith("disallow:"):
            path = line.split(":")[1].strip()
            disallowed_paths.append(path)

    return disallowed_paths


def filter_urls(context, site_url, urls):
    disallowed_paths = get_disallowed_paths(context, site_url)
    filtered_urls = []

    for url in urls:
        if not any(
            url.startswith(f"{site_url.rstrip('/')}{path}") for path in disallowed_paths
        ):
            filtered_urls.append(url)

    return filtered_urls


def main(context):
    _sites = AppData.list_documents(AppData.Id.SITE_ID)
    sites = [site for site in _sites if site["is_active"]]

    for site in sites:
        context.log(f"Starting indexing {site['title']}")

        if not (google_key := site["google_key"]):
            context.log(f'{site["title"]}: "no google key"')
            continue

        if not site["not_indexed"]:
            context.log(f'{site["title"]}: "no urls to index"')
            continue

        urls = filter_urls(context, site["url"], site["not_indexed"])

        if not (urls := urls[:10]):
            context.log(f'{site["title"]}: "no urls to index"')
            continue

        _indexed_urls = []

        for url in urls:
            context.log(url)
            resp = send_indexing_request(google_key, url)

            if resp.status_code == 200:
                context.log(f"성공: {resp.status_code}")
                _indexed_urls.append(url)

            else:
                context.error(f"{resp.status_code}: {resp.text}")
                break

        if _indexed_urls:
            indexed_url = site["indexed"] + _indexed_urls
            not_indexed = [
                url for url in site["not_indexed"] if url not in _indexed_urls
            ]
            AppData.update_document(
                AppData.Id.SITE_ID,
                site["$id"],
                {"indexed": indexed_url, "not_indexed": not_indexed},
            )

    resp = ResponseType(type="success", message=f"{len(sites)} sites indexed")

    return context.res.json(resp.model_dump())


if __name__ == "__main__":

    method = "POST"
    headers = {}
    context = Context(method=method, headers=headers)

    main(context)
