from pymediainfo import MediaInfo
import json

def get_media_metadata(file_path):
    media_info = MediaInfo.parse(file_path)
    return media_info

def main():
    file_path = r"C:\Users\razer\Desktop\WALKER\New folder\ban_gioc.PNG"  # Replace with your media file path
    media_info = get_media_metadata(file_path)

    
    metadata_list = [track.to_data() for track in media_info.tracks]
    
    # Pretty print the JSON output
    print(json.dumps(metadata_list, indent=4))

if __name__ == "__main__":
    main()


