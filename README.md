
# VidProUCF

![Preview](https://github.com/iamarijit/vid-pro-sys/blob/init/ss.png)
VidProUCF is a video processing system to extract and store features from videos of the [UCF101](https://www.crcv.ucf.edu/research/data-sets/ucf101/) dataset. It comes with an interactive web application to filter videos based on the extracted features.

## Demo

A demo app built on a tiny subset of the UCF101 dataset is hosted at https://vidpro-ucf-iamarijit.streamlit.app/.

## Setup

1. Install docker using instructions at https://docs.docker.com/engine/install/ 
2.    Build docker image 
```   
./env/build.sh
```

3.  Start docker container 
```
./env/start.sh
```
4. Open container CLI 
```
./env/bash.sh
```
5. Install dependencies
```
pip install -r requirements.txt
```

## Usage

### Download dataset
```
wget  --no-check-certificate  https://www.crcv.ucf.edu/datasets/human-actions/ucf101/UCF101.rar
unrar  x  UCF101.rar
```
Convert the raw videos to H264 codec which is supported by HTML5 video player
```
./convert.sh
```
**Note**: Change  **`video_dir`** to **UCF101** dataset path on local machine

### Extract & store features
```
python process.py
```
**Note**: Change  **`root`** to **UCF101** dataset path on local machine

###  Run web app to filter videos
```
streamlit run deploy.py
```
  Open http://localhost:8501 on your browser
