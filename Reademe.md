# Run in development
! pip install -r requirements
! uvicorn app:app

# Docs 

Navigate to /docs route after running the server to get the API swagger UI documentation.

# Build the image
docker build -t <Image-Name> .

# Run the container

docker run -p 8000:8000 <Image-Name>

This will build the Docker image and run a container with the FastAPI app. The app will be accessible at http://localhost:8000.