import pandas as pd
from datetime import datetime, timedelta

# 1. إعداد البيانات الأساسية
total_doctors = 78
zones = ['Zone A', 'Zone B', 'Zone C']
days_to_schedule = 30  # عدد الأيام المطلوب جدولة شفتاتها
start_date = datetime.now()

# 2. تقسيم الأطباء إلى 4 مجموعات (لتحقيق نظام: يوم عمل مقابل 3 أيام إجازة)
# كل مجموعة تحتوي على 19 أو 20 طبيب
doctors_list = [f"Doctor {i+1}" for i in range(total_doctors)]
teams = [doctors_list[i::4] for i in range(4)]

schedule_data = []

# 3. خوارزمية توزيع الشفتات
for day in range(days_to_schedule):
    current_date = start_date + timedelta(days=day)
    
    # تحديد أي فريق عليه الدور اليوم (Rotation)
    team_idx = day % 4
    current_team = teams[team_idx]
    
    # توزيع أطباء الفريق الحالي على المناطق A, B, C بالتساوي
    for i, doc in enumerate(current_team):
        zone = zones[i % len(zones)]
        schedule_data.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Day": current_date.strftime("%A"),
            "Doctor Name": doc,
            "Assigned Zone": zone,
            "Team": f"Team {team_idx + 1}"
        })

# 4. تحويل البيانات إلى جدول منظم
df = schedule_data
# يمكن تصدير هذا الجدول إلى ملف Excel
print("تم إنشاء هيكل الجدول بنجاح.")
