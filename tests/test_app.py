import pytest
from flask import Flask, jsonify
from app.app import app
from app.alert_handler import AlertHandler
from app.assessment_handler import AssessmentHandler

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_event_no_body(client):
    response = client.post('/event', data=None)
    assert response.status_code == 400
    assert response.get_json() == {"message_id": None, "status": "Request body is missing"}

def test_event_invalid_content_type(client):
    response = client.post('/event', data="{}", content_type="text/plain")
    assert response.status_code == 400
    assert response.get_json() == {"message_id": None, "status": "Request Content-Type must be JSON"}

def test_event_invalid_json(client):
    response = client.post('/event', data="invalid json", content_type="application/json")
    assert response.status_code == 400
    assert response.get_json() == {"message_id": None, "status": "No valid JSON body found in the request"}

def test_event_bad_request(client):
    message = {
        "data": {"objectType": "unknownType"},
        "id": "789"
    }
    response = client.post('/event', json=message)
    assert response.status_code == 422

def test_new_open_alert(client, mocker):
    mocker.patch('app.alert_handler.AlertHandler.routing', return_value=("Alert processed", 200))
    message = {
        "data": {
            "objectType": "alertStateChange",
            "objectId": "alert1",
            "objectBefore": {
                "state": "MONITORING",
                "score": 0.0,
                "docCount": 0,
                "target": {"id": "user123"},
                "security": {"orTags1": ["tag1"]},
                "assignedUsers": [{"id": "user123"}],
                "currentStatus": {"code": "ACTIVE"}
            },
            "objectAfter": {
                "state": "OPEN",
                "score": 0.0,
                "docCount": 0,
                "target": {"id": "user123"},
                "security": {"orTags1": ["tag1"]},
                "assignedUsers": [{"id": "user123"}],
                "currentStatus": {"code": "ACTIVE"}
            }
        },
        "id": "123",
        "time": {"delivered": "2023-01-01T00:00:00Z"},
        "type": "alert"
    }
    response = client.post('/event', json=message)
    assert response.status_code == 200

def test_new_completed_assessment_with_hits(client, mocker):
    mocker.patch('app.assessment_handler.AssessmentHandler.routing', return_value=("Assessment processed", 200))
    message = {
        "data": {
            "objectType": "assessmentStateChange",
            "objectId": "assessment1",
            "objectBefore": {
                "state": "IN_PROGRESS",
                "security": {"owners": ["owner1"]},
                "entities": [{"results":{"assignedUsers":[{"id": "user123"}], "status": "ACTIVE"}}]},
            "objectAfter": {
                "state": "COMPLETED_WITH_HITS",
                "security": {"owners": ["owner1"]},
                "entities": [{"results": {"assignedUsers": [{"id": "user123"}], "status": "ACTIVE"}}]
            }
        },
        "id": "456",
        "time": {"delivered": "2023-01-01T00:00:00Z"},
        "type": "assessment"
    }
    response = client.post('/event', json=message)
    assert response.status_code == 200


def test_new_alert_in_monitoring(client, mocker):
    mocker.patch('app.assessment_handler.AssessmentHandler.routing', return_value=("Alert processed", 200))
    message = {
        "id": "123",
        "time": {"delivered": "2023-01-01T00:00:00Z"},
        "type": "alert",
        "data": {
            "objectId": "alert1",
            "objectType": "alertStateChange",
            "objectBefore": None,
            "objectAfter": {               
                "state": 0,
                "score": 0.0,
                "docCount": 0,
                "target": {"id": "user123"},
                "security": {"orTags1": ["tag1"]},
                "assignedUsers": [{"id": "user123"}],
                "currentStatus": {"code": "ACTIVE"}
            }
        }
    }

    response = client.post('/event', json=message)
    assert response.status_code == 200

def test_new_assessment_in_progress(client, mocker):
    mocker.patch('app.assessment_handler.AssessmentHandler.routing', return_value=("Assessment processed", 200))
    message = {
        "id": "456",
        "time": {"delivered": "2023-01-01T00:00:00Z"},
        "type": "assessment",
        "data": {
            "objectType": "assessmentStateChange",
            "objectId": "assessment1",
            "objectBefore": None,
            "objectAfter": {
                "state": "IN_PROGRESS",
                "security": {"owners": ["owner1"]},
                "entities": [{"results": {"assignedUsers": [{"id": "user123"}], "status": "ACTIVE"}}]
            }
        }
    }
    response = client.post('/event', json=message)
    assert response.status_code == 200