import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ - مستشفيات البشير")

@st.cache_data
def load_data():
    try:
        # تحميل الملف - البدء من سطر الأسماء
        df = pd.read_excel("data.xlsx", header=16)
        # حذف الصفوف والأعمدة الفارغة تماماً
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        return df
    except Exception as e:
        st.error(f"تأكد من وجود ملف باسم data.xlsx. الخطأ: {e}")
        return None

df = load_data()

if df is not None:
    tab1, tab2 = st.tabs(["👤 بحث بالاسم", "🔍 الجدول العام"])

    with tab1:
        st.subheader("ابحث عن اسمك لمعرفة أيام مناوباتك")
        
        # استخراج الأسماء من أول عمود متوفر وتنظيفها
        first_column = df.columns[0]
        names = sorted(df[first_column].dropna().astype(str).unique())
        
        selected_doc = st.selectbox("اختر اسم الطبيب من القائمة", names)
        
        if selected_doc:
            # البحث بمرونة عن الاسم في العمود الأول
            result = df[df[first_column].astype(str).str.contains(selected_doc, na=False)]
            
            if not result.empty:
                st.success(f"جدول المناوبات لـ: {selected_doc}")
                # عرض النتيجة بشكل عرضي مريح
                st.dataframe(result, use_container_width=True)
                
                # إضافة تنبيه بسيط لشرح الرموز
                st.info("💡 ملاحظة: الرموز (A, B, C) تمثل وردياتك في الأيام المذكورة في الجدول أعلاه.")
            else:
                st.warning("تعذر عرض التفاصيل لهذا الاسم، جرب اختيار اسم آخر أو مراجعة الجدول العام.")

    with tab2:
        st.subheader("معاينة الجدول كاملاً")
        st.dataframe(df)
else:
    st.info("يرجى التأكد من رفع ملف 'data.xlsx' على GitHub.")
