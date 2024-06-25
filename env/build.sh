docker rmi -f python-env:3.9
docker build -t python-env:3.9 -f "$(pwd)/env/Dockerfile" .