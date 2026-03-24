import streamlit as st
import random
import os
import json
import time
import smtplib
import poplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.parser import Parser

# 从你的本地文件导入元数据
try:
    from metadata import METADATA
except ImportError:
    st.error("❌ 无法找到 metadata.py，请确保该文件在当前目录下。")
    st.stop()

# --- 1. 全局配置 ---
# --- 1. 全局配置 (修改后) ---
# 建议使用 st.secrets 获取，如果获取不到则报错提示
try:
    MY_EMAIL = st.secrets["email_user"]
    MY_PASSWORD = st.secrets["email_password"]
    DATASET_NAME = st.secrets.get("dataset_name", "rlgesture_Study") 
except KeyError:
    st.error("❌ 未找到 Secrets 配置，请在 Streamlit Cloud 仪表盘设置。")
    st.stop()



METHODS = ["ours", "raggesture", "gesturelsm", "emage"]
TOTAL_SAMPLES_NEEDED = 60                 # 目标收集样本数

# 实验二分类预处理
EXP2_SUB_CATS = {"contrast": [], "causality": [], "sequence": []}
for vid, info in METADATA.items():
    if info['cat'] in EXP2_SUB_CATS:
        EXP2_SUB_CATS[info['cat']].append(vid)

# --- 2. 邮件统计辅助函数 ---

@st.cache_data(ttl=60)
def get_submission_count():
    """通过读取邮箱中特定主题的邮件数量来统计已提交人数"""
    try:
        server = poplib.POP3_SSL('pop.126.com', 995)
        server.user(MY_EMAIL)
        server.pass_(MY_PASSWORD)
        
        # 获取邮件列表
        resp, mails, octets = server.list()
        msg_count = len(mails)
        
        count = 0
        subject_to_find = f"{DATASET_NAME} Number of submissions"
        
        # 从最新邮件开始往前找
        for i in range(msg_count, 0, -1):
            resp, lines, octets = server.retr(i)
            msg_content = b'\n'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            if msg['Subject'] == subject_to_find:
                # 假设正文里只存了一个数字
                payload = msg.get_payload(decode=True).decode('utf-8').strip()
                count = int(payload)
                break
        server.quit()
        return count
    except Exception as e:
        print(f"读取人数失败: {e}")
        return 0

def update_submission_count(new_count):
    """发送一封纯数字邮件，标记当前的提交总数"""
    msg = MIMEText(str(new_count))
    msg['Subject'] = f"{DATASET_NAME} Number of submissions"
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL
    try:
        smtp = smtplib.SMTP('smtp.126.com')
        smtp.login(MY_EMAIL, MY_PASSWORD)
        smtp.sendmail(MY_EMAIL, MY_EMAIL, msg.as_string())
        smtp.quit()
    except Exception as e:
        print(f"更新人数失败: {e}")

# --- 3. 核心逻辑函数 ---

def get_balanced_tasks():
    """
    核心修改：每人只看 3 组样本
    Exp 1 (1 组) + Exp 2 (1 组) + Exp 3 (1 组)
    """
    # Exp 1: 从 humanity 类别中随机抽 1 组
    exp1_all = [k for k, v in METADATA.items() if v['cat'] == "humanity"]
    tasks1 = random.sample(exp1_all, 1) if exp1_all else []
    
    # Exp 2: 从三个子类(contrast, causality, sequence)中整体随机抽 1 组
    # 或者如果你想更随机，直接从所有 Exp2 样本里抽 1 组
    exp2_all = []
    for cat_list in EXP2_SUB_CATS.values():
        exp2_all.extend(cat_list)
    tasks2 = random.sample(exp2_all, 1) if exp2_all else []
    
    # Exp 3: 从 long-tail 类别中随机抽 1 组
    exp3_all = [k for k, v in METADATA.items() if v['cat'] == "long-tail"]
    tasks3 = random.sample(exp3_all, 1) if exp3_all else []
    
    # 返回总计 3 组样本 ID
    return tasks1 + tasks2 + tasks3

