import pytest
import requests
from dotenv import load_dotenv
import os

# Load the .ENV file
load_dotenv()

@pytest.fixture
def headers():
    return {
        "Content-Type": "application/json",
        "Authorization": os.environ.get('BearerAuth')
    }

@pytest.fixture
def base_url():
    return "https://localhost:8000/"

# Respone 200,
def test_check_status_code_ok(headers, base_url):
    url_post = f"{base_url}/camera"
    body = {
        "mode": "video",
        "capture_address": "/home/user/Desktop/ben.mp4",
        "description": "a video camera",
        "rebroadcast_frame_width": 640,
        "min_detection_width": 30,
        "stream_max_faces": -1,
        "config": {
            "face_recognition_threshold": 60,
            "watchlists": [{
                "watchlist_id": "76447ff4-6949-11ea-94cb-001c42a390bd"
            }],
            "events_outputs": [{
                "events_url": "http://127.0.0.1:5100"
            }]
        }
    }
    response = requests.post(url_post, json=body, headers=headers)
    assert response.status_code == 200

# Respone 400, sending wrong parameters
def test_check_status_code_bad_request(headers, base_url):
    url_post = f"{base_url}/camera"
    body = {
        "mode": "video",
        "capture_address": "/home/user/Desktop/ben.mp4",
        "description": "a video camera",
        "rebroadcast_frame_width": 640,
        "min_detection_width": 30,
        "stream_max_faces": 10000,
        "config": {
            "face_recognition_threshold": 60,
            "watchlists": [{
                "watchlist_id": "76447ff4-6949-11ea-94cb-001c42a390bd"
            }],
            "events_outputs": [{
                "events_url": "http://127.0.0.1:5100"
            }]
        }
    }
    response = requests.post(url_post, json=body, headers=headers)
    assert response.status_code == 400

#404 Not Found
def test_check_status_code_Internal_Server_error(headers, base_url):
    url_post = f"{base_url}/WRONG_URL"
    body = {
        "mode": "video",
        "capture_address": "/home/user/Desktop/ben.mp4",
        "description": "a video camera",
        "rebroadcast_frame_width": 640,
        "min_detection_width": 30,
        "stream_max_faces": -1,
        "config": {
            "face_recognition_threshold": 60,
            "watchlists": [{
                "watchlist_id": "76447ff4-6949-11ea-94cb-001c42a390bd"
            }],
            "events_outputs": [{
                "events_url": "http://127.0.0.1:5100"
            }]
        }
    }
    response = requests.post(url_post, json=body, headers=headers)
    assert response.status_code == 404

# 401, Wrong Bearer token
def test_check_status_code_unauthorized(base_url):
    url_post = f"{base_url}/camera"
    headers = {
    "Content-Type": "application/json",
    "Authorization": os.environ.get('WRONG Bearer')
    }
    body = {
        "mode": "video",
        "capture_address": "/home/user/Desktop/ben.mp4",
        "description": "a video camera",
        "rebroadcast_frame_width": 640,
        "min_detection_width": 30,
        "stream_max_faces": -1,
        "config": {
            "face_recognition_threshold": 60,
            "watchlists": [{
                "watchlist_id": "76447ff4-6949-11ea-94cb-001c42a390bd"
            }],
            "events_outputs": [{
                "events_url": "http://127.0.0.1:5100"
            }]
        }
    }
    response = requests.post(url_post, json=body, headers=headers)
    assert response.status_code == 401
