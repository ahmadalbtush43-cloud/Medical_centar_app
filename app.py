import streamlit as st
import pandas as pd
import os

# تصميم الواجهة
st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الطوارئ - مستشفيات البشير")

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
    # قائمة القاعات الممكنة في ملفك
    zones_keywords = ['خضراء', 'صفراء', 'حمراء', 'إنعاش', 'فرز', 'جراحة', 'عظام']
    
    tab1, tab2 = st.tabs(["🔍 بحث بالاسم والقاعة", "📊 الجدول الكامل"])

    with tab1:
        search_name = st.text_input("اكتب اسم الطبيب هنا (مثلاً: حسام):", "")
        
        if search_name:
            # البحث عن الصفوف التي تحتوي على الاسم
            mask = df.astype(str).apply(lambda row: row.str.contains(search_name, case=False, na=False).any(), axis=1)
            results = df[mask].copy()
            
            if not results.empty:
                st.success(f"نتائج البحث لـ: {search_name}")
                
                # حركة ذكية: البحث عن "القاعة" في نفس الصف أو الصفوف القريبة
                def find_zone(row_idx):
                    # يبحث في أعمدة الصف المختار عن كلمة تدل على القاعة
                    row_content = " ".join(df.iloc[row_idx].astype(str))
                    for key in zones_keywords:
                        if key in row_content: return key
                    return "غير محدد"

                # إضافة عمود "القاعة المتوقعة" في العرض فقط
                results['القاعة / المنطقة'] = [find_zone(i) for i in results.index]
                
                # عرض النتيجة مرتبة
                st.write("### تفاصيل الدوام:")
                st.dataframe(results, use_container_width=True)
            else:
                st.warning("لم يتم العثور على الاسم.")

    with tab2:
        st.subheader("معاينة الجدول الأصلي")
        st.dataframe(df)
else:
    st.error("لم يتم العثور على ملف الإكسيل.")
