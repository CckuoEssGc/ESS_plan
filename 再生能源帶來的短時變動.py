#region 這一段代碼可以把每一年的太陽能風力發電裝置容量儲存到字典裡面
from data_set import get_capacity

years = range(2025, 2031)  # 包括2025年到2030年
capacity_dict = {}  # 用于存储每一年的容量的字典

for year in years:
    try:
        pv_capacity, wind_capacity = get_capacity(year)
        capacity_dict[year] = {'PV Capacity': pv_capacity, 'Wind Capacity': wind_capacity}
    except ValueError as e:
        print(str(e))

# 打印每一年的容量信息
for year, capacity in capacity_dict.items():
    print(f"Year: {year}, Capacity: {capacity}")
#endregion 





#region 這一段代碼可以讀取資料及然後畫出1月2月因為PV發電量變動所引起的頻率調整需求量
import data_set
import matplotlib.pyplot as plt

data_names = ['change_per_GW_down_February', 'change_per_GW_down_January', 'change_per_GW_up_February', 'change_per_GW_up_January']

data_dict = {}  # 用于存储数据的字典

x = range(0, 24)  # X-axis coordinates from 0 to 24 hours


for name in data_names:
    if hasattr(data_set, name):
        data = getattr(data_set, name)
        data_dict[name] = data  # 将数据存储到字典中
        plt.plot(x, data, label=name)
# plt.figure()
# # X軸的刻度每個小時
# plt.xticks(range(0, 25, 1))
# plt.xlabel('Hours')
# plt.ylabel('PV Short-term Variation Percentage')
# plt.title('PV-induced Frequency Regulation Demand')
# plt.legend()
# plt.show()

# 打印数据字典
for name, data in data_dict.items():
    print(f"{name}: {data}")

#endregion 










#region 根據每一年的太陽能裝置容量，來計算每個月每個小時短時間變動量，儲存在字典PV_variation_each_hour ，單位是GW

PV_variation_each_hour = {}  # 用于存储每一年每个月每个小时的变动量的字典

for year, capacity in capacity_dict.items():
    pv_capacity = capacity['PV Capacity']
    # print('pv_capacity',pv_capacity,'year',year)
    for month in ['January', 'February']:
        if f'change_per_GW_down_{month}' in data_dict:
            data = data_dict[f'change_per_GW_down_{month}']
            for hour in range(24):
                variation = pv_capacity * data[hour] / 100
                # print('data[hour]',data[hour],'pv_capacity',pv_capacity,'variation',variation,'year',year,'month',month,'hour',hour)
                PV_variation_each_hour[('down',year, month, hour)] = variation
                

        if f'change_per_GW_up_{month}' in data_dict:
            data = data_dict[f'change_per_GW_up_{month}']
            for hour in range(24):
                variation = pv_capacity * data[hour] /100
                PV_variation_each_hour[('up',year, month, hour)] = variation

# 打印每一年每个月每个小时的变动量 單位是GW
# for (up_or_down,year, month, hour), variation in PV_variation_each_hour.items():
#     print(f"Year: {year}, Month: {month}, Hour: {hour},  {up_or_down}, Variation: {variation} GW")
#打印PV_variation_each_hour
print('PV_variation_each_hour',PV_variation_each_hour)
#endregion 












#region 這一段代碼可以畫出2025年到2030年指定月份的的太陽能短時變動量
import matplotlib.pyplot as plt



month_assigned = 'January'
# Create a new figure
plt.figure()

# Iterate over the years
for year in years:
    # Get the relevant data for downward variation in February
    down_data_year_feb = {hour: variation for (up_or_down, y, month, hour), variation in PV_variation_each_hour.items() if up_or_down=='down' and y==year and month==month_assigned}

    # Get the relevant data for upward variation in February
    up_data_year_feb = {hour: variation for (up_or_down, y, month, hour), variation in PV_variation_each_hour.items() if up_or_down=='up' and y==year and month==month_assigned}

    # Sort the data by hour for both downward and upward variation
    sorted_down_data = sorted(down_data_year_feb.items())
    sorted_up_data = sorted(up_data_year_feb.items())

    # Split into two lists for plotting downward variation
    down_hours, down_variations = zip(*sorted_down_data)

    # Split into two lists for plotting upward variation
    up_hours, up_variations = zip(*sorted_up_data)

    # Create the plot for downward variation
    plt.plot(down_hours, down_variations, label=f'Downward PV Variation in {year}, '+month_assigned)

    # Create the plot for upward variation
    plt.plot(up_hours, up_variations, label=f'Upward PV Variation in {year}, '+month_assigned)

