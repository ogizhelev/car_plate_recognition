import requests
from PIL import Image
from io import BytesIO
import logging

_LOGGER = logging.getLogger(__name__)

def download_image(frigate_host: str, camera: str, event: dict):
    """Download the image for the specified camera event."""
    image_url = f"{frigate_host}/api/events/{event['id']}/image"  # Modify based on Frigate's API
    response = requests.get(image_url)
    if response.status_code == 200:
        _LOGGER.info(f"Image downloaded for camera: {camera}")
        image = Image.open(BytesIO(response.content))
        return image
    else:
        _LOGGER.error(f"Failed to download image for {camera}, status code: {response.status_code}")
        return None

def send_image_to_code_project(image: Image, code_project_host: str):
    """Send the downloaded image to the CODE_PROJECT_HOST for car plate recognition."""
    image.save("temp_image.jpg")  # Save the image temporarily for sending
    with open("temp_image.jpg", "rb") as img_file:
        response = requests.post(f"{code_project_host}/process_image", files={"file": img_file})
        if response.status_code == 200:
            result = response.json()
            if 'car_plate' in result:
                return result['car_plate']
            else:
                _LOGGER.warning("Car plate not recognized.")
                return None
        else:
            _LOGGER.error(f"Failed to send image for processing, status code: {response.status_code}")
            return None

def process_camera_event(frigate_host: str, code_project_host: str, camera: str, event: dict):
    """Process the camera event."""
    image = download_image(frigate_host, camera, event)
    if image:
        car_plate = send_image_to_code_project(image, code_project_host)
        if car_plate:
            _LOGGER.info(f"Car plate recognized: {car_plate}")
            return car_plate
        else:
            return None
    else:
        return None
