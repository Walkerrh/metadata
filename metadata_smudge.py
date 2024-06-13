from PIL import Image as PILImage
from PIL.ExifTags import TAGS, GPSTAGS
from pymediainfo import MediaInfo
import json
import fractions
import piexif

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
    exif_data = image.info.get('exif')

    if exif_data is not None:
        exif_dict = piexif.load(exif_data)
        exif = {}
        for ifd in exif_dict:
            for tag in exif_dict[ifd]:
                tag_name = TAGS.get(tag, tag)
                value = exif_dict[ifd][tag]
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

def modify_exif_metadata(file_path, output_path):
    image = PILImage.open(file_path)
    exif_data = image.info.get('exif')
    
    # Create inverse mapping for GPSTAGS
    GPSTAGS_INV = {v: k for k, v in GPSTAGS.items()}
    
    if exif_data is not None:
        exif_dict = piexif.load(exif_data)
        for ifd in exif_dict:
            for tag in exif_dict[ifd]:
                tag_name = TAGS.get(tag, tag)
                # Modify specific Exif fields
                if tag_name == "GPSInfo":
                    exif_dict[ifd][tag] = {
                        GPSTAGS_INV['GPSLatitude']: ((0, 1), (0, 1), (0, 1)),
                        GPSTAGS_INV['GPSLongitude']: ((0, 1), (0, 1), (0, 1)),
                        GPSTAGS_INV['GPSLatitudeRef']: "N",
                        GPSTAGS_INV['GPSLongitudeRef']: "E"
                    }
                elif tag_name == "Make":
                    exif_dict[ifd][tag] = "Unknown"
                elif tag_name == "Model":
                    exif_dict[ifd][tag] = "Unknown"
                # Add other modifications as needed

        exif_bytes = piexif.dump(exif_dict)
        image.save(output_path, exif=exif_bytes)
        print(f"Exif metadata modified and image saved to {output_path}")
    else:
        image.save(output_path)
        print("No Exif metadata found in the image. Image saved without Exif data.")

def smudge_file_dates(media_info):
    smudged_dates = {
        "file_creation_date": "1970-01-01 00:00:00.000 UTC",
        "file_creation_date__local": "1970-01-01 00:00:00.000",
        "file_last_modification_date": "1970-01-01 00:00:00.000 UTC",
        "file_last_modification_date__local": "1970-01-01 00:00:00.000"
    }
    for track in media_info.tracks:
        for key in smudged_dates:
            if hasattr(track, key):
                setattr(track, key, smudged_dates[key])
    return media_info

def main():
    file_path = r"C:\Users\razer\Desktop\New folder\ban_gioc.PNG"  # Replace with your media file path
    output_path = r"C:\Users\razer\Desktop\New folder\new\ban_gioc_smudged.png"  # Output file path
    
    # Modify Exif metadata
    modify_exif_metadata(file_path, output_path)
    
    # Get media metadata and smudge file dates
    media_info = get_media_metadata(output_path)
    smudged_media_info = smudge_file_dates(media_info)
    media_metadata = [track.to_data() for track in smudged_media_info.tracks]
    
    # Combine metadata
    exif_metadata = get_exif_metadata(output_path)
    combined_metadata = {
        'exif_metadata': exif_metadata,
        'media_metadata': media_metadata
    }
    
    # Pretty print the combined JSON output
    print(json.dumps(combined_metadata, indent=4, cls=CustomJSONEncoder))

if __name__ == "__main__":
    main()
