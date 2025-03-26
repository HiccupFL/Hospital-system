import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 创建图标目录
icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')
os.makedirs(icon_dir, exist_ok=True)

# 创建一个简单的医药图标
icon_size = 128
img = Image.new('RGBA', (icon_size, icon_size), color=(255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# 绘制一个圆形背景
center = icon_size // 2
radius = icon_size // 2 - 4
draw.ellipse((center - radius, center - radius, center + radius, center + radius), fill=(0, 120, 212))

# 绘制十字标志
cross_width = radius // 2
cross_thickness = radius // 4
draw.rectangle((center - cross_thickness//2, center - cross_width, 
                center + cross_thickness//2, center + cross_width), fill=(255, 255, 255))
draw.rectangle((center - cross_width, center - cross_thickness//2, 
                center + cross_width, center + cross_thickness//2), fill=(255, 255, 255))

# 保存图标
icon_path = os.path.join(icon_dir, 'medicine_icon.png')
img.save(icon_path)

print(f"图标已创建: {icon_path}")