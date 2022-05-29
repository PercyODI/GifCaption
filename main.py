from PIL import GifImagePlugin, Image, ImageDraw, ImageFont
from pathlib import Path
import requests
import io

# Setup settings and fonts
font = ImageFont.truetype('assets/font/impact.ttf', 55)
GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

# Get the GIF from the user
print("GIF URL: ", end="")
gif_url = input()

response = requests.get(gif_url)

# Get the text from the user
print("Text to write: ", end="")
text = input()

images = []
durations = []
with Image.open(io.BytesIO(response.content)) as im:
    next_frame = 0
    try:
        while 1:
            im.seek(next_frame)
            new_im = Image.frombytes(im.mode, im.size, im.tobytes())
            
            draw = ImageDraw.Draw(new_im)
            draw.text((im.size[0] / 2, im.size[1] * 0.95), text, align='center', anchor='mb', font=font, fill="white", stroke_width=4, stroke_fill="black")

            images.append(new_im)
            durations.append(im.info['duration'])
            
            next_frame = next_frame + 1
    except EOFError:
        pass

Path("./data/dst").mkdir(parents=True, exist_ok=True)
images[0].save('./data/dst/output.gif', save_all=True, append_images=images[1:], duration=durations, loop=0)

print("Done.")