"""Create application icon."""
from PIL import Image, ImageDraw

# Create a bell/alert icon
img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw bell shape in purple
# Bell body
draw.ellipse([15, 15, 49, 49], fill=(124, 58, 237, 255))
# Inner white circle
draw.ellipse([22, 22, 42, 42], fill=(255, 255, 255, 255))
# Notification dot (red)
draw.ellipse([42, 12, 54, 24], fill=(239, 68, 68, 255))

# Save as PNG and ICO
img.save('web_alert/icons/icon.png')
img.save('web_alert/icons/icon.ico')
print("Icons created successfully!")
