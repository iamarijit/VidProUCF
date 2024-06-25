#!/bin/bash

video_dir="./UCF-101"

for file in "$video_dir"/**/*.avi; do
  filename="${file%.*}"
  
  if [[ -f "$file" ]]; then
    output_file="$filename.mp4"
    ffmpeg -y -i "$file" -vcodec libx264 "$output_file"
    rm "$file"
    
    echo "Converted '$file' to '$output_file'"
  fi
done
