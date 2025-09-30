from PIL import Image, ImageDraw, ImageFont

# Sample meme text and image
meme_text = "When you realize AI memes are funnier!"
img = Image.open("your_meme_image.jpg")
W, H = img.size

# --- Start with a large font ---
font_size = 180  # bigger starting size
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except:
    font = ImageFont.load_default()

draw = ImageDraw.Draw(img)
max_width = W - 40  # leave padding

# --- Reduce font size until it fits ---
bbox = draw.textbbox((0, 0), meme_text, font=font)
text_width = bbox[2] - bbox[0]
while text_width > max_width and font_size > 10:
    font_size -= 5
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), meme_text, font=font)
    text_width = bbox[2] - bbox[0]

# --- Create new image with space for text above ---
new_img = Image.new("RGB", (W, H + font_size + 40), "white")
draw = ImageDraw.Draw(new_img)

# --- Center text above the image ---
x = (W - text_width) / 2
y = 20
draw.text((x, y), meme_text, font=font, fill="black")

# --- Paste original image below the text ---
new_img.paste(img, (0, font_size + 40))

# --- Save or show ---
new_img.save("meme_with_big_text.jpg")
new_img.show()
