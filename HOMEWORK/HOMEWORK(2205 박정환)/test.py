import pandas as pd
import folium
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우용 한글 폰트
plt.rcParams['axes.unicode_minus'] = False     # 마이너스 기호 깨짐 방지
import webbrowser
import os

# 데이터 불러오기
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.csv"
df = pd.read_csv(url)

# 인도네시아 영역으로 바꿈(위도 -15 ~ 10, 경도 95~145)
df_indo = df[
    (df['latitude'] > -15) & (df['latitude'] < 10) &
    (df['longitude'] > 95) & (df['longitude'] < 145)
]

# 지도 생성
indo_map = folium.Map(location=[-2, 120], zoom_start=4)
for _, row in df_indo.iterrows():
    popup = folium.Popup(f"위도: {row['latitude']:.2f}<br>경도: {row['longitude']:.2f}<br>규모: {row['mag']}", max_width=250)
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['mag'] * 1.5,
        color='red' if row['mag'] > 5 else 'orange',
        fill=True,
        fill_opacity=0.6,
        popup=popup
    ).add_to(indo_map)

indo_map.save("earthquakes_indonesia_map.html")

print("인도네시아 지진 지도 저장 완료: earthquakes_indonesia_map.html")


# 히스토그램 (지진 규모 분포 시각화)
sns.set(style="whitegrid")
plt.figure(figsize=(10,6))
sns.histplot(df_indo['mag'], bins=20,kde=True, color='skyblue', edgecolor = 'black')
plt.title("아시아 지역 지진 규모 분포", fontsize = 14)
plt.xlabel("지진 규모 (Magnitude)", fontsize=12)
plt.ylabel("빈도",fontsize=12)
plt.show()
print("히스토그램 저장 완료: earthquake_indonesia_hist.png")

#지도 열기
map_path = os.path.abspath("earthquakes_indonesia_map.html")
webbrowser.open(f"file://{map_path}")

print("인도네시아 지진 지도 저장 및 자동 열기 완료")