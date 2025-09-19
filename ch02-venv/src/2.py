'''
    크롤링 실습 : 원하는 웹페이지의 하이퍼링크와 텍스트 검출해보기
'''

import requests
from bs4 import BeautifulSoup

# 웹 페이지 요청
# url = 'http://www.naver.com'
# url = 'https://www.hanati.co.kr/kor/main.jsp'
url = 'https://ijss.icehs.kr/main.do'
response = requests.get(url)

# 요청 성공 여부 확인
if response.status_code == 200:
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser')

    # 모든 <a> 태그 추출
    links = soup.find_all('a')

    # 링크와 텍스트 출력
    for link in links:
        print(f"Text: {link.string}, URL: {link.get('href')}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")