import json
from datetime import datetime

def generate_json_report(target, data):
    filename = f"report_{target}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    return filename


def generate_html_report(target, data):
    filename = f"report_{target}.html"

    html = f"""
    <html>
    <body>
    <h1>Scan Report for {target}</h1>
    <p>Generated: {datetime.now()}</p>
    <h2>Risk: {data['risk_level']} ({data['risk_score']})</h2>
    <ul>
    """

    for port in data["open_ports"]:
        html += f"<li>Port {port['port']} - {port['banner']} - CVE: {port.get('cve')}</li>"

    html += "</ul></body></html>"

    with open(filename, "w") as f:
        f.write(html)

    return filename
