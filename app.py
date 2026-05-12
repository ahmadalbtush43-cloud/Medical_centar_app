import pandas as pd
import os

# هذا السطر يضمن أن البرنامج يبحث عن الملف في نفس المجلد الذي يوجد فيه الكود
current_dir = os.path.dirname(os.path.abspath(__file__))
file_name = 'data.xlsx - Sheet1.csv'  # تأكد أن الاسم مطابق تماماً للاسم في المجلد
file_path = os.path.join(current_dir, file_name)

try:
    # قراءة الملف مع تحديد الترميز (Encoding) لدعم اللغة العربية
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    print("✅ تم تحميل البيانات بنجاح!")
    print(df.head())
except FileNotFoundError:
    print(f"❌ خطأ: لم يتم العثور على الملف في المسار: {file_path}")
    print("تأكد من وضع ملف الـ CSV في نفس مجلد الكود.")
except Exception as e:
    print(f"❌ حدث خطأ غير متوقع: {e}")
