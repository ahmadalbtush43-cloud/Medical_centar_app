import pandas as pd

# قراءة ملف البيانات
file_path = 'data.xlsx - Sheet1.csv'
df = pd.read_csv(file_path)

# تنظيف البيانات (إزالة الأعمدة الفارغة إذا وجدت)
df = df.dropna(axis=1, how='all')

# عرض أول 5 أسطر للتأكد من القراءة الصحيحة
print("نظرة عامة على البيانات:")
print(df.head())

# مثال: استخراج قائمة بالأطباء في قاعة معينة (مثلاً Triage)
triage_doctors = df[df['اسم القاعه'].str.contains('Triage', na=False)]
print("\nأطباء منطقة الترياج (Triage):")
print(triage_doctors[['اسم الطبيب /المقيم', 'التاريخ']])

# حفظ نسخة منظمة من البيانات إذا أردت
# df.to_csv('cleaned_medical_data.csv', index=False)
