'''
    파이썬 모듈 설치 실습
    1. 파이썬 가상환경 생성
    2. pip install requests
'''

import requests

response = requests.get('https://api.github.com')
print(response.status_code) #200 출력 : HTTP응답