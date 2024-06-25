docker rm -f vid_sys
docker run --name vid_sys \
-p 8888:8888 \
-p 8501:8501 \
-v "$(pwd):/app" \
-d python-env:3.9