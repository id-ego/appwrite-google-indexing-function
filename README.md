# Appwrite Google Indexing Function

This project provides serverless functions to interact with Google Search Console using Appwrite Cloud. The functions automate the process of fetching site indexing information and updating the Google search index with new or changed content. The project consists of two main functions: `get-site-index` and `google-index-update`.

## Function Descriptions

### get-site-index

This function fetches and analyzes site indexing information. It extracts URLs from the sitemap, identifies URLs that are not indexed, and adds them to the update list.

#### Components

- `app_types.py`: Defines data types used in the application.
- `appwrite_api.py`: Contains code for interacting with the Appwrite API.
- `main.py`: The main script that fetches the sitemap and updates the list of unindexed URLs.

### google-index-update

This function updates the Google Search Console index to reflect new or updated content. It checks the robots.txt file to filter out disallowed paths and sends indexing requests to Google.

#### Components

- `app_types.py`: Defines data types used in the application.
- `appwrite_api.py`: Contains code for interacting with the Appwrite API.
- `google_api.py`: Contains code for interacting with the Google API.
- `main.py`: The main script that filters the list of URLs and sends indexing requests to Google.
