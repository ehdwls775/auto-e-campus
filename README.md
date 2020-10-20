# Auto E-Campus

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fyoolisel%2Fauto-e-campus&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://github.com/yoolisel/auto-e-campus)
  
Contact : yoolisel@gmail.com

## 왜
2020년을 맞이해 대부분의 것들이 비대면으로 전환되었습니다. 회사에서는 재택근무를 시행하고, 학교 역시 줌 서비스 등을 이용한 비대면 온라인 클래스를 운영하고 있습니다. 하지만 대 국립 경상대학교의 E 캠퍼스 시스템은 멍청하게도 오래되고 구닥다리의 rtmp 기반 웹 플레이어를 사용하고 있습니다. 그래서 학습의 효율성 증대를 위해 온라인 클래스를 다운로드해 배속으로 시청하고, 출석은 자동으로 진행하기로 결정했습니다.
  
저는 최근에 몇몇 커뮤니티를 통해서 비디오 다운로드를 하는 방법을 공유했습니다. 그러자 E캠퍼스팀은 rtmp 영상의 주소에 인덱스를 박아넣도록 변경했고, 그 말인 즉슨 그들은 이 rtmp 프로토콜을 숨길 생각도 능력도 자원도 없다는 뜻입니다. 최선의 방법은 학생들이 악용하지 못하도록 귀찮게 하는 것 뿐이겠죠. 하지만 저는 앉아서 방구나 끼고 있을 생각이 없습니다. 그냥 싸갈겨 만들었던 스크립트를 확장해 다운로드기능도 넣기로 했습니다.

## Requirements
- Selenium
- [Chrome Web Driver](https://chromedriver.chromium.org/downloads) ( compatible version to chrome on your system)

## Features  
1. 강의 자동으로 수강
2. rtmp 주소 파싱

## How To Use
### Essential
1. requirements  를 설치해야합니다.  
```
$ pip install -r requirements.txt
```
2. id.py 를 텍스트에디터(메모장 등)로 열어 아이디/비밀번호를 포맷에 맞추어 쓰세요.  
3. chromedriver 를 `/auto-e-campus/chromedriver.exe` 경로에 넣습니다.  

### 1. 강의 자동으로 수강
Run by python
- 크롬 브라우저 띄우기  

```
python study.py
```
- 크롬 브라우저 띄우지 않기  

```
python study.py headless
```
  
### 2. rtmp 주소 파싱
Run by python
```
python study.py address
```

- just execute address.bat file

그러면, `rtmp_{{ lecture.name }}.json'` 파일이  `/auto-e-campus/rtmp_xxx.json`  에 생성될 것입니다.
텍스트 에디터로 열어보세요. 그리고 다운로드 하면 됩니다. [download with FFMPEG](https://github.com/yoolisel/download-flow-player-rtmp)  


#### 파싱과 크롤링
제가 빡대가리라서 크롤링 대신 파싱이라는 용어를 사용한 것이 아닙니다.  
3강짜리 웹 크롤링 만들기 파이썬 튜토리얼을 따라해보고 크롤러냐고 물을거면 좆이나 까 잡수십시오.  
