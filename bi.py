import time
from random import random

import pandas as pd

from IntelligentAnalysis.qw import chat

from bilibili import demo_for_GUI
import gradio as gr
from IntelligentAnalysis.get_video import get_xhs_video
from IntelligentAnalysis.speech import stt, extract_for_gallery
from bili_video import get_video
from ImageGeneration.xhs_image import get_xhs_pictures
from ImageGeneration.websockets_api_example import run
import plotly.express as px

# 自定义CSS样式（冬天主题）
css = """
#winter_button {
    background-color: #4C9FF0;  /* 冰雪蓝色 */
    color: white;
    border: none;
    border-radius: 25px;  /* 圆角按钮 */
    padding: 15px 30px;
    font-size: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    font-family: 'Arial', sans-serif;
}

#winter_button:hover {
    background-color: #8BB9F7;  /* 鼠标悬浮时变成浅蓝色 */
    box-shadow: 0 8px 16px rgba(173, 216, 230, 0.5);  /* 冰雪般的发光效果 */
    transform: scale(1.05);  /* 鼠标悬浮时稍微放大按钮 */
}

body {
    background-color: #E0F7FA;  /* 清新的冰雪背景 */
    color: #1C4D77;  /* 深蓝色文本 */
}

#gradio-container {
    border: 5px solid #FFB6C1;
    border-radius: 25px;
    padding: 15px 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}    
#style {
   width: 2500px;
   height: 150px;
}  

"""
# df_list = pd.read_excel(r'D:\数据自动化与可视化实战\up_投稿数据_p.xlsx')
# df_list = df_list[['视频标题', '播放数', '评论数']]
# df_list = df_list.melt(id_vars=['视频标题'], var_name='视频指标', value_name='指标数值')
# 初始下拉列表选项
initial_options = ["初始视频标题"]
# 生成不同颜色的函数

# 定义回调函数，根据用户输入更新下拉列表
def update_dropdown(mid2):
    if mid2:
        # 这里简单示例，根据输入文本筛选选项
        new_options = demo_for_GUI(mid2)
        new_options = new_options['title']
    else:
        new_options = initial_options
    return gr.Dropdown(choices=list(new_options))
def filter_title(title, mid2):
    new_df = demo_for_GUI(mid2)
    new = pd.DataFrame()
    for i in title:
        temp = new_df[new_df['title'] == i]
        # pd.concat参数为列表类型
        new = pd.concat([new, temp])
    new_df = new[['title', 'play', 'comment']]
    # print(new_df)
    # new_df = new_df.rename(columns={'title' : '视频标题', 'play' : '播放量', 'comment' : '评论数'}, inplace=True)
    # print(new_df)
    return new_df


def respond(message, chat_history, mid):
    if '投稿数据' in message:
        # 首先将获取到的DataFrame转换为字符串类型再输给大语言模型
        data = demo_for_GUI(mid).to_string(index=False)
        message = f'请帮助分析up主投稿数据，并给出具体的建议，up主投稿数据数据如下：{data}'
    chat_history.append({"role": "user", "content": message})
    bot_message = chat(chat_history)
    chat_history.append({"role": "assistant", "content": bot_message})
    return "", chat_history

