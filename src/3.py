import pandas as pd
import numpy as np

# 读取打分数据（你提供的那种长表结构）
df = pd.read_excel('long_format_scores.xlsx')  # 替换为你的文件路径

# Step 1: 针对每个 group+method+metric 聚合
grouped = df.groupby(['group', 'method', 'metric'])['score'].agg(['mean', 'std']).reset_index()
grouped.rename(columns={'mean': 'group_mean', 'std': 'group_std'}, inplace=True)

# Step 2: 针对每个 method+metric 进行最终统计
final_stats = grouped.groupby(['method', 'metric'])['group_mean'].agg(['mean', 'std']).reset_index()
final_stats.rename(columns={'mean': 'final_mean', 'std': 'final_std'}, inplace=True)

# 查看结果
print(final_stats)

# 可选：导出到 Excel
final_stats.to_excel('final_method_metric_stats.xlsx', index=False)
