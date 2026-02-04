import gradio as gr
import pandas as pd

df = pd.read_excel()
title_list = list(df['视频标题'].unique())

def filter_title(title):
    new_df = df[['视频标题'] == title]
    return new_df
def gen_mp4_path(title):
    path = rf'./视频存储/{title}.mp4'
    return path
with gr.Blocks() as demo:
    text = gr.Textbox()
    video = gr.Video()
    dropdown = gr.Dropdown(title_list, interactive=True)
    plot = gr.LinePlot(value=df, x='秒数', y='点击指数')
    plot2 = gr.LinePlot(value=df, x='秒数', y='流失指数')
    dropdown.change(fn=filter_title, inputs=dropdown, outputs=plot)
    dropdown.change(fn=filter_title, inputs=dropdown, outputs=plot2)
    dropdown.change(fn=gen_mp4_path(), inputs=dropdown, outputs=video)




if __name__ == "__main__":
    demo.launch()