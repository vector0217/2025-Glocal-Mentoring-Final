import pandas as pd
import folium
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 불러오기
df = pd.read_csv("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.csv")

# 일본/한국 근처만 필터링 (위도 20~50, 경도 120~150)
df_asia = df[(df['latitude'] > 20) & (df['latitude'] < 50) &
             (df['longitude'] > 120) & (df['longitude'] < 150)]

# 지도 생성
map = folium.Map(location=[35, 135], zoom_start=4)
for _, row in df_asia.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['mag'] * 1.5,
        color='red' if row['mag'] > 5 else 'orange',
        fill=True,
        fill_opacity=0.6
    ).add_to(map)
map.save("earthquakes_map.html")

# 히스토그램 (지진 규모 분포)
sns.histplot(df_asia['mag'], bins=20)
plt.title("지진 규모 분포")
plt.xlabel("규모 (Magnitude)")
plt.ylabel("빈도")
plt.show()