with gr.Blocks(css=css) as demo:
    gr.Image(r'C:\Users\20215\Pictures\B站横幅图.png', show_download_button=False, show_label=False)
    with gr.Row():
        with gr.Column():
            # 标题
            gr.Markdown("""
                                    # 爬取UP投稿数据🐍
                                    """)
            mid1 = gr.Textbox(label='请输入UP主的mid')
            btn1 = gr.Button(value='获取我的投稿数据', elem_id="winter_button")
            df1 = gr.DataFrame()
            gr.Image(r'C:\Users\20215\Pictures\哆啦A梦.jpg', show_download_button=False, show_label=False)

        with gr.Column():
            gr.Markdown("""
                        # 稿件数据柱形图📊
                        """)
            mid2 = gr.Textbox(label='请输入UP主的mid并点击下方按钮以获取视频,例如291245814',  elem_id='gradio-container')
            btn2 = gr.Button(value='获取我的投稿数据', elem_id="winter_button")
            # dropdown = gr.Dropdown(choices=initial_options,label="请选择视频标题🔖", interactive=True)
            # 使用多选框
            dropdown = gr.CheckboxGroup(choices=initial_options,label="请选择视频标题🔖", interactive=True)
            with gr.Row():
                with gr.Column():
                    bar_plot1 = gr.BarPlot(
                        x="title",  # x 轴对应的列名
                        y="play",  # y 轴对应的列名
                        color="play",
                        tooltip=["title", "play"]  # 鼠标悬停时显示的信息
                    )
                with gr.Column():
                    bar_plot2 = gr.BarPlot(
                        x="title",  # x 轴对应的列名
                        y="comment",  # y 轴对应的列名
                        color="comment",
                        tooltip=["title", "comment"]  # 鼠标悬停时显示的信息
                    )
            dropdown.change(fn=filter_title, inputs=[dropdown, mid2], outputs=[bar_plot1])
            dropdown.change(fn=filter_title, inputs=[dropdown, mid2], outputs=[bar_plot2])
    # 定义AI接口
    # 标题
    gr.Markdown("""
                                           # AI视频分析🎞️
                                           """)
    with gr.Row():
        with gr.Column():
            video = gr.Video(height=450, width=550, elem_id='gradio-container')
            video_bvid = gr.Textbox(label='请输入视频bvid，例如BV1hZc5eWEGV🎄', elem_id='gradio-container')
            video_btn = gr.Button(value='点击获取视频', elem_id="winter_button")
            video_btn.click(fn=get_video, inputs=video_bvid, outputs=video)

            text = gr.Textbox(label='语音识别内容🍩', elem_id='gradio-container')
            sentence_info = gr.Textbox(label='每句话对应的时间起始与结束', visible=False)
            stt_btn = gr.Button(value='语音识别', elem_id="winter_button")
            stt_btn.click(stt, video, [text, sentence_info])
        with gr.Column():
            img_btn = gr.Button(value='点击获取视频内容和对应文字', elem_id="winter_button")
            img = gr.Gallery(columns=[4], elem_id='gradio-container')
            img_btn.click(extract_for_gallery, [video, sentence_info], img)
            gr.Image(r'D:\数据自动化与可视化实战\项目二\output.jpg', show_download_button=False, show_label=False)
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
                            # AI数据分析🪼
                            """)
            chatbot = gr.Chatbot(type="messages", label='🎡', elem_id='gradio-container')
            msg = gr.Textbox(label='请输入您想问的问题，并回车。例如：帮我分析投稿数据(已确保输入了mid哦🍭)', elem_id='gradio-container')
            clear = gr.ClearButton([msg, chatbot], value="清除聊天", elem_id="winter_button")
            msg.submit(respond, [msg, chatbot, mid1], [msg, chatbot])
            gr.Image(r'C:\Users\20215\Pictures\star.gif', show_download_button=False, show_label=False)
        with gr.Column():
            gr.Markdown("""
                            # AI绘图🌌
                            """)
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        xhs_url = gr.Textbox(label='请输入小红书笔记链接吧📕', elem_id='gradio-container')
                        img_path = gr.Textbox(label='笔记存放位置🔅', visible=False)
                        img_btn = gr.Button(value='获取笔记图片', elem_id="winter_button")
                        # 注意：Gallery的入参需要列表类型
                        img_gallery = gr.Gallery(elem_id='gradio-container')
                        img_btn.click(fn=get_xhs_pictures, inputs=xhs_url, outputs=[img_path, img_gallery])
                with gr.Column():
                    num = gr.Textbox(label='请输入每张图片期待生成的图片数量💗', elem_id='gradio-container')
                    ai_btn = gr.Button(value='AI绘图', elem_id="winter_button")
                    output_gallery = gr.Gallery(elem_id='gradio-container')
                    ai_btn.click(fn=run, inputs=[img_path, num], outputs=output_gallery)

    btn1.click(demo_for_GUI, mid1, df1)
    # 绑定文本输入框的 change 事件到回调函数
    btn2.click(
        fn=update_dropdown,
        inputs=mid2,
        outputs=dropdown
    )

if __name__=="__main__":
    demo.launch(share=True, allowed_paths=[r'D:\comfUI\ComfyUI-aki-v1.6\ComfyUI\output'])