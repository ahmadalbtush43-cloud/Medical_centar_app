import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ")

@st.cache_data
def load_data():
    try:
        # قراءة الملف مع تجاوز أول 15 سطر (الترويسة الإدارية)
        df = pd.read_excel("data.xlsx", header=15)
        # تنظيف الأعمدة التي لا تحتوي على أسماء أو بيانات
        df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)
        return df
    except Exception as e:
        st.error(f"تأكد من اسم الملف data.xlsx. الخطأ: {e}")
        return None

df = load_data()

if df is not None:
    # قائمة الأسماء من العمود الأول
    raw_names = df.iloc[:, 0].dropna().astype(str).unique()
    names = sorted([n.strip() for n in raw_names if len(n.strip()) > 3])

    selected_doc = st.selectbox("👤 اختر اسم الطبيب من القائمة", names)
    
    if selected_doc:
        # البحث عن سطر الطبيب
        result = df[df.iloc[:, 0].astype(str) == selected_doc]
        if not result.empty:
            st.success(f"الجدول الخاص بـ: {selected_doc}")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("اختر اسماً من القائمة لعرض التفاصيل.")
            
    st.divider()
    with st.expander("🔍 عرض الجدول الكامل للمستشفى"):
        st.dataframe(df)
else:
    st.info("جاري مزامنة البيانات...")
