
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
 
إعداد واجهة التطبيق
st.set_page_config(page_title="نظام جدولة المركز الطبي", layout="wide")
st.title("🏥 نظام إدارة شفتات الأطباء والزونات")
 
إعداد البيانات الأساسية (78 طبيب و 4 مجموعات)
total_doctors = 78
teams_count = 4
doctors = [f"دكتور {i+1}" for i in range(total_doctors)]
teams = [doctors[i::teams_count] for i in
 
range(teams_count)]
zones = ['المنطقة A', 'المنطقة B', 'المنطقة C']
 
اختيار التاريخ من قبل المستخدم
selected_date = st.date_input("اختر التاريخ لعرض الجدول", datetime.now())
 
حساب اليوم لمعرفة أي فريق عليه الدور (يوم عمل و3 أيام إجازة)
نستخدم تاريخ مرجعي ثابت لضبط الدورة
reference_date = datetime(2026, 5, 1).date()
days_diff = (selected_date - reference_date).days
team_idx = days_diff % teams_count
 
current_team = teams[team_idx]
 
 
توزيع الفريق الحالي على المناطق
schedule_list = []
for i, doc in enumerate(current_team):
zone = zones[i % len(zones)]
schedule_list.append({"الطبيب": doc, "المنطقة": zone, "الفريق": f"مجموعة {team_idx + 1}"})
 
عرض النتائج في التطبيق
st.subheader(f"جدول يوم: {selected_date}")
st.info(f"الفريق المناوب اليوم: المجموعة {team_idx + 1}")
 
df = pd.DataFrame(schedule_list)
st.table(df)
 
زر لتحميل الجدول كملف Excel
st.download_button(
label="تحميل الجدول كملف Excel",
data=df.to_csv(index=False).encode('utf-8-sig'),
file_name=f'schedule_{selected_date}.csv',
mime='text/csv',
