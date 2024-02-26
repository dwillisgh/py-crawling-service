import argparse
import asyncio
import os
from lxml.html.soupparser import fromstring, etree


async def parse_html_results_for_urls(html_file, url_results_file):
    html = None

    path = os.path.expanduser(html_file)

    #  open html search results file
    with open(path) as f:
        html = f.read()

    print(f"{html}")
    tree = fromstring(html)
    hrefs = tree.xpath("//div//a/@href")
    for href in hrefs:
        print(f"{href}")

    filtered_hrefs = filter_urls(hrefs)
    filtered_hrefs = list(set(filtered_hrefs))
    filtered_hrefs.sort()

    path = os.path.expanduser(url_results_file)

    with open(path, 'w') as temp_file:
        temp_file.write('\n'.join(filtered_hrefs))


def filter_urls(hrefs):
    hrefs_filtered = []
    for href in hrefs:
        if "https://" not in href:
            continue
        if "google" in href:
            continue
        hrefs_filtered.append(href)
    return hrefs_filtered


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("htmlFile", help="search provider results html file to process")
    parser.add_argument("outputFile", help="file of urls from the search provider results html")
    args = parser.parse_args()

    html_file = args.htmlFile
    url_results_file = args.outputFile

    await parse_html_results_for_urls(html_file, url_results_file)


if __name__ == "__main__":
    asyncio.run(main())
