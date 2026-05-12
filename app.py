import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ - مستشفيات البشير")

@st.cache_data
def load_data():
    try:
        # قراءة ملف الإكسيل وتجاهل أول 10 أسطر إدارية
        df = pd.read_excel("data.xlsx", header=10)
        return df
    except Exception as e:
        st.error(f"تأكد من وجود ملف باسم data.xlsx. الخطأ: {e}")
        return None

df = load_data()

if df is not None:
    tab1, tab2 = st.tabs(["👤 بحث بالاسم (متى دوامي؟)", "🔍 عرض الجدول الكامل"])

    with tab1:
        st.subheader("اختر اسمك لمعرفة أيام مناوباتك")
        
        # استخراج قائمة الأسماء من العمود رقم 14 (الذي يحتوي الأسماء في ملفك)
        # قمنا بتنظيفها من أي قيم فارغة أو نصوص غير ضرورية
        if df.shape[1] > 14:
            raw_names = df.iloc[:, 14].dropna().astype(str).unique()
            names = sorted([n.strip() for n in raw_names if len(n.strip()) > 5])
            
            selected_doc = st.selectbox("اختر اسم الطبيب من القائمة", names)
            
            if selected_doc:
                # البحث عن الصفوف التي تحتوي على اسم الطبيب المختار
                mask = df.astype(str).apply(lambda row: row.str.contains(selected_doc, na=False).any(), axis=1)
                result = df[mask]
                
                if not result.empty:
                    st.success(f"تم العثور على سجلات لـ: {selected_doc}")
                    # عرض النتيجة كجدول مبسط
                    st.dataframe(result.dropna(how='all', axis=1))
                else:
                    st.warning("لم يتم العثور على أيام دوام مسجلة بهذا الاسم.")
        else:
            st.error("يبدو أن بنية ملف الإكسيل تختلف، يرجى التأكد من رفع الملف الصحيح.")

    with tab2:
        st.subheader("معاينة الملف الأصلي")
        st.dataframe(df)
else:
    st.info("بانتظار معالجة ملف data.xlsx...")
