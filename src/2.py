import os
import json
import pandas as pd

# 固定的方法顺序
methods = ["emage", "gesturelsm", "zeroeggs", "diffuseStyle", "ours"]
metrics = ['human_likeness', 'smoothness', 'semantic_accuracy']

# 存储所有记录
rows = []

# 设置你的 .txt 文件夹路径
folder = "result/ablation"  # 修改为你自己的文件夹路径

for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        continue
    
    filepath = os.path.join(folder, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except:
            print(f"[!] 解析失败，跳过文件：{filename}")
            continue

    groups = data.get("assigned_groups", [])
    if len(groups) != 2:
        print(f"[!] 组号数量不是两个，跳过文件：{filename}")
        continue

    for metric in metrics:
        scores = data.get(metric, [])
        if len(scores) != 10:
            print(f"[!] 指标 {metric} 长度不为10，跳过文件：{filename}")
            continue
        
        # 前 5 个分数 -> 第一个组，第 6~10 个分数 -> 第二个组
        for i in range(10):
            group_index = 0 if i < 5 else 1
            group_id = groups[group_index]
            method = methods[i % 5]
            score = scores[i]
            rows.append({
                "group": group_id,
                "method": method,
                "metric": metric,
                "score": score
            })

# 保存为 DataFrame 并导出为 Excel
df = pd.DataFrame(rows)
df.to_excel("long_format_scores.xlsx", index=False)
print("[✓] 数据已保存为 long_format_scores.xlsx")
