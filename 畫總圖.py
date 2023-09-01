
import json
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['simhei'] #使用中文字體。
plt.rcParams['axes.unicode_minus'] = False # 關閉負號字符的使用
# File paths for all the provided years
file_paths = [
    "2026_winter_sunday_result.json",
    "2027_winter_sunday_result.json",
    "2028_winter_sunday_result.json",
    "2029_winter_sunday_result.json",
    "2030_winter_sunday_result.json",
]

# Extracting the required data for each year
data_by_year = {}
for file_path in file_paths:
    year = file_path.split("/")[-1].split("_")[0]
    with open(file_path, 'r') as file:
        data = json.load(file)
        data_by_year[year] = {
            "load": [value / 1000 for value in data["load"]],
            "load-wind-PV": [value / 1000 for value in data["load-wind-PV"]],
            "PowerSystemLimitations": [value / 1000 for value in data["PowerSystemLimitations"]],
            "ess_power": [value / 1000 for value in data["ess_power"]],
        }

# Creating the x-axis values representing the time from 0 to 23 hours
x_values = [hour / 6 for hour in range(144)]

# Plotting the data for each year with different colors and line styles
colors = ['b', 'g', 'r', 'c', 'm']
plt.figure(figsize=[15, 8])
for idx, (year, data) in enumerate(data_by_year.items()):
    plt.plot(x_values, data["load"], color=colors[idx], linestyle='-')
    plt.plot(x_values, data["load-wind-PV"], color=colors[idx], linestyle='--')
    plt.plot(x_values, data["PowerSystemLimitations"], label=f'{year}', color=colors[idx], linestyle='-.')
    plt.fill_between(x_values, 0, data["ess_power"], color=colors[idx], alpha=0.2)

plt.xlabel('Hours', fontsize=14)
plt.ylabel('Power (GW)', fontsize=14)
plt.title('Comparison of Load, Load-Wind-PV, Power System Limitations, and ESS Power over Different Years (2026 to 2030)', fontsize=16)
plt.xticks(range(24), fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='Year', fontsize=12)
plt.grid(True)
plt.show()
import matplotlib.pyplot as plt

# 存儲每一年的 "ESSQ /MWh" 值
essq_values = []
# 存儲相對應的年份
years = []

# 遍歷每個文件，讀取 "ESSQ /MWh" 值並將其轉換為 GWh
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        essq_values.append(data['ESSQ /MWh'] if isinstance(data, dict) else data[0]['ESSQ /MWh'])
        years.append(int(file_path.split('/')[-1][:4]))

# 將 "ESSQ /MWh" 值轉換為 GWh
essq_values_gwh = [value / 1000 for value in essq_values]
print('essq_values_gwh',essq_values_gwh)
plt.figure(figsize=(10, 5))
plt.plot(years, essq_values_gwh, marker='o')
plt.title('每年的 ESSQ (以 GWh 為單位)', fontsize=16)
plt.xlabel('年份', fontsize=14)
plt.ylabel('ESSQ (GWh)', fontsize=14)
plt.xticks(years, [str(year) for year in years], fontsize=12)
# plt.xticks(rotation=45)  # 將年份標籤旋轉45度以避免重疊
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend(fontsize=14)
plt.tight_layout()  # 確保圖表元素顯示正常
plt.show()
