import streamlit as st
import pandas as pd
import os

# إعداد الصفحة
st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ")

def find_excel_file():
    # البحث عن أي ملف ينتهي بـ xlsx أو xls في المجلد
    for file in os.listdir("."):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            return file
    return None

file_path = find_excel_file()

if file_path:
    try:
        # قراءة الملف - نبدأ من السطر 15 لتجاوز الشعارات
        df = pd.read_excel(file_path, header=15)
        
        # تنظيف البيانات
        df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)
        
        # استخراج قائمة الأسماء (العمود الأول)
        raw_names = df.iloc[:, 0].dropna().astype(str).unique()
        names = sorted([n.strip() for n in raw_names if len(n.strip()) > 3])

        selected_doc = st.selectbox("👤 اختر اسمك من القائمة لمعرفة جدولك", ["اختر اسمك من هنا..."] + names)
        
        if selected_doc != "اختر اسمك من هنا...":
            # البحث عن سطر الطبيب
            result = df[df.iloc[:, 0].astype(str) == selected_doc]
            if not result.empty:
                st.success(f"الجدول الخاص بـ: {selected_doc}")
                st.dataframe(result, use_container_width=True)
            else:
                st.warning("الرجاء اختيار اسم صحيح من القائمة.")
        
        st.divider()
        with st.expander("🔍 عرض الجدول الكامل للمستشفى"):
            st.dataframe(df)
            
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
else:
    st.error("❌ لم يتم العثور على أي ملف إكسيل في المستودع.")
    st.info("تأكد أنك قمت برفع ملف الإكسيل في الصفحة الرئيسية بجانب ملف app.py")
