import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة بتصميم احترافي
st.set_page_config(page_title="نظام مناوبات البشير الذكي", layout="wide")

# تصميم CSS لتحسين شكل البطاقات والنتائج
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput>div>div>input { border-radius: 15px; border: 2px solid #1a73e8; padding: 10px; }
    .duty-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-right: 6px solid #1a73e8;
        margin-bottom: 15px;
    }
    .zone-text { color: #1a73e8; font-weight: bold; font-size: 18px; }
    .shift-badge { 
        background-color: #e8f0fe; 
        color: #1a73e8; 
        padding: 4px 12px; 
        border-radius: 8px; 
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 نظام توزيع أطباء البشير - الإصدار الشامل")
st.write("مايو 2026 - عرض القاعات والشفتات")

@st.cache_data
def load_data():
    # البحث عن ملف البيانات (data.xlsx)
    for file in os.listdir("."):
        if file.startswith("data") and file.endswith((".xlsx", ".xls")):
            try:
                df = pd.read_excel(file)
                return df
            except:
                continue
    return None

df = load_data()

if df is not None:
    # محرك البحث بالاسم
    search_query = st.text_input("🔍 ابحث عن اسمك لمعرفة قاعتك وشفتك (مثلاً: أسامة، حسام، أحمد):", "")

    if search_query:
        # البحث بمرونة في عمود "اسم الطبيب / المقيم"
        # تأكد أن اسم العمود في الإكسيل يطابق: "اسم الطبيب / المقيم"
        try:
            mask = df.iloc[:, 3].astype(str).str.contains(search_query, case=False, na=False)
            results = df[mask]

            if not results.empty:
                st.write(f"### ✅ تم العثور على {len(results)} مناوبات مسجلة:")
                
                for _, row in results.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class="duty-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <span class="label">📅 التاريخ:</span> <b>{row.iloc[2]}</b> | 
                                    <span class="label">👤 الطبيب:</span> <b>{row.iloc[3]}</b>
                                </div>
                                <div class="shift-badge">شفت: {row.iloc[1]}</div>
                            </div>
                            <div style="margin-top: 10px;">
                                📍 القاعة: <span class="zone-text">{row.iloc[0]}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("❌ لم يتم العثور على هذا الاسم في الجدول.")
        except Exception as e:
            st.warning("يرجى التأكد من أن الجدول يحتوي على الأعمدة: القاعة، الشفت، التاريخ، الاسم.")
    
    st.divider()
    with st.expander("📊 معاينة أوقات الشفتات الرسمية"):
        st.info("A (08-16) | B (16-23) | C (23-08) | D (08-20) | [span_2](start_span)Night (20-08)")[span_2](end_span)
        st.dataframe(df, use_container_width=True)
else:
    st.error("❌ لم يتم العثور على ملف data.xlsx في GitHub.")

st.caption("نظام داخلي - مستشفيات البشير")
