import requests
import ctypes
import os
import time

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 1
SPIF_SENDCHANGE = 2
flags = SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATE_FILE = os.path.join(BASE_DIR, "lastDate.txt")

LOG_FILE = os.path.join(BASE_DIR, "run.log")

API_KEY="JnAH4b8Dh2z3bkYpRofpHBgSHWmBK3jbgfs8W1ZO"
params={
    "api_key":API_KEY,
    "thumbs": True
}
url="https://api.nasa.gov/planetary/apod"
archivedir = os.path.join(BASE_DIR, "archive")
os.makedirs(archivedir, exist_ok=True)

def getURL(isHiDef):
    if data["media_type"]=="image":
        if isHiDef:
            imageURL=data.get("hdurl") if data.get("hdurl") else data.get("url")
        else:
            imageURL = data.get("url")
    else:
        imageURL = data.get("thumbnail_url")
    return imageURL

def setWallp():
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        imagePath,
        flags
    )

def saveImage():
    saveURL=getURL(isHiDef=False)
    dateTemp=data["date"]
    yyyy,mm,dd=dateTemp.split("-")
    date=f"{dd}-{mm}-{yyyy}"
    fileName=f"{date}.jpg"
    imageDataTemp=requests.get(saveURL,timeout=10).content
    filePath=os.path.join(archivedir,fileName)
    with open(f"{filePath}","wb") as f:
        f.write(imageDataTemp)

def dateCheck():
    today=data["date"]
    if os.path.exists(DATE_FILE):
        with open(DATE_FILE) as f:
            last=f.read().strip()
    else:
        last=""
    if today==last:
        return

def setDate():
    with open(DATE_FILE, "w") as f:
        f.write(data["date"])

if __name__ == "__main__":
    with open(LOG_FILE, "a") as f:
        f.write(f"Ran at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    response=requests.get(url, params=params,timeout=10)
    response.raise_for_status()
    data=response.json()
    dateCheck()

    imageData=requests.get(getURL(isHiDef=True),timeout=10).content

    imagePath = os.path.join(BASE_DIR, "apod.jpg")

    with open(imagePath, "wb") as f:
        f.write(imageData)

    saveImage()

    # time.sleep(0.5)
    setWallp()

    setDate()