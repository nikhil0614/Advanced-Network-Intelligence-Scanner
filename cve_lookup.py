import requests

def lookup_cve(service_banner):
    if not service_banner or service_banner == "No Banner":
        return None

    keywords = service_banner.split(" ")

    for word in keywords:
        try:
            url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={word}"
            response = requests.get(url, timeout=3)
            data = response.json()

            if "vulnerabilities" in data and data["vulnerabilities"]:
                return data["vulnerabilities"][0]["cve"]["id"]

        except:
            continue

    return None
