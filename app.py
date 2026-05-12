import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ - مستشفيات البشير")

@st.cache_data
def load_data():
    try:
        # تحميل الملف وتجاوز الأسطر الإدارية في الأعلى
        df = pd.read_excel("data.xlsx", header=16) 
        # حذف الأعمدة الفارغة تماماً
        df = df.dropna(how='all', axis=1)
        # تسمية العمود الأول بـ "الاسم" إذا لم يكن مسمى
        df.rename(columns={df.columns[0]: 'الاسم'}, inplace=True)
        return df
    except Exception as e:
        st.error(f"تأكد من وجود ملف باسم data.xlsx. الخطأ: {e}")
        return None

df = load_data()

if df is not None:
    tab1, tab2 = st.tabs(["👤 بحث بالاسم", "🔍 الجدول كاملاً"])

    with tab1:
        st.subheader("ابحث عن اسمك لمعرفة أيام مناوباتك")
        
        # استخراج الأسماء من أول عمود وتنظيفها
        all_names = df.iloc[:, 0].dropna().astype(str).unique()
        names = sorted([n.strip() for n in all_names if len(n.strip()) > 3])
        
        selected_doc = st.selectbox("اختر اسم الطبيب", names)
        
        if selected_doc:
            # البحث عن الصف الخاص بالطبيب
            result = df[df.iloc[:, 0].astype(str) == selected_doc]
            
            if not result.empty:
                st.success(f"جدول المناوبات لـ: {selected_doc}")
                # تنظيف النتيجة من القيم الفارغة قبل العرض
                clean_result = result.dropna(how='all', axis=1)
                st.dataframe(clean_result, use_container_width=True)
                
                st.info("ملاحظة: الأرقام في الجدول تمثل أيام الشهر (1 إلى 31) ورموز الوردينات.")
            else:
                st.warning("لم يتم العثور على بيانات لهذا الاسم.")

    with tab2:
        st.subheader("معاينة الجدول العام")
        st.dataframe(df)
else:
    st.info("يرجى التأكد من رفع ملف 'data.xlsx' على GitHub.")
