from moviepy.editor import VideoFileClip
import os

from utils.db import get_table, drop_table, fetch_data, insert_data
from utils.meta import add_spaces_before_uppercase, extract_metadata
from utils.model import extract_model_info, get_models

def get_video_paths(root, no_of_actions=5):
    actions = [action for action in os.listdir(root) if os.path.isdir(os.path.join(root, action))][:no_of_actions]
    all_files = []

    for action in actions:
        folder = os.listdir(os.path.join(root, action))
        all_files += [os.path.join(root, action, file) for file in folder if '.mp4' in file]

    print(f"Collecting data for {no_of_actions} actions : {actions}")
    return all_files

def extract_and_insert_single_video_data(file, conn, table, models):
    segment_feature_extractor, segment_model, gender_feature_extractor, gender_model = models
    clip = VideoFileClip(file)

    action = add_spaces_before_uppercase(file.split('/')[-2])
    duration, fps, resolution, key_frames = extract_metadata(clip)
    is_human_present, genders, location = extract_model_info(
        key_frames, 
        segment_feature_extractor, 
        segment_model, 
        gender_feature_extractor, 
        gender_model)
    
    insert_data(conn, table, file, location, genders, len(key_frames), duration, fps, resolution, action, is_human_present)

def display_data(location='Indoor', gender='Female', action='Cliff Diving'):
    conn, table = get_table()
    result = fetch_data(conn, table, location, gender, action)

    for each in result:
        print(each)
    
    conn.close()

def drop_existing_table():
    conn, _ = get_table()
    drop_table(conn)
    conn.close()
    print('Table dropped !')

def insert_ucf_data_to_table(root, print_freq=1):
    conn, table = get_table()
    file_paths = get_video_paths(root)
    models = get_models()

    no_of_videos = len(file_paths)
    for idx, file in enumerate(file_paths):
        extract_and_insert_single_video_data(file, conn, table, models)

        if idx % print_freq == 0:
            print(f"Data inserted for {idx+1}/{no_of_videos} videos")

    conn.close()

def main():
    root = './UCF-101'
    drop = True
    
    if drop:
        drop_existing_table()
    
    if root:
        insert_ucf_data_to_table(root)

if __name__ == '__main__':
    main()
