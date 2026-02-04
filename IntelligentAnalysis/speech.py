import os.path
import re
from funasr import AutoModel
from pprint import pprint

# paraformer-zh is a multi-functional asr model
# use vad, punc, spk or not as you need
from moviepy import VideoFileClip


def stt(mp4):
    model = AutoModel(model="paraformer-zh", model_revision="v2.0.4",
                      vad_model="fsmn-vad", vad_model_revision="v2.0.4",
                      punc_model="ct-punc-c", punc_model_revision="v2.0.4",

                      )
    res = model.generate(input=mp4,
                batch_size_s=300,
                hotword='魔搭')
    pprint(res)
    text = res[0]['text']
    text = re.sub(r'([？。])', r'\1\n\n', text)
    return text, res[0]['sentence_info']
def extract_frame(video_path, time_in_seconds, output_image_path):
    # 加载视频文件
    clip = VideoFileClip(video_path)

    # 提取指定时间点的帧
    frame = clip.get_frame(time_in_seconds)

    # 保存帧为图片
    clip.save_frame(output_image_path, t=time_in_seconds)

    # 关闭视频文件
    clip.close()
def extract_for_gallery(video_path, sentence_info):
    file_name = os.path.basename(video_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    output_path = rf'./图片存储/{file_name_without_extension}'
    # 还原sentence_info的格式
    sentence_info = eval(sentence_info)
    list_for_gallery = []
    for sentence in sentence_info:
        text = sentence['text']
        start = sentence['start']
        end = sentence['end']
        time_in_seconds = (start + end) / 2 / 1000
        save_name = output_path + f'{time_in_seconds}.png'
        extract_frame(video_path, time_in_seconds, save_name)
        list_for_gallery.append((save_name, text))
    return list_for_gallery

if __name__ == "__main__":
    # stt()
    # 示例使用
    video_path = r"D:\数据自动化与可视化实战\项目二\视频存储\唯有牡丹真国色.mp4"  # 输入视频文件路径
    time_in_seconds = 10  # 提取第10秒的帧
    output_image_path = "output_frame.png"  # 输出图片路径
    extract_frame(video_path, time_in_seconds, output_image_path)
    print(f"帧已保存为 {output_image_path}")






