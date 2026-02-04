# This is an example that uses the websockets api to know when a prompt execution is done
# Once the prompt execution is done it downloads the images using the /history endpoint
import os.path

import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
from random import randint

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())


def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    print(data)
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()


def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break  # Execution is done
        else:
            # If you want to be able to decode the binary stream for latent previews, here is how you can do it:
            # bytesIO = BytesIO(out[8:])
            # preview_image = Image.open(bytesIO) # This is your preview in PIL image format, store it in a global
            continue  # previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        images_output = []
        if 'images' in node_output:
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
        output_images[node_id] = images_output

    return output_images, 'D:\comfUI\ComfyUI-aki-v1.6\ComfyUI\output\\' + image['filename']


prompt_text = {
  "3": {
    "inputs": {
      "seed": 143806043404000,
      "steps": 20,
      "cfg": 8,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 0.91,
      "model": [
        "26",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "17",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "K采样器"
    }
  },
  "6": {
    "inputs": {
      "text": [
        "24",
        0
      ],
      "clip": [
        "26",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码器"
    }
  },
  "7": {
    "inputs": {
      "text": "text, watermark",
      "clip": [
        "26",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码器"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "26",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE解码"
    }
  },
  "11": {
    "inputs": {
      "image": "2025.jpg",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "加载图像"
    }
  },
  "12": {
    "inputs": {
      "text": [
        "24",
        0
      ],
      "text2": " The image is a graphic illustration, likely designed to celebrate the Chinese New Year. It features two animated characters, one on each side, with the character on the right resembling Hello Kitty, a popular anime-style cartoon character, and the character on the left looking like Kurochii, also known as Marui, from the same franchise, depicted in a similar cute style. They are surrounded by a festive scene including Chinese lanterns, banners with what appears to be Chinese characters, and Japanese oranges (tangerines) known as \"yuzu\" in Japan. There is a cake on the right decorated with more characters and symbols that could be related to Hello Kitty's world or the Chinese New Year. The background is pink with Japanese cherry blossom motifs.\n\nThe date \"2016年1月8日\" (January 8, 2016) is prominently displayed in the top left corner, suggesting that this image was created to commemorate a special occasion or event within that year. The overall design of the image combines elements from both Japanese and Chinese cultures, indicating a celebration that brings these two worlds together. "
    },
    "class_type": "ShowText|pysssss",
    "_meta": {
      "title": "展示文本"
    }
  },
  "17": {
    "inputs": {
      "pixels": [
        "19",
        0
      ],
      "vae": [
        "26",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE编码"
    }
  },
  "19": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "scale_by": 0.6,
      "image": [
        "11",
        0
      ]
    },
    "class_type": "ImageScaleBy",
    "_meta": {
      "title": "图像按系数缩放"
    }
  },
  "23": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  },
  "24": {
    "inputs": {
      "query": "briefly describe the image",
      "debug": "enable",
      "url": "http://127.0.0.1:11434",
      "model": "llava:7b",
      "keep_alive": 0,
      "format": "text",
      "seed": 1312620951,
      "images": [
        "11",
        0
      ]
    },
    "class_type": "OllamaVision",
    "_meta": {
      "title": "Ollama Vision"
    }
  },
  "26": {
    "inputs": {
      "ckpt_name": "pixelArtDiffusionXL_spriteShaper.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Checkpoint加载器(简易)"
    }
  }
}


# prompt = json.loads(prompt_text)
# #set the text prompt for our positive CLIPTextEncode
# set the seed for our KSampler node

def run(path, num):
    img_list = [path + '\\' + filename for filename in os.listdir(path)]
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    img_path_list = []
    for img in img_list:
        prompt_text['11']['inputs']['image'] = img
        for _ in range(int(num)):
            prompt_text['24']['inputs']['seed'] = randint(1, 88888888)
            prompt_text["3"]["inputs"]["seed"] = randint(1, 88888888)
            images, img_path = get_images(ws, prompt_text)
            img_path_list.append(img_path)
            # 返回结果之后，函数依然运行
            yield img_path_list
    ws.close()

# for in case this example is used in an environment where it will be repeatedly called, like in a Gradio app. otherwise, you'll randomly receive connection timeouts
# Commented out code to display the output images:

# for node_id in images:
#     for image_data in images[node_id]:
#         from PIL import Image
#         import io
#         image = Image.open(io.BytesIO(image_data))
#         image.show()