# Set the title and labels
plt.title('PV Variation in '+month_assigned+' from 2025 to 2030')
plt.xlabel('Hour of the day')
plt.ylabel('Variation (GW)')
# X軸的刻度從0到23
plt.xticks(range(0, 24, 1))
# Display the legend
plt.legend()
# plt.show()
#endregion 








#region 得到1月2月因為風力變動產生的額外調整頻率需求，並且製作出每一年每一個月份額外的調整頻率需求

import data_set 
Additional_frequency_capacity_adjustment_due_to_wind_up=data_set.wind_variation_percentage_up
Additional_frequency_capacity_adjustment_due_to_wind_down =data_set.wind_variation_percentage_down
print('Additional_frequency_capacity_adjustment_due_to_wind_up',Additional_frequency_capacity_adjustment_due_to_wind_up)
print('Additional_frequency_capacity_adjustment_due_to_wind_down',Additional_frequency_capacity_adjustment_due_to_wind_down)
wind_variation_each_month ={}



wind_variation_dict = {}  # 用於存儲風力發電變動量的字典

for year, capacity in capacity_dict.items():
    pv_capacity = capacity['PV Capacity']
    wind_capacity = capacity['Wind Capacity']
    wind_variation_dict[year] = {}  # 用於存儲每年的變動量的子字典

    for month in range(1, 13):
        variation_up = wind_capacity * Additional_frequency_capacity_adjustment_due_to_wind_up[month - 1]/100
        variation_down = wind_capacity * Additional_frequency_capacity_adjustment_due_to_wind_down[month - 1]/100
        wind_variation_dict[year][month] = {'Upward Variation': variation_up, 'Downward Variation': variation_down}

# 打印每年每個月的風力發電變動量
for year, month_variations in wind_variation_dict.items():
    for month, variations in month_variations.items():
        print(f"Year: {year}, Month: {month}, Variations: {variations}")


# Create a new figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# Plot upward variations
for year, month_variations in wind_variation_dict.items():
    months = list(month_variations.keys())
    upward_variations = [variations['Upward Variation'] for variations in month_variations.values()]
    ax1.plot(months, upward_variations, label=f'Upward Variation in {year}')

# Plot downward variations
for year, month_variations in wind_variation_dict.items():
    months = list(month_variations.keys())
    downward_variations = [variations['Downward Variation'] for variations in month_variations.values()]
    ax2.plot(months, downward_variations, label=f'Downward Variation in {year}')

# Set titles and labels for each subplot
# X軸的刻度1到12
ax1.set_xticks(range(1, 13, 1))
ax1.set_title('Wind Power Variation - Upward')
ax1.set_ylabel(f'Variation (GW)')
ax2.set_title('Wind Power Variation - Downward')
ax2.set_xlabel('Month')
ax2.set_ylabel('Variation (GW)')

# Display the legend for each subplot
ax1.legend()
ax2.legend()

# Adjust the layout and spacing
plt.tight_layout()

# Show the plot

#endregion 




#region 把太陽能還有風力變動引起的調頻需求加起來
'''取出2025到2030年每年1月還有2月的風力發電短時變動量'''

# Create a new dictionary to store the variation data
variation_data = {}

# Iterate over the years
for year, month_variations in wind_variation_dict.items():
    # Check if the year is within the desired range
    if year >= 2025 and year <= 2030:
        # Initialize the year entry in the variation_data dictionary
        variation_data[year] = {}

        # Iterate over the months
        for month, variations in month_variations.items():
            # Check if the month is January or February
            if month == 1 or month == 2:
                # Add the variations to the variation_data dictionary
                variation_data[year][month] = variations

