import requests
import ctypes
import os
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter


SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 1
SPIF_SENDCHANGE = 2
flags = SPIF_UPDATEINIFILE | SPIF_SENDCHANGE

API_KEY="JnAH4b8Dh2z3bkYpRofpHBgSHWmBK3jbgfs8W1ZO"
params={
    "api_key":API_KEY,
    "thumbs": True
}
url="https://api.nasa.gov/planetary/apod"
archivedir="archive"
os.makedirs(archivedir,exist_ok=True)

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

if __name__ == "__main__":
    response=requests.get(url, params=params,timeout=10)
    response.raise_for_status()
    data=response.json()

    imageData=requests.get(getURL(isHiDef=True),timeout=10).content

    with open("apod.jpg","wb") as f:
        f.write(imageData)

    basePath=os.path.dirname(os.path.abspath(__file__))
    imagePath = os.path.join(basePath,"apod.jpg")
    saveImage()

    img=Image.open("apod.jpg").convert("RGB")

    # time.sleep(0.5)
    setWallp()