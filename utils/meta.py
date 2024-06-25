import re

def add_spaces_before_uppercase(text):
  return re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

def extract_metadata(video):
    action = video.filename.split('/')[-1].split('.')[0].split('_')[1]
    duration, fps, size = video.duration, video.fps, video.size
    key_frames = [video.get_frame(t) for t in range(int(duration)+1)]
    return duration, fps, size, key_frames