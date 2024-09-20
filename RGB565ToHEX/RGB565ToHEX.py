from PIL import Image
import numpy as np
import os

def rgb_to_rgb565(r, g, b):
    """Convert RGB888 to RGB565."""
    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return rgb565

def image_to_rgb565_hex(image_path, output_path=None):
    """Convert an image to RGB565 hex format."""
    # Load the image
    image = Image.open(image_path)
    image = image.convert('RGB')
    
    # Get image dimensions
    width, height = image.size
    
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Initialize list to hold hex data
    hex_data = []
    
    # Convert each pixel to RGB565
    for y in range(height):
        for x in range(width):
            r, g, b = img_array[y, x]
            rgb565 = rgb_to_rgb565(r, g, b)
            hex_data.append(f"0x{rgb565:04X}, ")
        hex_data.append("\n")
    
    # Optionally write hex data to a file
    if output_path:
        with open(output_path, 'w') as f:
            f.write("".join(hex_data))
    
    return hex_data

def image_to_rgb565_hex_folder(folder_path):
    """Convert all images in a folder to RGB565 hex format."""
    for file in os.listdir(folder_path):
        if file.endswith('.bmp') or file.endswith('.png') or file.endswith('.jpg'):
            image_path = os.path.join(folder_path, file)
            output_path = os.path.join(folder_path, file.split('.')[0] + '-rgb565.txt')
            image_to_rgb565_hex(image_path, output_path)

# Main
print("##################################################")
print("RGB565 To HEX Converter")
dir_path = input("Please input the folder path:")

print("Files prepare to convert:")
for file in os.listdir(dir_path):
    if file.endswith('.bmp') or file.endswith('.png') or file.endswith('.jpg'):
        print(file)

if(input("# Continue to convert files? (y/n): ").lower() == 'y'):
    print("# Converting files\n")
    image_to_rgb565_hex_folder(dir_path)
else:
    print("# Exiting...")
    exit()