def data_collection(results_dict, count):
    """保存结果并发送附件邮件"""
    content_dict = {
        "user_id": count,
        "assigned_tasks": st.session_state.get("tasks", []),
        "method_order": {k: st.session_state.get(f"order_{k}") for k in results_dict.keys()},
        "results": results_dict
    }
    
    string = json.dumps(content_dict, ensure_ascii=False, indent=2)
    localtime_obj = datetime.now() + timedelta(hours=8)
    localtime_str = localtime_obj.strftime('%m-%d %H-%M-%S')
    ID = f"{count}-{localtime_obj.strftime('%S')}"
    file_name = f"{DATASET_NAME}_{count}_{localtime_str}.txt"
    
    # 本地备份
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(string)

    # 邮件附件
    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL
    msg['Subject'] = f"{DATASET_NAME} Result: ID {ID}"
    msg.attach(MIMEText(string))
    
    with open(file_name, 'rb') as f:
        part = MIMEApplication(f.read(), Name=file_name)
        part['Content-Disposition'] = f'attachment; filename="{file_name}"'
        msg.attach(part)

    smtp = smtplib.SMTP('smtp.126.com')
    smtp.login(MY_EMAIL, MY_PASSWORD)
    smtp.sendmail(MY_EMAIL, MY_EMAIL, msg.as_string())
    smtp.quit()
    
    return ID, localtime_str

# --- 4. UI 组件 ---

