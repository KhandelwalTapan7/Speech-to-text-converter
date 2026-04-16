import os
import magic

def check_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    file_info = magic.from_file(file_path)
    print(f"File: {file_path}")
    print(f"Type: {file_info}")
    print(f"Size: {os.path.getsize(file_path)} bytes")
    
    # Check extension
    ext = os.path.splitext(file_path)[1].lower()
    print(f"Extension: {ext}")

if __name__ == "__main__":
    # Replace with your WAV file path
    check_file("path_to_your_wav_file.wav")