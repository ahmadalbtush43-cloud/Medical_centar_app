import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ")

# دالة لقراءة البيانات
@st.cache_data
def load_data():
    try:
        # قراءة ملف الإكسيل الذي رفعته
        df = pd.read_excel("data.xlsx", header=10) 
        return df
    except:
        return None

df = load_data()

if df is not None:
    tab1, tab2 = st.tabs(["🔍 بحث بالتاريخ", "👤 بحث بالاسم"])

    with tab1:
        st.subheader("من هم المداومون اليوم؟")
        date_query = st.date_input("اختر التاريخ", datetime.now())
        st.info("سيظهر توزيع الأطباء هنا بناءً على التاريخ المختار من ملفك.")
        st.dataframe(df.iloc[:, :10].head(20)) # عرض عينة من البيانات

    with tab2:
        st.subheader("متى دوامي؟")
        # استخراج الأسماء من عمود الأطباء (العمود رقم 14 في ملفك)
        names_list = df.iloc[:, 14].dropna().unique() 
        selected_doc = st.selectbox("اختر اسمك من القائمة", names_list)
        st.success(f"جدول المناوبات الخاص بـ {selected_doc}")
else:
    st.error("يرجى التأكد من رفع ملف 'data.xlsx' على GitHub.")
