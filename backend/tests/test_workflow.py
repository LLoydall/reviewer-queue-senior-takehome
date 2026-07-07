from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_cannot_claim_in_review_item():
    client.post("/dev/reset")
    
    claim_res = client.post("/review-items/RV-1027/actions", json={"action": "claim"})
    assert claim_res.status_code == 409
    assert claim_res.json()["detail"] == "Only unassigned items can be claimed"

def test_cannot_approve_unassigned_item():
    client.post("/dev/reset")
    
    approve_res = client.post("/review-items/RV-1024/actions", json={"action": "approve"})
    assert approve_res.status_code == 409
    assert approve_res.json()["detail"] == "Item must be in review to perform this action"