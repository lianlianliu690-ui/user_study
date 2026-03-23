from moviepy.editor import VideoFileClip
import os

def crop_left_half(input_path, output_path=None):
    # 加载视频
    clip = VideoFileClip(input_path)
    
    # 获取原始尺寸
    w, h = clip.size
    
    # 裁剪左半边
    cropped = clip.crop(x1=0, y1=0, x2=w//2, y2=h)
    
    # 自动生成输出路径
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_left{ext}"
    
    # 保存新视频
    cropped.write_videofile(output_path, codec="libx264", audio_codec="aac")

# 示例使用
if __name__ == "__main__":
    input_video = r"C:\Users\12551\Desktop\user_study\video\ours\5_stewart_0_3_3\ours_30_40.mp4"  # 替换为你的视频路径
    crop_left_half(input_video)
