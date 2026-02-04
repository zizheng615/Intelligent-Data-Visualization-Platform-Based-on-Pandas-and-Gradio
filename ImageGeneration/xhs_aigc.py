import gradio as gr
from xhs_image import  get_xhs_pictures
from websockets_api_example import run


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            with gr.Row():
                xhs_url = gr.Textbox(label='请输入笔记链接吧🍧')
                img_path = gr.Textbox(label='笔记存放位置🔅', visible=False)
                img_btn = gr.Button(value='获取笔记图片')
                # 注意：Gallery的入参需要列表类型
                img_gallery = gr.Gallery()
                img_btn.click(fn=get_xhs_pictures, inputs=xhs_url, outputs=[img_path, img_gallery])
        with gr.Column():
            num = gr.Textbox(label='请输入期待生成图片的数量💗')
            ai_btn = gr.Button(value='AI绘图')
            output_gallery = gr.Gallery()
            ai_btn.click(fn=run, inputs=[img_path, num], outputs=output_gallery)
# allowed_paths 表示配置白名单
demo.launch(allowed_paths=[r'D:\comfUI\ComfyUI-aki-v1.6\ComfyUI\output'])