import gradio as gr
from get_video import get_xhs_video
from speech import stt, extract_for_gallery
from speech import extract_frame
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            video = gr.Video(height=450, width=450)
            video_url = gr.Textbox(label='请输入视频链接')
            video_btn = gr.Button(value='点击获取视频')
            video_btn.click(fn=get_xhs_video, inputs=video_url, outputs=video)

            text = gr.Textbox(label='语音识别内容')
            sentence_info = gr.Textbox(label='每句话对应的时间起始与结束', visible=False)
            stt_btn = gr.Button(value='语音识别')
            stt_btn.click(stt, video, [text, sentence_info])
        with gr.Column():
            img_btn = gr.Button(value='点击获取视频内容和对应文字')
            img = gr.Gallery(columns=[4])
            img_btn.click(extract_for_gallery, [video, sentence_info], img)



if __name__=="__main__":
    demo.launch()