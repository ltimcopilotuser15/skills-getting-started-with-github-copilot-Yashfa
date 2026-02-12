import pytest
from httpx import AsyncClient
from src.app import app

import asyncio

@pytest.mark.asyncio
async def test_get_activities():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v for v in data.values())

@pytest.mark.asyncio
async def test_signup_and_unregister():
    test_email = "testuser@mergington.edu"
    activity = next(iter((await AsyncClient(app=app, base_url="http://test").get("/activities")).json().keys()))
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Sign up
        resp_signup = await ac.post(f"/activities/{activity}/signup?email={test_email}")
        assert resp_signup.status_code == 200
        # Duplicate signup should fail
        resp_dup = await ac.post(f"/activities/{activity}/signup?email={test_email}")
        assert resp_dup.status_code == 400
        # Unregister
        resp_unreg = await ac.post(f"/activities/{activity}/unregister?email={test_email}")
        assert resp_unreg.status_code == 200
        # Unregister again should fail
        resp_unreg2 = await ac.post(f"/activities/{activity}/unregister?email={test_email}")
        assert resp_unreg2.status_code == 400
