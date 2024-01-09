import matplotlib
import pandas as pd
import streamlit as st
from calculateGPA import CalGPA
import matplotlib.pyplot as plt

# 设置字体为支持中文的字体，例如 'SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

file_path = 'data/all_scores.csv'
df = pd.read_csv(file_path)
CalGPA = CalGPA(df)

st.title("成绩详情")
st.dataframe(df)
GPA = CalGPA.calMeanGPA()

st.title("修读情况总览")
st.table(GPA["total"])

st.title("修读情况详情")
st.table(GPA["detailed"])

st.title("绩点成长折线图")
# 将图形显示在Streamlit应用程序中
# 获取数据
data = GPA["detailed"][1]
# st.write(data)
x = [item for item in data.index]
y = [item for item in data]
# 绘制折线图
plt.plot(x, y)
plt.xlabel('学期')
plt.ylabel('平均绩点')
plt.title('GPA Plot')
st.pyplot(plt)