# --- 2. UI 组件：垂直排列展示视频 ---
def render_comparison_row(sample_id, step_idx):
    info = METADATA.get(sample_id, {"text": "", "cat": ""})
    
    # A. 顶部引导语与文本展示 (修改后)
    if info['cat'] == "humanity":
        st.subheader("实验一：运动自然度和音频一致性评分")
        st.info("""
        💡 **评价重点：**
        1. **物理真实性**：请观察视频中虚拟角色的运动，并判断其是否符合人类的真实行为习惯（请忽略面部表情）。
        2. **韵律契合度**：动作的起伏、停顿与力度，是否与语音的**节奏、重音及语气变化**高度一致。
        
        ⚠️ **注意**：本组实验旨在考察模型的基础生成能力，**不提供文本对照**，请凭直觉感知音画配合度。  
        📌 **技术说明**：部分视频中脚步可能存在轻微漂移现象，此为模型生成的正常现象，**请重点关注肢体动作的质量与节奏**。
        """)
    elif info['cat'] in EXP2_SUB_CATS:
        st.subheader("实验二：逻辑衔接与话语态势评分")
        st.warning(f"💬 **语音文本：** {info['text']}")
        st.info("""
        🔍 **评价重点：**
        1. **逻辑转折点**：观察在出现“但是(BUT)”、“因为(BECAUSE)”、“所以(SO)”等词汇时，动作是否有明显的**幅度改变或方向切换**。
        2. **隐式衔接**：即使没有显式逻辑词，在语意发生因果或并列转折处，数字人的姿态（Pose）是否做出了相应的引导或强调。
        
        ⚠️ **评价建议**：请先通读上方文本理解逻辑，再观察视频中动作的“起承转合”是否自然衔接。  
        📌 **技术说明**：部分视频中脚步可能存在轻微漂移现象，此为模型生成的正常现象，**请重点关注运动动作的逻辑衔接**。
        """)
    else:
        st.subheader("实验三：特定语义与动作准确度评分")
        st.success(f"💬 **语音文本：** {info['text']}")
        st.info("""
        🔍 **评价重点：**
        1. **动作还原度**：重点观察肢体动作是否精准地“表现”了语音中的具体含义（如：指点、挥手、犹豫、惊恐等）。
        2. **语义生动性**：动作是否具有**高辨识度**，能否让人一眼看出在做什么，而非仅仅是随语调进行的机械摆动。
        
        ⚠️ **注意**：本组实验包含较多具有**明确含义**的关键词，请重点判断数字人是否捕捉到了这些特定词汇所蕴含的动作细节。  
        📌 **技术说明**：部分视频中脚步可能存在轻微漂移现象，此为模型生成的正常现象，**请重点关注动作与语义的匹配度**。
        """)

    st.write(f"📊 **总进度: {step_idx + 1} / 3**")
    st.divider()

    # B. 随机打乱方法顺序 (防止位置偏见)
    display_methods = METHODS.copy()
    if f"order_{sample_id}" not in st.session_state:
        random.shuffle(display_methods)
        st.session_state[f"order_{sample_id}"] = display_methods
    else:
        display_methods = st.session_state[f"order_{sample_id}"]

    scores = {}

    # C. 垂直循环渲染视频
    for i, m_name in enumerate(display_methods):
        # 使用容器美化每一组视频
        with st.container():
            # --- 新增提示语 ---
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; background-color: #f0f2f6; padding: 5px 15px; border-radius: 5px; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: #ff4b4b;">👈 左侧：候选方法 {chr(65+i)}</span>
                    <span style="font-weight: bold; color: #1f77b4;">右侧：地面真实运动 (Ground Truth) 👉</span>
                </div>
            """, unsafe_allow_html=True)
            # ----------------
            
            # 路径：video_rl/方法名/样本ID.mp4
            video_url = f"video_rl/{m_name}/{sample_id}.mp4" 
            
            if os.path.exists(video_url):
                # 调整视频宽度
                st.video(video_url) 
            else:
                st.error(f"文件未找到: {video_url}")
            
            # 定义两行文案：第一行加粗，第二行缩小并换行
            # 注意：第一行末尾有两个空格，这是 Markdown 换行的触发开关
            label_text = (
                f"请对 **方法 {chr(65+i)}** 进行打分 (1=差, 5=好)  \n"
                f":gray[（注意：右侧 GT 仅作为运动合理性的参考标准，而非追求动作轨迹的完全重合。）]"
            )

            scores[m_name] = st.radio(
                label=label_text,
                options=[1, 2, 3, 4, 5], 
                index=None, 
                key=f"score_{step_idx}_{i}",
                horizontal=True
            )
            st.write("") # 留白
            st.divider() # 方法之间的分割线

    return scores

# --- 6. 实验说明页组件 ---
def show_instructions():
    """第一页：详细的实验说明"""
    st.title("📑 实验参与指南")
    # 核心提醒：使用 error 样式或大号加粗红色字体
    st.error("⚠️ **重要提示：评价时请专注于身体动作（Body Motion），所有视频均请忽略面部表情（Facial Expressions）。**")
    st.markdown("""
    感谢您参加本次**语音驱动三维数字人运动生成质量评估**研究！请在开始实验前仔细阅读以下说明。
    
    ### 1. 实验目标
    本次实验旨在评估不同算法生成的数字人动作。您将观看 3 组视频，每组包含 4 个不同的生成结果。
    
    ### 2. 评价维度
    实验分为三个阶段，每个阶段的关注点有所不同：
    
    #### **🔹 阶段一：自然度与音画同步性**
    重点评估生成动作的**物理合理性**与**韵律契合度**。
    * **物理质量**：肢体运动是否顺滑自然（无怪异抖动、无反关节或穿模现象）。
    * **节奏对齐**：动作起伏与停顿，是否与语音的**重音、语速及语气节奏**高度一致。

    #### **🔸 阶段二：逻辑衔接性**
    考察模型对**转折、因果或者并列关系**的表达。
    * **操作建议**：请**先阅读语音转录文本**理解语义背景，随后观察视频。
    * **评价核心**：肢体动作与逻辑词（如：**但是、因为、而且**）是否契合？在逻辑转换处是否有明显的态势切换或强调性手势。

    #### **🟢 阶段三：语义生动性**
    评估动作对**长尾/复杂语义词汇**（如：拥抱、惊慌等）的捕捉能力。
    * **评价核心**：观察肢体动作是否精准地“还原”了语音的具体含义。
    * **辨识度判断**：动作是否具备**生动性**，而非仅仅是随语调进行的常规摆动。

    ### 3. 打分标准
    请根据您的直观感受，为每个视频打 **1-5 分**（1分代表非常糟糕，5分代表完美符合）。
    
    ---
    **⚠️ 注意事项：**
    1. 请尽量使用**电脑端浏览器**进行操作以获得最佳显示效果。
    2. 实验中途请勿刷新网页，否则进度将丢失。
    3. 最后一页请务必点击 **“提交最终结果”**。
    """)
    st.divider()
    if st.button("我已阅读并明白，开始实验 🚀", type="primary", use_container_width=True):
        st.session_state.study_started = True
        st.rerun()



# --- 5. 主页面流程 ---

def main():
    st.set_page_config(page_title="Gestural AI User Study", layout="centered")
    
    # 初始化“是否开始”的状态
    if "study_started" not in st.session_state:
        st.session_state.study_started = False

    # 如果没开始，显示说明页
    if not st.session_state.study_started:
        show_instructions()
        return # 结束当前运行，不往下执行实验逻辑

    # --- 以下是原有的实验逻辑 ---
    st.title("三维数字人生成质量评估研究")
    
    # 检查人数是否已满
    current_count = get_submission_count()
    if current_count >= TOTAL_SAMPLES_NEEDED:
        st.error("🙏 感谢关注！本实验样本收集已达上限。")
        st.stop()

    # 初始化任务
    if "tasks" not in st.session_state:
        st.session_state.tasks = get_balanced_tasks()
        st.session_state.current_step = 0
        st.session_state.results = {}

    step = st.session_state.current_step
    
    # 主实验界面
    if step < 3:
        sample_id = st.session_state.tasks[step]
        current_scores = render_comparison_row(sample_id, step)

        st.divider()
        c1, c2 = st.columns([1, 1])
        
        if c1.button("← 返回上一组") and step > 0:
            st.session_state.current_step -= 1
            st.rerun()

        # 修改：进入下一组或完成
        button_text = "确认并进入下一组 →" if step < 2 else "确认并查看结果摘要 →"
        if c2.button(button_text):
            if any(s is None for s in current_scores.values()):
                st.error("⚠️ 请确保完成本页所有候选方法的评分。")
            else:
                st.session_state.results[sample_id] = current_scores
                st.session_state.current_step += 1
                st.rerun()
                
    # 完成提交界面
    else:
        st.balloons()
        st.header("🏁 评分结果预览")
        st.write("请在提交前核对您的评分结果。如果需要修改，请点击下方的“重新开始”或刷新页面（注意：刷新将丢失所有进度）。")

        # --- 新增：结果汇总展示表 ---
        summary_data = []
        for step_idx, sample_id in enumerate(st.session_state.tasks):
            # 获取该样本的原始分数
            scores = st.session_state.results.get(sample_id, {})
            # 获取该样本展示时的随机顺序
            order = st.session_state.get(f"order_{sample_id}", METHODS)
            
            # 构造一行显示数据：将方法 ID 映射回受试者看到的“方法 A, B, C, D”
            row = {"阶段": f"实验 {step_idx + 1}"}
            for i, m_name in enumerate(order):
                row[f"方法 {chr(65+i)}"] = scores.get(m_name, "未打分")
            summary_data.append(row)

        # 使用 Streamlit 表格展示
        st.table(summary_data)
        st.divider()
        # --- 汇总展示结束 ---

        st.success("🎉 所有评分已核对无误！请点击下方按钮上传结果。")
        
        if "button_clicked" not in st.session_state:
            st.session_state.button_clicked = False

        if not st.session_state.button_clicked:
            if st.button("🚀 提交最终结果", type="primary", use_container_width=True):
                with st.spinner('正在同步数据到服务器，请勿关闭页面...'):
                    # 1. 重新获取计数并更新
                    count = get_submission_count() + 1
                    update_submission_count(count)

                    # 2. 发送详细数据
                    try:
                        ID, localtime = data_collection(
                            st.session_state.results, 
                            count
                        )
                        st.success("✅ 数据提交成功！")
                        st.session_state.button_clicked = True
                        st.session_state.final_id = ID
                        st.session_state.final_time = localtime
                        st.rerun()
                    except Exception as e:
                        st.error(f"提交失败: {e}")

        else:
            st.divider()
            st.markdown("### 📝 提交凭证")
            st.info(f"您的提交 ID: **{st.session_state.get('final_id')}**")
            st.info(f"提交时间: **{st.session_state.get('final_time')}**")
            st.write("请对本页面截图留存。再次感谢您的参与！")
            
            if st.button("退出系统"):
                st.cache_data.clear()
                st.session_state.clear()
                st.rerun()

if __name__ == "__main__":
    main()