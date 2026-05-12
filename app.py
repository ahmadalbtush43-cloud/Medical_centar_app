import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ")

@st.cache_data
def load_data():
    # البحث عن أي ملف إكسيل في المجلد
    files = [f for f in os.listdir('.') if f.endswith('.xlsx') or f.endswith('.csv')]
    if not files:
        return None, "لا يوجد ملف إكسيل في المستودع"
    
    target_file = files[0] # سيأخذ أول ملف إكسيل يجده
    try:
        if target_file.endswith('.csv'):
            df = pd.read_csv(target_file)
        else:
            # محاولة القراءة من عدة أسطر ترويسة لضمان الوصول للأسماء
            df = pd.read_excel(target_file, header=15)
        return df, target_file
    except Exception as e:
        return None, str(e)

df, file_name = load_data()

if df is not None:
    st.sidebar.success(f"متصل بملف: {file_name}")
    
    # تنظيف البيانات
    df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    # استخراج الأسماء (العمود الأول عادة)
    try:
        raw_names = df.iloc[:, 0].dropna().astype(str).unique()
        names = sorted([n.strip() for n in raw_names if "د." in n or "د " in n or len(n) > 5])

        selected_doc = st.selectbox("👤 اختر اسم الطبيب من القائمة المنسدلة", ["اختر الاسم..."] + names)
        
        if selected_doc != "اختر الاسم...":
            # البحث عن سطر الطبيب بمرونة
            result = df[df.iloc[:, 0].astype(str).str.contains(selected_doc, na=False)]
            st.success(f"الجدول الخاص بـ: {selected_doc}")
            st.dataframe(result, use_container_width=True)
    except:
        st.warning("يرجى اختيار الاسم لعرض الجدول")

    st.divider()
    with st.expander("🔍 عرض الجدول الكامل"):
        st.dataframe(df)
else:
    st.error("❌ لم يتم العثور على ملف البيانات. يرجى رفع ملف الإكسيل على GitHub.")
    st.info("نصيحة: تأكد أنك قمت برفع ملف الإكسيل في القسم الرئيسي (Main) بجانب ملف app.py")
