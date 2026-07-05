import re
import requests
import xml.etree.ElementTree as ET

CHANNEL_ID = "YOUR_CHANNEL_ID"

RSS = f"https://www.youtube.com/feeds/videos.xml?channel_id={"UCRs-ZxEdF1cmgRvnGrbmvNQ"}"

response = requests.get(RSS)
root = ET.fromstring(response.content)

ns = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015"
}

videos = []

for entry in root.findall("atom:entry", ns)[:4]:

    title = entry.find("atom:title", ns).text

    video_id = entry.find("yt:videoId", ns).text

    url = f"https://youtu.be/{video_id}"

    thumbnail = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

    videos.append(
        f"""
<td align="center">
<a href="{url}">
<img src="{thumbnail}" width="340">
</a><br>
<b>{title}</b>
</td>
"""
    )

table = "<table>"

for i in range(0, len(videos), 2):

    table += "<tr>"

    table += videos[i]

    if i + 1 < len(videos):
        table += videos[i + 1]

    table += "</tr>"

table += "</table>"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

pattern = r"<!-- YOUTUBE-VIDEOS-START -->(.*?)<!-- YOUTUBE-VIDEOS-END -->"

replacement = (
    "<!-- YOUTUBE-VIDEOS-START -->\n"
    + table +
    "\n<!-- YOUTUBE-VIDEOS-END -->"
)

updated = re.sub(pattern, replacement, readme, flags=re.S)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)

print("README Updated!")
