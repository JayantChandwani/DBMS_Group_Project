from PIL import Image, ImageDraw, ImageFont

# Create a blank gray image
img = Image.new('RGB', (184, 246), color='#cccccc')
draw = ImageDraw.Draw(img)

# Add some text
text = "No Image"
try:
    # Attempt to load a font, fall back to default if not available
    font = ImageFont.truetype("arial.ttf", 20)
except IOError:
    font = ImageFont.load_default()

# Calculate text position to center it
text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
position = ((184 - text_width) // 2, (246 - text_height) // 2)

# Draw the text
draw.text(position, text, fill='#333333', font=font)

# Save the image
img.save("Products/placeholder.jpg")
print("Placeholder image created successfully!") 