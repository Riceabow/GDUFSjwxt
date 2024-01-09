import matplotlib
import pandas as pd
import streamlit as st
from calculateGPA import CalGPA
import matplotlib.pyplot as plt

# 设置字体为支持中文的字体，例如 'SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

file_path = 'data/all_scores.csv'
df = pd.read_csv(file_path)
GPAcount = df['绩点'].value_counts()
GPAcount = GPAcount.sort_values(ascending=True)
CalGPA = CalGPA(df)

st.title("成绩详情")
st.dataframe(df)
GPA = CalGPA.calMeanGPA()

st.title("修读情况总览")
st.table(GPA["total"])

st.title("修读情况详情")
st.table(GPA["detailed"])

st.title("图表分析")
# 将图形显示在Streamlit应用程序中
# 获取数据
data = GPA["detailed"][1]
# st.write(data)
x = [item for item in data.index]
y = [item for item in data]

# 创建第一个图像
fig1, ax1 = plt.subplots()
ax1.plot(x, y)
ax1.set_xlabel('学期')
ax1.set_ylabel('平均绩点')
ax1.set_title('GPA学期成长变化折线图')
st.pyplot(fig1)

# 创建第二个图像
fig2, ax2 = plt.subplots()
ax2.set_title("绩点分布柱状图")
ax2.set_xlabel("绩点")
ax2.set_ylabel("频数")
ax2.set_yticks([i for i in range(int(GPAcount.min()), int(GPAcount.max()) + 1)])
GPAcount.plot(kind='bar', ax=ax2)
st.pyplot(fig2)
