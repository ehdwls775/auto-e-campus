# Auto E-Campus

## Introduction
In the 2020s, most of the things are processed without face-to-face. Companies work from home, and schools also have remote classes through zoom service. But the e-campus learning system at the Great Gyeonsang National University is stupidly using a very old and outdated shitty rtmp-based web player. So to inrease the efficiency of learning, I decided to download lectures videos and take classes automatically.  
  
I recently shared a video download method throught several communities. However, the team of e-campus have made it to bring rtmp address every time by implementing index of video to addresses. It means the they have no ability to hide their rtmp protocol. The best option they can do is to annoy us. but I don't want to sit down and suffer. Thus lets parse rtmp link by extending this auto-e-campus.

## Requirements
- Selenium
- [Chrome Web Driver](https://chromedriver.chromium.org/downloads) ( compatible version to chrome on your system)

## Features  
1. watch lectures automatically
2. get video rtmp address from e-campus

## How To Use
### Essential
1. install requirements  
```
$ pip install -r requirements.txt
```
2. Fill identification in id.py with any text editor  
3. place chromedriver at `/auto-e-campus/chromedriver.exe`

### 1. watch lectures automatically
Run by python
- with browser

```
python study.py
```
- without browser

```
python study.py headless
```

- just execute run.bat file
  
### 2. get video rtmp addresses
Run by python
```
python study.py address
```

- just execute address.bat file

then, `rtmp_{{ lecture.name }}.json'` will be created at `/auto-e-campus/rtmp_xxx.json`  
open json with any text editor and [download with FFMPEG](https://github.com/yoolisel/download-flow-player-rtmp)  
