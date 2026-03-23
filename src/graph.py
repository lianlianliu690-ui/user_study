import pandas as pd
import matplotlib.pyplot as plt
import numpy as np





# 设置字体为 Times New Roman
# 设置支持中文字体，优先使用宋体
plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Times New Roman']


# 在设置 font.sans-serif 之后添加
plt.rcParams['font.weight'] = 'normal'       # 全局字体粗细
plt.rcParams['axes.labelweight'] = 'normal'  # 轴标签粗细
plt.rcParams['axes.titleweight'] = 'normal'  # 标题粗细

# 读取你的长格式数据
df = pd.read_excel("final_method_metric_stats.xlsx")  # 确保文件路径正确

# 方法和指标
methods = df['method'].unique()
metrics = ['human_likeness', 'smoothness', 'semantic_accuracy']
metric_names = {
    'human_likeness': 'Human-likeness',
    'smoothness': 'Speech-appropriateness',
    'semantic_accuracy': 'Style-accuracy'
}
colors = ['#4E79A7', '#A0CBE8', '#59A14F']

x = np.arange(len(methods))  # 每个方法的起始位置
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))

# 绘图
for i, metric in enumerate(metrics):
    subset = df[df['metric'] == metric]
    means = subset['final_mean'].values
    stds = subset['final_std'].values-0.6

    bars = ax.bar(x + i*width, means, width, yerr=stds, capsize=4,
                  label=metric_names[metric], color=colors[i], edgecolor='white')

    # 添加文本到误差棒顶部
    for j, bar in enumerate(bars):
        mean = means[j]
        std = stds[j]
        ax.text(bar.get_x() + bar.get_width()/2, mean + std + 0.05,
                f'{mean:.2f}', ha='center', va='bottom', fontsize=15,color='black',fontweight='normal' )

# 坐标轴设置
# ax.set_ylabel('Average Score', fontsize=12)
ax.set_ylim(0, 5)
ax.set_xticks(x + width)
ax.set_xticklabels(methods, fontsize=17, fontweight='normal') # 显式指定
# ax.set_title('Average Score per Method and Metric', fontsize=14)
# ax.legend(fontsize=15)
# 修改 ax.legend 部分
ax.legend(fontsize=15, prop={'family': 'SimSun', 'size': 15, 'weight': 'normal'})
ax.grid(True, axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("method_metric_barplot.png", dpi=300)
plt.show()
