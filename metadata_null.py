# from PIL import Image as PILImage
# from pymediainfo import MediaInfo
# import json
# import piexif

# class CustomJSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         # Handle unexpected non-serializable objects
#         try:
#             return float(obj)
#         except (TypeError, ValueError):
#             return str(obj)
#         return super().default(obj)

# def get_exif_metadata(file_path):
#     image = PILImage.open(file_path)
#     exif_data = image.info.get('exif')

#     if exif_data is not None:
#         exif_dict = piexif.load(exif_data)
#         exif = {}
#         for ifd in exif_dict:
#             for tag in exif_dict[ifd]:
#                 tag_name = piexif.TAGS.get(ifd, {}).get(tag, (None, None))[0]
#                 if tag_name:
#                     value = exif_dict[ifd][tag]
#                     # Skip binary data for cleaner output
#                     if isinstance(value, bytes):
#                         continue
#                     exif[tag_name] = value

#                     if tag_name == 'GPSInfo':
#                         gps_data = {}
#                         for gps_tag in value:
#                             gps_tag_name = piexif.GPSIFD.get(gps_tag, gps_tag)
#                             gps_data[gps_tag_name] = value[gps_tag]
#                         exif[tag_name] = gps_data

#         return exif
#     else:
#         return None

# def get_media_metadata(file_path):
#     media_info = MediaInfo.parse(file_path)
#     return media_info

# def modify_exif_metadata(file_path, output_path):
#     image = PILImage.open(file_path)
#     image.save(output_path)
#     print("Image saved without modifying Exif metadata.")

# def main():
#     file_path = r"C:\Users\razer\Desktop\New folder\ban_gioc.PNG"  # Replace with your media file path
#     output_path = r"C:\Users\razer\Desktop\New folder\new\ban_gioc_smudged.png"  # Output file path
    
#     # Save image without modifying Exif metadata
#     modify_exif_metadata(file_path, output_path)
    
#     # Nullify Exif metadata
#     exif_metadata = None
    
#     # Get media metadata and set to null
#     media_info = get_media_metadata(output_path)
#     media_metadata = None
    
#     # Combine metadata
#     combined_metadata = {
#         'exif_metadata': exif_metadata,
#         'media_metadata': media_metadata
#     }
    
#     # Pretty print the combined JSON output
#     print(json.dumps(combined_metadata, indent=4, cls=CustomJSONEncoder))

# if __name__ == "__main__":
#     main()















from PIL import Image as PILImage
from pymediainfo import MediaInfo
import json
import piexif

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Handle unexpected non-serializable objects
        try:
            return float(obj)
        except (TypeError, ValueError):
            return str(obj)
        return super().default(obj)

def remove_exif_metadata(file_path, output_path):
    image = PILImage.open(file_path)
    exif_data = image.info.get('exif')
    if exif_data:
        exif_dict = piexif.load(exif_data)
        exif_bytes = piexif.dump({})
        image.save(output_path, exif=exif_bytes)
        print(f"Exif metadata removed. Image saved to {output_path}")
    else:
        image.save(output_path)
        print("No Exif metadata found in the image. Image saved without Exif data.")

def get_media_metadata(file_path):
    media_info = MediaInfo.parse(file_path)
    return media_info

def nullify_media_metadata(media_info):
    # Set media metadata fields to None
    nullified_fields = [
        "file_creation_date", "file_creation_date__local",
        "file_last_modification_date", "file_last_modification_date__local"
    ]
    for track in media_info.tracks:
        for field in nullified_fields:
            if hasattr(track, field):
                setattr(track, field, None)
    return media_info

def main():
    file_path = r"C:\Users\razer\Desktop\New folder\ban_gioc.PNG"  # Replace with your media file path
    output_path = r"C:\Users\razer\Desktop\New folder\new\ban_gioc_smudged.png"  # Output file path
    
    # Remove Exif metadata from image
    remove_exif_metadata(file_path, output_path)
    
    # Get media metadata and nullify specific fields
    media_info = get_media_metadata(output_path)
    nullified_media_info = nullify_media_metadata(media_info)
    media_metadata = None  # Set to None for JSON output
    
    # Combine metadata
    exif_metadata = None  # Set to None for JSON output
    combined_metadata = {
        'exif_metadata': exif_metadata,
        'media_metadata': media_metadata
    }
    
    # Pretty print the combined JSON output
    print(json.dumps(combined_metadata, indent=4, cls=CustomJSONEncoder))

if __name__ == "__main__":
    main()

















