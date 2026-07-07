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

def test_active_queue_filtering_and_sorting():
    client.post("/dev/reset")
    
    response = client.get("/review-items")
    assert response.status_code == 200
    
    items = response.json()["items"]
    
    # 1. Verify Filtering: No terminal states should be in the active queue
    terminal_states = {"approved", "rejected", "escalated"}
    for item in items:
        assert item["status"] not in terminal_states
        
    # 2. Verify Sorting rules
    risk_weight = {"high": 1, "medium": 2, "low": 3}
    tier_weight = {"priority": 1, "standard": 2}
    
    for i in range(len(items) - 1):
        current = items[i]
        next_item = items[i + 1]
        
        curr_risk = risk_weight[current["risk_level"]]
        next_risk = risk_weight[next_item["risk_level"]]
        
        curr_tier = tier_weight[current["customer_tier"]]
        next_tier = tier_weight[next_item["customer_tier"]]
        
        # Rule A: Higher risk outranks lower risk
        assert curr_risk <= next_risk
        
        if curr_risk == next_risk:
            # Rule B: Priority outranks standard within the same risk
            assert curr_tier <= next_tier
            
            if curr_tier == next_tier:
                # Rule C: Older items outrank newer items within the same tier and risk
                assert current["submitted_at"] <= next_item["submitted_at"]


def test_terminal_items_cannot_be_modified():
    client.post("/dev/reset")
    
    # RV-1029 is seeded as 'approved'
    response_approved = client.post(
        "/review-items/RV-1029/actions", 
        json={"action": "reject"}
    )
    assert response_approved.status_code == 409
    assert response_approved.json()["detail"] == "This item is closed and cannot be modified"
    
    # RV-1033 is seeded as 'escalated'
    response_escalated = client.post(
        "/review-items/RV-1033/actions", 
        json={"action": "claim"}
    )
    assert response_escalated.status_code == 409
    assert response_escalated.json()["detail"] == "This item is closed and cannot be modified"
    
    # RV-1034 is seeded as 'rejected'
    response_rejected = client.post(
        "/review-items/RV-1034/actions", 
        json={"action": "approve"}
    )
    assert response_rejected.status_code == 409
    assert response_rejected.json()["detail"] == "This item is closed and cannot be modified"