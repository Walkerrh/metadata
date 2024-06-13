# from PIL import Image as PILImage
# from PIL.ExifTags import TAGS, GPSTAGS
# import json
# import fractions

# class CustomJSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         # Handle fractions.Fraction
#         if isinstance(obj, fractions.Fraction):
#             return float(obj)
#         # Handle unexpected non-serializable objects
#         try:
#             return float(obj)
#         except (TypeError, ValueError):
#             return str(obj)
#         return super().default(obj)

# def get_exif_metadata(file_path):
#     image = PILImage.open(file_path)
#     exif_data = image._getexif()

#     if exif_data is not None:
#         exif = {}
#         for tag, value in exif_data.items():
#             tag_name = TAGS.get(tag, tag)
#             exif[tag_name] = value

#             if tag_name == 'GPSInfo':
#                 gps_data = {}
#                 for gps_tag in value:
#                     gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
#                     gps_data[gps_tag_name] = value[gps_tag]
#                 exif[tag_name] = gps_data

#         return exif
#     else:
#         return None

# def main():
#     file_path = 'C:/Users/razer/Desktop/walkerrh.github.io/assets/me/ban_gioc.png'  # Replace with your image file path
#     exif_metadata = get_exif_metadata(file_path)
    
#     if exif_metadata:
#         # Pretty print the JSON output using the custom JSON encoder
#         print(json.dumps(exif_metadata, indent=4, cls=CustomJSONEncoder))
#     else:
#         print("No Exif metadata found")

# if __name__ == "__main__":
#     main()



""" 
Pillow: A Python Imaging Library (PIL) fork, which adds support for opening, manipulating, and saving image files.
json: A built-in Python library to handle JSON data.

PIL.Image is used for opening and manipulating images.
PIL.ExifTags contains constants for interpreting Exif metadata.
json is used to serialize Python objects into JSON strings.
fractions is used to handle rational numbers in Exif metadata.

[Custom JSON Encoder Class]
This class CustomJSONEncoder extends the default JSON encoder to handle special types:
Converts fractions.Fraction to float.
Tries to convert any non-serializable object to float, and if it fails, converts it to a string.

[Function to Extract Exif Metadata]
PILImage.open(file_path): Opens the image file.
image._getexif(): Retrieves Exif metadata from the image.
The function then processes the Exif data:
Converts tag codes to human-readable tag names using TAGS.
Filters out binary data for cleaner output.
Processes GPS information separately to convert GPS tag codes to names using GPSTAGS.

[Main Function]
file_path: Path to the image file.
Calls get_exif_metadata(file_path) to extract metadata.
Prints the metadata as a prettified JSON string using the CustomJSONEncoder for serialization.

[How the Packages Work Together]
Pillow: Opens the image and extracts Exif metadata. Exif metadata is embedded in image files and contains information about the image, such as camera make and model, date taken, GPS coordinates, and more.
ExifTags: Provides dictionaries to convert Exif tag IDs and GPS tag IDs into human-readable names.
json: Serializes the extracted and processed metadata into a JSON string. The custom JSON encoder handles non-standard types that are not directly serializable, ensuring all data can be outputted in a readable format.

[How the Data is Handled]
1. Opening the Image:
    * The image file is opened using PILImage.open(file_path).
2. Extracting Exif Metadata:
    * Metadata is extracted using image._getexif().
3. Processing Metadata:
    * Exif data is processed to convert tag IDs to human-readable names.
    * GPS information is processed separately to handle nested tags.
    * Binary data is filtered out to avoid clutter.
4. Serializing Metadata:
    * Processed metadata is serialized into a JSON string using json.dumps() with the CustomJSONEncoder.
5. Output:
    * The JSON string is printed to the console, providing a readable representation of the image's metadata.
"""



from PIL import Image as PILImage
from PIL.ExifTags import TAGS, GPSTAGS
import json
import fractions

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Handle fractions.Fraction
        if isinstance(obj, fractions.Fraction):
            return float(obj)
        # Handle unexpected non-serializable objects
        try:
            return float(obj)
        except (TypeError, ValueError):
            return str(obj)
        return super().default(obj)

def get_exif_metadata(file_path):
    image = PILImage.open(file_path)
    exif_data = image._getexif()

    if exif_data is not None:
        exif = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            # Skip binary data for cleaner output
            if isinstance(value, bytes):
                continue
            exif[tag_name] = value

            if tag_name == 'GPSInfo':
                gps_data = {}
                for gps_tag in value:
                    gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[gps_tag_name] = value[gps_tag]
                exif[tag_name] = gps_data

        return exif
    else:
        return None

def main():
    file_path = r"C:\Users\razer\Desktop\WALKER\New folder\ban_gioc.PNG"  # Replace with your image file path
    exif_metadata = get_exif_metadata(file_path)
    
    if exif_metadata:
        # Pretty print the JSON output using the custom JSON encoder
        print(json.dumps(exif_metadata, indent=4, cls=CustomJSONEncoder))
    else:
        print("No Exif metadata found")

if __name__ == "__main__":
    main()
