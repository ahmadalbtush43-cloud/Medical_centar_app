import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة بتصميم عصري
st.set_page_config(page_title="نظام مناوبات البشير الذكي", layout="wide")

# تصميم واجهة المستخدم بلغة CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput>div>div>input { border-radius: 10px; border: 2px solid #007bff; }
    .doctor-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-right: 5px solid #007bff;
        margin-bottom: 20px;
    }
    .zone-badge {
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ")
st.write("مستشفيات البشير - الإصدار الذكي المنظم")

@st.cache_data
def load_data():
    # البحث عن الملف الذي قمت برفعه
    for file in os.listdir("."):
        if file.endswith((".xlsx", ".xls")):
            try:
                # قراءة الملف (يفترض أن الاسم في العمود الأول أو الثاني)
                df = pd.read_excel(file)
                return df, file
            except:
                continue
    return None, None

df, file_name = load_data()

if df is not None:
    # تنظيف البيانات من الأسطر الفارغة تماماً
    df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
    
    st.info(f"📁 تم تحميل الجدول بنجاح")

    # البحث الذكي
    search_query = st.text_input("🔍 اكتب اسمك هنا للبحث (مثلاً: حسام، أسامة، أحمد...)", "")

    if search_query:
        # البحث في كافة الخلايا
        mask = df.astype(str).apply(lambda row: row.str.contains(search_query, case=False, na=False).any(), axis=1)
        results = df[mask]

        if not results.empty:
            for index, row in results.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="doctor-card">
                        <h3>👨‍⚕️ تفاصيل المناوبة</h3>
                        <p style='font-size: 18px;'><b>البيانات المستخرجة:</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.dataframe(results.loc[[index]].dropna(axis=1), use_container_width=True)
        else:
            st.error("❌ لم يتم العثور على نتائج لهذا الاسم.")
    else:
        st.write("💡 **نصيحة:** اكتب أول حرفين من اسمك فقط لتظهر لك النتائج بسرعة.")

    st.divider()
    with st.expander("📊 عرض الجدول الكامل للمستشفى"):
        st.dataframe(df)
else:
    st.error("❌ لم يتم العثور على ملف الجدول (data.xlsx).")
