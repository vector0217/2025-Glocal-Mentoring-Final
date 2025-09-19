import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import zipfile
import os

# Step 1. 연합뉴스에서 기사 제목 크롤링
url = "https://www.yna.co.kr/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

titles = []
for item in soup.find_all(class_='tit-news'):
    title = item.get_text().strip()
    if title:
        titles.append(title)

text = ' '.join(titles)

# Step 2. 한글 폰트 ZIP 다운로드 및 압축 해제
zip_url = "https://github.com/naver/nanumfont/releases/download/VER2.5/NanumGothicCoding-2.5.zip"
zip_path = "NanumGothicCoding.zip"
font_dir = "fonts"
font_path = os.path.join(font_dir, "NanumGothicCoding-Bold.ttf")  # 사용할 .ttf 폰트

if not os.path.exists(font_path):
    print("📥 폰트 ZIP 다운로드 중...")
    r = requests.get(zip_url)
    with open(zip_path, "wb") as f:
        f.write(r.content)
    print("✅ ZIP 다운로드 완료!")

    print("🗜️ 압축 해제 중...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(font_dir)
    print("✅ 압축 해제 완료!")

# Step 3. WordCloud & matplotlib에 폰트 설정
fontprop = fm.FontProperties(fname=font_path)

# Step 4. 워드클라우드 생성 및 시각화
if text and os.path.exists(font_path):
    wordcloud = WordCloud(
        font_path=font_path,
        background_color='white',
        width=800,
        height=400
    ).generate(text)

    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("연합뉴스 워드클라우드 실습", fontsize=100, fontproperties=fontprop)
    plt.show()
else:
    print("뉴스 텍스트 또는 폰트가 존재하지 않습니다.")
