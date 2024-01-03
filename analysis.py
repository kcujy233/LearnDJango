# 标签 (字典的键)
qual_labels = qual_dict.keys()
salary_labels = salary_dict.keys()
# 数值 (字典的值)
qual_sizes = qual_dict.values()
salary_sizes = salary_dict.values()
'''学历图'''
plt.figure(figsize=(10, 6)) # 设置画布大小
plt.pie(qual_sizes, labels=qual_labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('企业对学历的要求')

'''薪资图'''
plt.figure(1)
plt.figure(figsize=(10, 6))  # 设置画布大小
plt.pie(salary_sizes, labels=salary_labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title("最低薪资占比")

'''词云图'''
# 创建WordCloud对象，并设置参数
# wc = WordCloud(width=800, height=400)
wc = WordCloud(font_path='C:/Windows/Fonts/等线/Deng.ttf', width=800, height=400)
wc.generate_from_frequencies(stop_dict)
plt.figure(2)
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")  # 不显示坐标轴
plt.title("岗位词云图")
plt.show()