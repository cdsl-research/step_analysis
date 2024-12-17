import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import matplotlib
import os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import calendar
import numpy as np
from collections import defaultdict

# 歩数データ先
xml_file_path = 'sakai_export.xml'  # xmlファイルのパス

# 曜日切り替え
weekday_num = 0
weekday_Eng = calendar.day_abbr[weekday_num]

# 8/8~10/16
start_date = datetime(2024, 8, 8)
end_date = datetime(2024, 10, 16)


# 歩数の処理する関数
def step_count_weekdays(xml_file, start_date, end_date):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    weekly_counts = defaultdict(lambda: defaultdict(int))
    # 24時間を各10分で分割したリスト
    time_slots = [(datetime(2024, 1, 1, 0, 0) + timedelta(minutes=10 * i)).strftime('%H:%M') for i in range(144)]
    step_count_summary = [{ 'time': time, 'weeks_over_200': 0 } for time in time_slots]

    for record in root.findall('Record'):
        if record.get('type') == 'HKQuantityTypeIdentifierStepCount':
            start_date_str = record.get('startDate')
            value = int(record.get('value'))

            # 日付を変換
            start_date_dt = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S %z')
            start_date_dt = start_date_dt.replace(tzinfo=None)
            
            if (start_date <= start_date_dt <= end_date) & (start_date_dt.weekday() == weekday_num):
                target_time = start_date_dt.replace(minute=(start_date_dt.minute // 10) * 10, second=0)
                interval_key = target_time.strftime('%H:%M')
                date_key = start_date_dt.date()
                
                # weekly_counts[特定の10分][特定の日]　にその歩数を記録
                weekly_counts[interval_key][date_key] += value
                
    return step_count_summary, weekly_counts


# グラフ作成
def plot_graph(step_count_summary, weekly_counts, save_path):
    times = [record['time'] for record in step_count_summary]

    fig, ax = plt.subplots(figsize=(15, 6))

    # 各曜日の歩数の合計を計算して折れ線グラフとして追加
    weekday_step_totals = []
    for time_slot in times:
        daily_total_steps = [weekly_counts[time_slot].get(date, 0) for date in weekly_counts[time_slot]]
        weekday_step_totals.append(np.sum(daily_total_steps))

    ax.plot(range(len(times)), weekday_step_totals, color='red', label='Total Steps', linestyle='-', marker='o')
    ax.set_xlim(0, len(times) - 1)
    ax.set_ylim(0, 8000)

    plt.xticks(range(0, len(times), 6), times[::6], rotation=90)
    plt.xlabel('Time')
     
    plt.title(f'{start_date}~{end_date} ({weekday_Eng}) step graph')

    plt.grid(True, axis='y')
    plt.legend()
    plt.tight_layout()

    # 保存先指定
    plt.savefig(save_path)
    plt.close()


# 出力
for week in range(0, 7):
    # 曜日切り替え
    weekday_num = week
    weekday_Eng = calendar.day_abbr[weekday_num]

    step_count_summary, weekly_counts = step_count_weekdays(xml_file_path, start_date, end_date)

    start_output = start_date.strftime('%Y-%m-%d')
    end_output = end_date.strftime('%Y-%m-%d')
    plot_graph(step_count_summary, weekly_counts, f'/home/c0a2206905/step_analysis/makepng/{start_output}_{end_output}_{weekday_Eng}_step_graph.png')
