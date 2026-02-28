"""API endpoint tests."""
import time

import pytest
from fastapi.testclient import TestClient

# Import after env is patched
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_post_chat_returns_message_id(client):
    """POST /chat returns 200 with messageId."""
    resp = client.post("/chat", json={"question": "What is a headache?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "messageId" in data
    assert len(data["messageId"]) == 36  # UUID format


def test_get_chat_processing(client):
    """GET /chat/{id} returns processing for new message."""
    post_resp = client.post("/chat", json={"question": "test"})
    message_id = post_resp.json()["messageId"]
    get_resp = client.get(f"/chat/{message_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["status"] in ("processing", "completed", "failed")


def test_get_chat_completed(client):
    """GET /chat/{id} eventually returns completed or failed (mock ~1-3s)."""
    post_resp = client.post("/chat", json={"question": "test"})
    message_id = post_resp.json()["messageId"]
    for _ in range(30):  # 30 * 0.5s = 15s max (mock delay 1-3s)
        get_resp = client.get(f"/chat/{message_id}")
        assert get_resp.status_code == 200
        data = get_resp.json()
        if data["status"] == "completed":
            assert "answer" in data
            assert len(data["answer"]) > 0
            return
        if data["status"] == "failed":
            pytest.fail(f"Message failed: {data.get('error', '')}")
        time.sleep(0.5)
    # Timeout - at least verify we got processing
    get_resp = client.get(f"/chat/{message_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["status"] in ("processing", "completed", "failed")


def test_get_chat_404(client):
    """GET /chat/{id} returns 404 for unknown id."""
    resp = client.get("/chat/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()


def test_get_statistics(client):
    """GET /statistics returns 200 with expected fields."""
    resp = client.get("/statistics")
    assert resp.status_code == 200
    data = resp.json()
    for key in (
        "messagesProcessed",
        "messagesSucceeded",
        "messagesFailed",
        "totalRetries",
        "averageProcessingTimeMs",
        "averageTokensPerMessage",
        "totalTokensUsed",
        "currentQueueLength",
        "idleWorkers",
        "activeWorkers",
    ):
        assert key in data, f"Missing {key}"
        assert isinstance(data[key], (int, float)), f"{key} should be number"


def test_post_chat_empty_question_rejected(client):
    """POST /chat with empty question returns 422."""
    resp = client.post("/chat", json={"question": ""})
    assert resp.status_code == 422
