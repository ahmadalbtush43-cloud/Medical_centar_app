import streamlit as st
import pandas as pd
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ - مستشفيات البشير")

@st.cache_data
def load_data():
    try:
        # قراءة الملف بالكامل وتجاهل الترويسة الإدارية
        df = pd.read_excel("data.xlsx")
        return df
    except Exception as e:
        st.error(f"تأكد من وجود ملف باسم data.xlsx. الخطأ: {e}")
        return None

df = load_data()

if df is not None:
    tab1, tab2 = st.tabs(["👤 بحث بالاسم (متى دوامي؟)", "🔍 عرض الجدول الكامل"])

    with tab1:
        st.subheader("ابحث عن اسمك لمعرفة أيام مناوباتك")
        
        # استخراج كافة النصوص من الجدول للبحث عن الأسماء
        all_entries = df.astype(str).values.flatten()
        # تنقية الأسماء (أي خلية تحتوي على حرف د وبعدها مسافة أو نقطة)
        names = sorted(list(set([str(x).strip() for x in all_entries if "د." in str(x) or "د " in str(x)])))
        
        if names:
            selected_doc = st.selectbox("اختر اسم الطبيب من القائمة", names)
            
            # البحث عن الصفوف التي يظهر فيها الاسم
            mask = df.astype(str).apply(lambda row: row.str.contains(selected_doc, na=False).any(), axis=1)
            result = df[mask].dropna(how='all', axis=1)
            
            st.success(f"تم العثور على اسم {selected_doc} في السجلات التالية:")
            st.dataframe(result)
        else:
            st.warning("لم يتم العثور على أسماء أطباء في الملف. تأكد من أن الأسماء تبدأ بـ 'د.'")

    with tab2:
        st.subheader("معاينة الجدول الأصلي")
        st.write("يمكنك مراجعة الملف المرفوع بالكامل هنا:")
        st.dataframe(df)
else:
    st.info("جاري تحميل البيانات من ملف data.xlsx...")
