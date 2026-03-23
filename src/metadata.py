# 建议新建一个 metadata.py 或直接写在主脚本顶部
METADATA = {
    # 实验一：10个 (无文本需求)
    "1_wayne_0_1_1_exp3_clip3": {"text": "", "cat": "humanity"},
    "1_wayne_0_5_5_exp3_clip3": {"text": "", "cat": "humanity"},
    "1_wayne_0_5_5_exp3_clip6": {"text": "", "cat": "humanity"},
    "20_li_0_81_81_exp3_clip1": {"text": "", "cat": "humanity"},
    "20_li_0_81_81_exp3_clip4": {"text": "", "cat": "humanity"},
    "27_yingqing_0_95_95_exp3_clip1": {"text": "", "cat": "humanity"},
    "2_scott_0_65_65_exp3_clip6": {"text": "", "cat": "humanity"},
    "30_katya_0_103_103_exp3_clip1": {"text": "", "cat": "humanity"},
    "30_katya_0_103_103_exp3_clip5": {"text": "", "cat": "humanity"},
    "5_stewart_0_8_8_exp3_clip4": {"text": "", "cat": "humanity"},

   # 实验二：9个 (分三类，需展示文本)
    "10_kieks_0_111_111_clip1": {
        "text": "Now mobile phones have become very close to everyone, and some people can't live without them. I appreciate the technology, but we should have based [it] on basic [ethics].", 
        "cat": "contrast"
    },

    "11_nidal_0_103_103_clip1": {
        "text": "And I was in the university almost more than 10 years ago. That community security was not very good, and was often more than not in a dangerous situation. One time, I was walking home from work, waiting at the bus stop for a bus; then, I heard the sound of a gunfire from across the road.", 
        "cat": "contrast"
    },

    "2_scott_0_5_5_clip1": {
        "text": "...handle these problems by myself. Even though this improves my independent ability, I still miss my mom and her rules. But most importantly...", 
        "cat": "contrast"
    },
    
    # ===================

    "18_daiki_0_2_2_clip1": {
        "text": "These books can—and give me—the motivation to be healthier than in 'dusty'. And the last things I like to do when I'm free is eat out with my family members.", 
        "cat": "causality"
    },

    "1_wayne_0_103_103_clip1": {
        "text": "...across the street, I was so scared. The main reason was because you've got no, no place to hide. You're at a bus station; there's no place to go.", 
        "cat": "causality"
    },

    "1_wayne_0_103_103_clip2": {
        "text": "They shook the car and [swore] at me. I thought to myself, 'This is horrible,' because a few days ago someone was shot dead. Maybe I'll be [next]...", 
        "cat": "contrast"
    },

     # ===================

    "4_lawrence_0_111_111_clip1": {
        "text": "Some people hitting stones, pelting... what are some people? Pelting stones at dogs and watching them yelp in pain, amused. Some little children begging on the street.", 
        "cat": "sequence"
    },
    
    "4_lawrence_0_2_2_clip1": {
        "text": "I'll actually give each restaurant a score based on how good the food is, how good the environment is, and at the same time, I will write down each type of food they serve.", 
        "cat": "sequence"
    },

    "4_lawrence_0_3_3_clip1": {
        "text": "For example, people being shifted from the center of the frame to the left side of the frame can make a different feeling when seen in context with the background.", 
        "cat": "sequence"
    },

    # 实验三：10个 (长尾语义，需展示文本)
    "30_katya_0_95_95_exp3_clip1": {
        "text": "Well, the world is so small, actually. Last year, I was visiting a client during my work time on the way back around...", 
        "cat": "long-tail"
    },

    "30_katya_0_95_95_exp3_clip3": {
        "text": "It's been three or four years since we've seen each other, right? We are very happy to meet together after not seeing...", 
        "cat": "long-tail"
    },

    "11_nidal_0_5_5_exp3_clip10": {
        "text": "Even though this improved my independence abilities, I still miss my mom and her rules. But most importantly...", 
        "cat": "long-tail"
    },

    "11_nidal_0_5_5_exp3_clip11": {
        "text": "But most importantly, I now understand how much my mom had helped me, and all her struggles in the process.", 
        "cat": "long-tail"
    },

    "28_tiffnay_0_95_95_exp3_clip5": {
        "text": "We went to a cafe to sit. While we were eating and drinking, he told me that he is now working at a middle school as an English teacher. Oh, you found your dream job!", 
        "cat": "long-tail"
    },

    "28_tiffnay_0_95_95_exp3_clip6": {
        "text": "Oh, you found your dream job! I remember you wanted to be an English teacher when you were in college. Overall, it was the time when I [was in] Italy and, surprisingly...", 
        "cat": "long-tail"
    },
    
    "6_carla_0_95_95_exp3_clip3": {
        "text": "...seen each other, right? We were very happy to meet together after not seeing each other for such a long time. We gave each other a warm hug and decided to spend some time together.", 
        "cat": "long-tail"
    },

    "6_carla_0_95_95_exp3_clip4": {
        "text": "We went to a cafe to sit. While we were eating and drinking, he told me he is now working at a middle school as an English teacher. Oh, you found your dream job! I remember you wanted to...", 
        "cat": "long-tail"
    },

    "12_zhao_0_103_103_exp3_clip1": {
        "text": "When I was in university, almost more than 10 years ago, maybe the community security was not very good.", 
        "cat": "long-tail"
    },

    "12_zhao_0_103_103_exp3_clip2": {
        "text": "...was not very good, so we were often—more often than not—in dangerous situations. One time, I was walking home from work, or waiting at the bus stop for [the] bus.", 
        "cat": "long-tail"
    },

}