# Build the image

docker build -t <Image-Name> .

# Run the container

docker run -p 8000:8000 <Image-Name>

This will build the Docker image and run a container with the FastAPI app. The app will be accessible at http://localhost:8000.