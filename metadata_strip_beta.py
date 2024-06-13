from PIL import Image as PILImage
from PIL.ExifTags import TAGS, GPSTAGS, GPSTAGS_INV
from fractions import Fraction

def modify_exif_metadata(file_path, output_path):
    image = PILImage.open(file_path)
    exif_data = image._getexif()
    
    if exif_data is not None:
        new_exif_data = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            # Modify specific Exif fields
            if tag_name == "GPSInfo":
                value = {
                    GPSTAGS_INV['GPSLatitude']: (0, 0, 0),
                    GPSTAGS_INV['GPSLongitude']: (0, 0, 0),
                    GPSTAGS_INV['GPSLatitudeRef']: "N",
                    GPSTAGS_INV['GPSLongitudeRef']: "E"
                }
            elif tag_name == "Make":
                value = "Unknown"
            elif tag_name == "Model":
                value = "Unknown"
            # Add other modifications as needed
            
            new_exif_data[tag] = value
        
        # Save the image with modified Exif data
        image.save(output_path, exif=new_exif_data)
        print(f"Exif metadata modified and image saved to {output_path}")
    else:
        print("No Exif metadata found in the image")

def main():
    file_path = r"C:\Users\razer\Desktop\New folder\ban_gioc.PNG"  # Replace with your image file path
    output_path = r"C:\Users\razer\Desktop\New folder\new\ban_gioc_smudged.png"  # Output file path
    
    modify_exif_metadata(file_path, output_path)

if __name__ == "__main__":
    main()
