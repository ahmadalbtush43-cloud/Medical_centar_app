import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .doc-card { 
        background: white; padding: 20px; border-radius: 10px; 
        border-right: 10px solid #28a745; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ")

@st.cache_data
def load_data():
    files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
    if not files: return None
    try:
        # قراءة الملف بالكامل
        df = pd.read_excel(files[0])
        return df
    except: return None

df = load_data()

if df is not None:
    # خانة البحث
    name_input = st.text_input("🔍 اكتب اسم الطبيب (مثلاً: أسامة):", "")

    if name_input:
        # البحث عن الاسم في كل الجدول
        mask = df.astype(str).apply(lambda row: row.str.contains(name_input, case=False, na=False).any(), axis=1)
        res = df[mask]
        
        if not res.empty:
            for i, row in res.iterrows():
                # محاولة استخراج القاعة آلياً
                row_text = " ".join(row.astype(str))
                qaa = "غير محدد"
                for k in ['خضراء', 'صفراء', 'حمراء', 'إنعاش', 'فرز']:
                    if k in row_text: qaa = k; break
                
                st.markdown(f"""
                <div class="doc-card">
                    <h3>👨‍⚕️ تفاصيل المناوبة</h3>
                    <p><b>القاعة:</b> {qaa}</p>
                    <p><b>الاسم الكامل:</b> {name_input}</p>
                </div>
                """, unsafe_allow_html=True)
                st.write("---")
                st.dataframe(res.loc[[i]].dropna(axis=1), use_container_width=True)
        else:
            st.warning("لم يتم العثور على الاسم، تأكد من رفعه في GitHub.")
    
    with st.expander("📊 عرض الجدول الكامل"):
        st.dataframe(df)
else:
    st.error("❌ ملف data.xlsx غير موجود في GitHub. يرجى رفعه أولاً.")
