import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="نظام مناوبات البشير الملون", layout="wide")
st.title("🏥 نظام توزيع الأطباء حسب القاعات والوردينات")

@st.cache_data
def load_data():
    for file in os.listdir("."):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            try:
                # القراءة من السطر 16 حيث تبدأ البيانات الفعلية
                df = pd.read_excel(file, header=16)
                df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)
                # تسمية العمود الأول بـ "الاسم" والعمود الثاني بـ "القاعة/المنطقة"
                df.columns.values[0] = "الاسم"
                df.columns.values[1] = "القاعة"
                return df
            except:
                continue
    return None

df = load_data()

# دالة لتلوين الصفوف بناءً على القاعة
def color_zones(val):
    color = ''
    if 'خضراء' in str(val) or 'Green' in str(val):
        color = 'background-color: #d4edda' # أخضر فاتح
    elif 'صفراء' in str(val) or 'Yellow' in str(val):
        color = 'background-color: #fff3cd' # أصفر فاتح
    elif 'إنعاش' in str(val) or 'Resuscitation' in str(val):
        color = 'background-color: #f8d7da' # أحمر فاتح (للإنعاش)
    elif 'حمراء' in str(val) or 'Red' in str(val):
        color = 'background-color: #f8d7da'
    return color

if df is not None:
    tab1, tab2 = st.tabs(["👤 بحث بالاسم (تحديد القاعة)", "📊 الجدول الكامل الملون"])

    with tab1:
        st.subheader("ابحث عن اسمك لمعرفة قاعتك ووقت دوامك")
        all_names = df["الاسم"].dropna().astype(str).unique()
        names = sorted([n.strip() for n in all_names if len(n.strip()) > 3])
        
        selected_doc = st.selectbox("اختر اسم الطبيب", ["اختر من القائمة..."] + names)
        
        if selected_doc != "اختر من القائمة...":
            result = df[df["الاسم"].astype(str) == selected_doc]
            if not result.empty:
                # تطبيق التلوين على نتيجة البحث
                st.success(f"النتيجة للطبيب: {selected_doc}")
                st.style.apply(lambda x: [color_zones(result.iloc[0, 1])] * len(x), axis=1)
                st.table(result) # عرض الجدول ليكون واضحاً وثابتاً
            else:
                st.warning("لم يتم العثور على بيانات.")

    with tab2:
        st.subheader("الجدول الكامل مصنفاً حسب الألوان")
        # تطبيق التلوين على كل خلية في عمود القاعة
        styled_df = df.style.applymap(color_zones, subset=['القاعة'])
        st.dataframe(styled_df, use_container_width=True)

else:
    st.error("يرجى التأكد من رفع ملف الإكسيل باسم data.xlsx")
