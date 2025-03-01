import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_state_change
from homeassistant.components.camera import CameraEntity
from homeassistant.const import STATE_ON, STATE_OFF
from .camera_event_handler import process_camera_event

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up the Car Plate Recognition component from a config entry."""
    frigate_host = entry.data['host']  # Frigate host URL (configured by user)
    code_project_host = entry.data['code_project_host']  # AI processing service URL
    cameras = entry.data['cameras']  # List of camera IDs or names

    # Register a state change listener for each camera
    for camera in cameras:
        async_track_state_change(
            hass, camera, lambda entity_id, from_state, to_state: handle_camera_event(
                hass, frigate_host, code_project_host, camera, from_state, to_state
            )
        )
    return True

async def handle_camera_event(hass: HomeAssistant, frigate_host, code_project_host, camera, from_state, to_state):
    """Handle the camera event from Frigate."""
    # Check if the event is related to a relevant state change, e.g., motion detection or object detection
    if to_state.state == STATE_ON:
        _LOGGER.info(f"Event triggered for camera {camera}. Processing image...")
        
        # You could fetch the actual event from Frigate here
        # For example, using Frigate's API to get the event details
        event = await get_frigate_event(frigate_host, camera)
        
        # Process the event
        car_plate = process_camera_event(frigate_host, code_project_host, camera, event)
        if car_plate:
            _LOGGER.info(f"Car plate recognized: {car_plate}")
        else:
            _LOGGER.warning(f"No car plate recognized for camera {camera}.")
    
    else:
        _LOGGER.info(f"State change from {from_state} to {to_state} ignored for camera {camera}.")

async def get_frigate_event(frigate_host, camera):
    """Fetch the relevant event details from Frigate."""
    # Placeholder code for fetching event data from Frigate API.
    # This may require modifying based on Frigate's actual API.
    event_url = f"{frigate_host}/api/events/{camera}/latest"  # Modify accordingly
    response = await hass.async_add_executor_job(requests.get, event_url)
    if response.status_code == 200:
        return response.json()
    else:
        _LOGGER.error(f"Failed to get event from Frigate, status code: {response.status_code}")
        return None
