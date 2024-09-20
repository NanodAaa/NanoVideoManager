import os
from PIL import Image

# 指定图片所在的文件夹路径
folder_path = input('Please input the input path: ')

# 创建一个输出文件夹
output_folder = os.path.join(folder_path, 'rotated_images')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 确保只处理图片文件（如jpg, png等）
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        # 打开图片
        img_path = os.path.join(folder_path, filename)
        img = Image.open(img_path)
        
        # 将图片旋转90度
        rotated_img = img.rotate(-90, expand=True)
        
        # 保存旋转后的图片到输出文件夹
        rotated_img.save(os.path.join(output_folder, filename))

print(f"图片已保存至：{output_folder}")
