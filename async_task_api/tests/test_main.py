# Unit tests using FastAPI’s TestClient and pytest.


# • Tests cover the task creation, status checking, and streaming endpoints.
# • The tests use the authentication header provided by the configuration.

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

@pytest.fixture
def auth_header():
    return {"Authorization": f"Bearer {settings.SECRET_TOKEN}"}

def test_create_task(auth_header):
    payload = {"task_id":101,"data":"test data"}
    response = client.post("/tasks/", headers=auth_header, json= payload)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["task_id"] == 101
    assert json_resp["status"] == "completed"
    assert "Processed data:" in json_resp["result"]

def test_task_status(auth_header):
    # First, create a task
    payload ={"task_id":102,"data":"status check"}
    client.post("/tasks/", headers=auth_header,json=payload)

    # Now, get the status (since task processing takes a few seconds,
    # you might need to wait for completion in real tests)
    response = client.get("/tasks/102/status", headers = auth_header)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["task_id"] == 102
    assert json_resp["status"] in ["in progress", "completed"]

def tast_stream_numbers(auth_header):
    response = client.get("/stream/", headers = auth_header)
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    # Since generator streams numbers, content should include "Number:"
    assert "Number:" in content

