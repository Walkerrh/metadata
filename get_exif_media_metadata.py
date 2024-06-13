



from PIL import Image as PILImage
from PIL.ExifTags import TAGS, GPSTAGS
from pymediainfo import MediaInfo
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

def get_media_metadata(file_path):
    media_info = MediaInfo.parse(file_path)
    return media_info

def main():
    file_path = r"C:\Users\razer\Desktop\New folder\new\ban_gioc_smudged.png"  # Replace with your media file path
    
    exif_metadata = get_exif_metadata(file_path)
    media_info = get_media_metadata(file_path)
    media_metadata = [track.to_data() for track in media_info.tracks]
    
    combined_metadata = {
        'exif_metadata': exif_metadata,
        'media_metadata': media_metadata
    }
    
    # Pretty print the combined JSON output
    print(json.dumps(combined_metadata, indent=4, cls=CustomJSONEncoder))

if __name__ == "__main__":
    main()