# Print the variation data
for year, month_variations in variation_data.items():
    for month, variations in month_variations.items():
        print(f"Year: {year}, Month: {month}, Variations(GW): {variations}")

print('variation_data',variation_data)
''' 把每一年太陽能的變動量再加上風力的變動量'''
print('PV_variation_each_hour',PV_variation_each_hour)
total_variation_each_hour = {}

month_key = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',
9:'September',10:'October',11:'November',12:'December'}
for year, months in variation_data.items():
    for month, variations in months.items():
        for i in years:
            if i == year:
                for hour in range(24):
                    key = ('up', year, month_key[month], hour)
                    total_variation_each_hour[key] = PV_variation_each_hour.get(key, 0) + variations['Upward Variation']
                    key = ('down', year, month_key[month], hour)
                    total_variation_each_hour[key] = PV_variation_each_hour.get(key, 0) + variations['Downward Variation']




#畫出圖片檢驗
import matplotlib.pyplot as plt

month_assigned = 'January'

# Create a new figure
plt.figure()

# Iterate over the years
for year in years:
    # Get the relevant data for downward variation in the assigned month
    down_data_year = {hour: variation for (up_or_down, y, month, hour), variation in total_variation_each_hour.items() if up_or_down == 'down' and y == year and month == month_assigned}

    # Get the relevant data for upward variation in the assigned month
    up_data_year = {hour: variation for (up_or_down, y, month, hour), variation in total_variation_each_hour.items() if up_or_down == 'up' and y == year and month == month_assigned}

    # Sort the data by hour for both downward and upward variation
    sorted_down_data = sorted(down_data_year.items())
    sorted_up_data = sorted(up_data_year.items())

    # Split into two lists for plotting downward variation
    down_hours, down_variations = zip(*sorted_down_data)

    # Split into two lists for plotting upward variation
    up_hours, up_variations = zip(*sorted_up_data)

    # Create the plot for downward variation
    plt.plot(down_hours, down_variations, label=f'Downward PV Variation in {year}, '+month_assigned)

    # Create the plot for upward variation
    plt.plot(up_hours, up_variations, label=f'Upward PV Variation in {year}, '+month_assigned)

# Set the title and labels
plt.title('total Variation in ' + month_assigned + ' from 2025 to 2030')
plt.xlabel('Hour of the day')
plt.ylabel('Variation (GW)')
# X軸的刻度從0到23
plt.xticks(range(0, 24, 1))
#放大軸刻度的字體還有軸座標標題的字體
plt.tick_params(axis='both', labelsize=16)
#放大圖例的字體
plt.legend(fontsize=16)

plt.legend()
# Show the plot
# plt.show()

#endregion 








#region讀取json檔案 得到每一年的燃氣發電量 每個小時的
import matplotlib.pyplot as plt
# Sure! Here's the code to read the contents of multiple files:
import json
import os

file_directory='.'
file_names = [
    "2025_winter_sunday_result.json",
    "2026_winter_sunday_result.json",
    "2027_winter_sunday_result.json",
    "2028_winter_sunday_result.json",
    "2029_winter_sunday_result.json",
    "2030_winter_sunday_result.json"
]
# Define the dict to store all load-wind-PV data
load_wind_PV_data = {}
PowerSystemLimitations={}

for file_name in file_names:
    file_path = os.path.join(file_directory, file_name)
    with open(file_path, "r") as file:
        json_data = json.load(file)
        if 'load-wind-PV' in json_data:
            load_wind_PV_data[os.path.splitext(file_name)[0]] = json_data['load-wind-PV']
        if 'PowerSystemLimitations /MW' in json_data:
            PowerSystemLimitations[os.path.splitext(file_name)[0]] = json_data['PowerSystemLimitations /MW']

gas_generation = {}

for year, data in load_wind_PV_data.items():
    power_limit = PowerSystemLimitations[year]
    new_data = []
    for value in data:
        if value < power_limit:
            new_data.append(power_limit)
        else:
            new_data.append(value)
    gas_generation[year] = new_data

print('gas_generation' ,gas_generation)
print('',)

# Plot all load-wind-PV data



