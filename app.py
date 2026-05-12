import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="نظام مناوبات البشير", layout="wide")
st.title("🏥 نظام توزيع أطباء الإسعاف والطوارئ")

def load_data():
    for file in os.listdir("."):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            try:
                # نبدأ من السطر 16 حيث تبدأ الأسماء والزونات
                df = pd.read_excel(file, header=16)
                df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)
                return df
            except:
                continue
    return None

df = load_data()

if df is not None:
    # محاولة تسمية الأعمدة بناءً على محتوى ملفك (القاعة والاسم)
    if df.shape[1] > 0:
        df.rename(columns={df.columns[0]: 'الاسم'}, inplace=True)

    tab1, tab2 = st.tabs(["👤 ابحث عن اسمك (وقاعتك)", "📊 الجدول الكامل"])

    with tab1:
        st.subheader("ابحث عن اسمك لمعرفة يومك و(القاعة) المخصصة لك")
        
        all_names = df['الاسم'].dropna().astype(str).unique()
        names = sorted([n.strip() for n in all_names if len(n.strip()) > 3])
        
        selected_doc = st.selectbox("اختر اسم الطبيب", ["اختر..."] + names)
        
        if selected_doc != "اختر...":
            # البحث عن سطر الطبيب
            result = df[df['الاسم'].astype(str) == selected_doc]
            
            if not result.empty:
                st.success(f"تم العثور على بيانات الطبيب: {selected_doc}")
                
                # إظهار القاعة (غالباً العمود الأول أو الثاني يحتوي على الزون)
                # سنعرض الصف بالكامل ليتمكن من رؤية التقسيم
                st.dataframe(result, use_container_width=True)
                
                # رسالة توضيحية بناءً على محتوى الملف
                st.info("💡 ملاحظة: انظر إلى الأعمدة الأولى في الجدول أعلاه؛ ستجد اسم 'القاعة' (خضراء، صفراء، إنعاش) بجانب اسمك مباشرة.")
            else:
                st.warning("يرجى التأكد من اختيار الاسم الصحيح.")

    with tab2:
        st.subheader("معاينة شاملة لجميع القاعات والأطباء")
        st.dataframe(df)
else:
    st.error("لم يتم العثور على ملف data.xlsx. تأكد من رفعه في GitHub.")
