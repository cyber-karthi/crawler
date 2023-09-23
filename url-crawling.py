import json

import requests


def crawl_wayback_archive(domain, max_depth=3, output_file="output.txt"):
    visited = set()
    wayback_url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json"

    def _crawl(snapshot_url, depth):
        if depth > max_depth or snapshot_url in visited:
            return

        visited.add(snapshot_url)

        try:
            response = requests.get(snapshot_url)
            
            # Check if the response is successful
            if response.status_code == 200:
                # Check if the response content is not empty
                if response.text.strip():
                    archived_data = response.json()
                    with open(output_file, "a") as file:
                        for snapshot in archived_data[1:]:
                            snapshot_url = snapshot[2]
                            file.write(f"{snapshot_url}\n")
                            print(f"Crawling: {snapshot_url}")
                else:
                    print(f"Empty response content from {snapshot_url}")
            else:
                print(f"Non-200 status code for {snapshot_url}: {response.status_code}")

        except Exception as e:
            print(f"Error crawling {snapshot_url}: {str(e)}")

    try:
        response = requests.get(wayback_url)
        if response.status_code == 200:
            snapshots = response.json()

            for snapshot in snapshots[1:]:
                snapshot_url = f"http://web.archive.org/web/{snapshot[1]}if_/{snapshot[2]}"
                _crawl(snapshot_url, 0)

        else:
            print(f"Non-200 status code for Wayback API: {response.status_code}")

    except Exception as e:
        print(f"Error fetching snapshots for {domain}: {str(e)}")

if __name__ == "__main__":
    target_domain = input("Enter the domain to start crawling from Wayback Archive (e.g., example.com): ")
    crawl_wayback_archive(target_domain)
