import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ - مستشفيات البشير")

@st.cache_data
def load_data():
    try:
        # قراءة الملف - جربنا التحميل من السطر 11
        df = pd.read_excel("data.xlsx", header=None)
        return df
    except Exception as e:
        st.error(f"تأكد من وجود ملف باسم data.xlsx. الخطأ: {e}")
        return None

df = load_data()

if df is not None:
    tab1, tab2 = st.tabs(["🔍 بحث بالتاريخ", "👤 بحث بالاسم"])

    with tab1:
        st.subheader("جدول المناوبات حسب التاريخ")
        # اختيار اليوم من 1 إلى 31 (حسب شهر 5)
        day_selected = st.slider("اختر يوم الشهر (مايو)", 1, 31, datetime.now().day)
        st.info(f"عرض جدول يوم {day_selected} / 5 / 2026")
        # عرض الجدول بشكل كامل لمراجعته
        st.dataframe(df)

    with tab2:
        st.subheader("ابحث عن اسمك لمعرفة أيام دوامك")
        # استخلاص كل الكلمات من الجدول وتحويلها لقائمة أسماء
        all_text = df.astype(str).values.flatten()
        names = sorted(list(set([name for name in all_text if "د." in name or "د " in name])))
        
        if names:
            selected_doc = st.selectbox("اختر اسم الطبيب", names)
            st.success(f"نتائج البحث عن: {selected_doc}")
            # فلترة الصفوف التي تحتوي على الاسم
            mask = df.apply(lambda row: row.astype(str).str.contains(selected_doc).any(), axis=1)
            result = df[mask]
            st.table(result)
        else:
            st.warning("لم يتم العثور على أسماء تبدأ بـ 'د.' في الملف. يرجى التأكد من محتوى الإكسيل.")
else:
    st.info("بانتظار معالجة البيانات...")
