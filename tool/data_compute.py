import os
import json
import pandas as pd

# 方法顺序
methods = ["emage", "gesturelsm", "zeroeggs", "diffuseStyle", "ours"]
metrics = ["human_likeness", "smoothness", "semantic_accuracy"]

# 存储所有记录
records = []

def process_file(file_path, filename):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"[跳过] 无效 JSON: {file_path}")
            return

    for metric in metrics:
        values = data.get(metric, [])
        if len(values) != 10:
            print(f"[跳过] {metric} 不满足 10 项评分: {file_path}")
            return

        # 拆分为每组5个方法，记录每个方法对应的评分
        for i in range(5):  # 第一组
            records.append({
                "file": filename,
                "group": 1,
                "method": methods[i],
                "metric": metric,
                "score": values[i]
            })
        for i in range(5):  # 第二组
            records.append({
                "file": filename,
                "group": 2,
                "method": methods[i],
                "metric": metric,
                "score": values[i + 5]
            })

if __name__ == '__main__':
    folder_path = r'C:\Users\12551\Desktop\src_1\result\ablation'  # 修改为你的实际路径

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            full_path = os.path.join(folder_path, filename)
            process_file(full_path, filename)

    df = pd.DataFrame(records)
    df = df[["file", "group", "method", "metric", "score"]]  # 排序列
    df.to_excel("all_scores_raw.xlsx", index=False)
    print("✅ 所有评分已提取并保存为 all_scores_raw.xlsx")
