import streamlit as st
import pandas as pd
import os

# إعداد الصفحة وتوسيع العرض
st.set_page_config(page_title="نظام توزيع أطباء البشير", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stDataFrame { border: 1px solid #e6e9ef; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ - مستشفيات البشير")

@st.cache_data
def load_data():
    for file in os.listdir("."):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            try:
                # القراءة من السطر 15 لتجاوز الترويسة
                df = pd.read_excel(file, header=15)
                # حذف الأعمدة والصفوف الفارغة تماماً
                df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)
                # تسمية الأعمدة الأساسية
                df.columns.values[0] = "المنطقة / القاعة"
                df.columns.values[1] = "اسم الطبيب"
                return df
            except:
                continue
    return None

df = load_data()

# دالة ذكية لتلوين القاعات بناءً على المسميات في ملفك
def style_zones(row):
    color = ''
    zone = str(row['المنطقة / القاعة']).lower()
    if 'خضراء' in zone or 'green' in zone:
        color = 'background-color: #d4edda; color: #155724; font-weight: bold;'
    elif 'صفراء' in zone or 'yellow' in zone:
        color = 'background-color: #fff3cd; color: #856404; font-weight: bold;'
    elif 'حمراء' in zone or 'red' in zone or 'إنعاش' in zone:
        color = 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    return [color] * len(row)

if df is not None:
    tab1, tab2 = st.tabs(["👤 بحث بالاسم (وقاعتك)", "📊 الجدول الملون الكامل"])

    with tab1:
        st.subheader("ابحث عن اسمك لمعرفة قاعتك ومناوبتك")
        all_names = df["اسم الطبيب"].dropna().astype(str).unique()
        names = sorted([n.strip() for n in all_names if len(n.strip()) > 3])
        
        selected_doc = st.selectbox("اختر اسم الطبيب من القائمة المنسدلة", ["-- اختر الاسم --"] + names)
        
        if selected_doc != "-- اختر الاسم --":
            result = df[df["اسم الطبيب"].astype(str) == selected_doc]
            if not result.empty:
                st.success(f"النتيجة للطبيب: {selected_doc}")
                # عرض السطر الخاص بالطبيب مع التلوين
                st.write("تفاصيل المناوبة والقاعة:")
                st.table(result.style.apply(style_zones, axis=1))
            else:
                st.warning("لم يتم العثور على بيانات، تأكد من اختيار الاسم الصحيح.")

    with tab2:
        st.subheader("جدول المستشفى الكامل (مصنف بالألوان)")
        # تطبيق التلوين على الجدول بالكامل
        st.dataframe(df.style.apply(style_zones, axis=1), use_container_width=True)
else:
    st.error("يرجى رفع ملف 'data.xlsx' في المستودع ليعمل النظام.")