plt.figure(figsize=(12, 8))
for key, value in gas_generation.items():
    plt.plot(value, label=key)

plt.legend(loc='best')
plt.title('Load-Wind-PV data over years')
plt.xlabel('Hours')
plt.ylabel('Load-Wind-PV')
plt.grid(True)


'''得到每一年每個小時的燃氣發電量'''

def calculate_hourly_average(data):
    hourly_averages = []
    for i in range(0, len(data), 6):
        hour_data = data[i:i+6]
        hourly_average = int (sum(hour_data) / len(hour_data))
        hourly_averages.append(hourly_average)
    return hourly_averages

result_dict = {}

for year, data in gas_generation.items():
    # 计算每小时平均发电量
    hourly_averages = calculate_hourly_average(data)
    
    # 存储结果到新的字典
    result_dict[f"{year}_hourly_gas_power"] = hourly_averages

# 输出结果
print(result_dict)
import matplotlib.pyplot as plt

# 提取年份和每小时燃气发电量数据
hourly_gas_power = {}

for key, value in result_dict.items():
    if "hourly_gas_power" in key:
        year = key.split("_")[0]
        hourly_gas_power[year] = value

# 绘制折线图
plt.figure(figsize=(10, 6))
for year, data in hourly_gas_power.items():
    plt.plot(data, label=year)
plt.xlabel('Hour')
plt.ylabel('Gas Power Generation')
plt.title('Hourly Gas Power Generation')
plt.xticks(range(0, 24, 1))
plt.legend()
plt.grid(True)
# plt.show()

#endregion 


#region 

print('hourly_gas_power',hourly_gas_power) #單位是MW
print('total_variation_each_hour',total_variation_each_hour)

fluctuations_faced_by_gas_generators_per_GW = {}

for key, value in total_variation_each_hour.items():
    direction, year, month, hour = key
    print('direction',direction,'year',year,'month',month,'hour',hour)
    print('hourly_gas_power[str(year)][hour]',hourly_gas_power[str(year)][hour]/1000)
    updated_value = value / (hourly_gas_power[str(year)][hour]/1000)
    updated_key = (direction, year, month, hour)
    fluctuations_faced_by_gas_generators_per_GW[updated_key] = updated_value



#畫出圖片檢驗
import matplotlib.pyplot as plt

month_assigned = 'January'

# Create a new figure
plt.figure()
# Reset the line color cycle
plt.gca().set_prop_cycle(None)
# Iterate over the years
for year in years:
    # Get the relevant data for downward variation in the assigned month
    down_data_year = {hour: variation for (up_or_down, y, month, hour), variation in fluctuations_faced_by_gas_generators_per_GW.items() if up_or_down == 'down' and y == year and month == month_assigned}

    # Get the relevant data for upward variation in the assigned month
    up_data_year = {hour: variation for (up_or_down, y, month, hour), variation in fluctuations_faced_by_gas_generators_per_GW.items() if up_or_down == 'up' and y == year and month == month_assigned}

    # Sort the data by hour for both downward and upward variation
    sorted_down_data = sorted(down_data_year.items())
    sorted_up_data = sorted(up_data_year.items())

    # Split into two lists for plotting downward variation
    down_hours, down_variations = zip(*sorted_down_data)

    # Split into two lists for plotting upward variation
    up_hours, up_variations = zip(*sorted_up_data)

    # Create the plot for downward variation
    plt.plot(down_hours, down_variations, label=f'Downward PV Variation in {year}, '+month_assigned)

    # Create the plot for upward variation
    plt.plot(up_hours, up_variations, label=f'Upward PV Variation in {year}, '+month_assigned)

# Set the title and labels
plt.title('Variation per GW gas ' + month_assigned + ' from 2025 to 2030',fontsize=16)
plt.xlabel('Hour of the day',fontsize=16)
plt.ylabel('Variation per GW gas',fontsize=16)
# X軸的刻度從0到23
plt.xticks(range(0, 24, 1))
#放大軸刻度的字體還有軸座標標題的字體
plt.tick_params(axis='both', labelsize=16)
#放大圖例的字體
plt.legend(fontsize=16)

plt.legend()
# Show the plot
plt.show()

#endregion 