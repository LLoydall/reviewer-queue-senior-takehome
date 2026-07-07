import asyncio

from app.main import health, list_review_items


def run_async(coro):
    return asyncio.run(coro)


def test_health_check() -> None:
    assert run_async(health()) == {"status": "ok"}


def test_review_items_endpoint_returns_only_active_items() -> None:
    response = run_async(list_review_items(list_type="active"))
    assert len(response["items"]) > 0

def test_review_items_endpoint_returns_only_active_items() -> None:
    response = run_async(list_review_items(list_type="active"))
    assert all(item["status"] not in {"approved", "rejected", "escalated"} for item in response["items"])

def test_review_items_endpoint_returns_terminated_items() -> None:
    response = run_async(list_review_items(list_type="terminal"))
    assert all(item["status"] in {"approved", "rejected", "escalated"} for item in response["items"])