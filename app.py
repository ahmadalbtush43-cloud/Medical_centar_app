import streamlit as st
import pandas as pd
import os

# إعداد الصفحة وتصميم احترافي
st.set_page_config(page_title="نظام مناوبات أطباء البشير", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stAlert { border-radius: 10px; }
    th { background-color: #f0f2f6 !省f; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ")
st.write("---")

@st.cache_data
def load_data():
    # البحث عن أي ملف إكسيل مرفوع
    files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
    if not files:
        return None
    try:
        # قراءة الملف بدون تحديد هيدر (سنعالجه يدوياً)
        df = pd.read_excel(files[0])
        return df
    except:
        return None

df = load_data()

if df is not None:
    # تنظيف بدائي للبيانات
    df_clean = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
    
    tab1, tab2 = st.tabs(["👤 بحث سريع عن طبيب", "📊 عرض الجدول الكامل"])

    with tab1:
        st.subheader("ابحث عن اسمك لمعرفة قاعتك ومناوبتك")
        # تحويل كل الجدول لنصوص للبحث فيها
        search_term = st.text_input("اكتب جزءاً من الاسم (مثلاً: حسام أو أسامة)", "")
        
        if search_term:
            # البحث في كل خلايا الجدول عن هذا الاسم
            mask = df_clean.astype(str).apply(lambda row: row.str.contains(search_term, case=False, na=False).any(), axis=1)
            results = df_clean[mask]
            
            if not results.empty:
                st.success(f"تم العثور على {len(results)} سجلات تطابق: {search_term}")
                st.dataframe(results, use_container_width=True)
            else:
                st.warning("لم يتم العثور على هذا الاسم، تأكد من كتابته بشكل صحيح.")
        else:
            st.info("الرجاء كتابة الاسم في مربع البحث أعلاه.")

    with tab2:
        st.subheader("جدول المستشفى كاملاً")
        st.write("يمكنك سحب الجدول يميناً ويساراً لمشاهدة كافة الأيام")
        st.dataframe(df_clean, use_container_width=True)

else:
    st.error("❌ لم نجد ملف الإكسيل (data.xlsx) في المستودع.")
    st.info("تأكد أنك قمت برفع ملف الإكسيل في الصفحة الرئيسية لـ GitHub بجانب ملف app.py")

st.write("---")
st.caption("نظام داخلي خاص بمستشفيات البشير - قسم الإسعاف والطوارئ")
