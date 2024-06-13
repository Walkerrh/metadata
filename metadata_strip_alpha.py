from PIL import Image as PILImage
import os

def remove_exif_metadata(file_path, output_path):
    image = PILImage.open(file_path)
    data = list(image.getdata())
    image_without_exif = PILImage.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save(output_path)

def main():
    file_path = r"C:\Users\razer\Desktop\New folder\ban_gioc.PNG"  # Replace with your image file path
    output_path = r"C:\Users\razer\Desktop\New folder\new\ban_gioc_smudged.png"  # Output file path
    
    remove_exif_metadata(file_path, output_path)
    print(f"Exif metadata removed. Image saved to {output_path}")

if __name__ == "__main__":
    main()
