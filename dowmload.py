import yt_dlp

def download_video():
    url = input("Paste the video link here: ")

    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',  # Save with video title
        'format': 'best',                # Best quality
        'noplaylist': True               # Download single video only
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("\nDownloading...")
            ydl.download([url])
            print("\nDownload completed successfully!")
    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    download_video()
