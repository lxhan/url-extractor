from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import requests

API_VIDEO_URL = "https://edge.api.brightcove.com/playback"

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

on = True
while on:
    input_url = input("Input video url:\n")

    if input_url == "done":
        on  = False
        break

    driver.get(input_url)

    video_url = ""
    pk = ""
    for request in driver.requests:
        if request.response and API_VIDEO_URL in request.url:
            video_url = request.url
            pk = request.headers.get("accept")

    if video_url:
        headers = {
            "accept": pk
        }
        r = requests.get(url=video_url, headers=headers)
        data = r.json()
        sources = data["sources"]
        src_url = sources[-1]["src"]

        print("\n---------------------------------------------------------------------------------")
        print(src_url)
        print("---------------------------------------------------------------------------------\n")
