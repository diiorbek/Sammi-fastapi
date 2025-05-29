import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from fastapi import status

from src.main import app
from src.utils.database import override_get_db, engine_test, Base

from src.core.session import get_db

app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client



@pytest.mark.asyncio
async def test_user_registration_and_login(test_client: AsyncClient):
    user_data = {"email": f"user_{uuid.uuid4().hex[:8]}@example.com", "password": "strongpassword123", "user_role": "user"}
    response = await test_client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_200_OK, f"Registration failed: {response.text}"
    response = await test_client.post("/auth/login", json=user_data)
    assert response.status_code == status.HTTP_200_OK, f"Login failed: {response.text}"

@pytest.mark.asyncio
async def test_course_crud(test_client: AsyncClient):
    course_payload = {"title": "Test Course", "description": "Course description", "image_url": "https://example.com/image.jpg"}
    response = await test_client.post("/courses/", json=course_payload)
    assert response.status_code == status.HTTP_200_OK
    
    course = response.json()
    course_id = course["id"]
    response = await test_client.get("/courses/")
    assert response.status_code == status.HTTP_200_OK
    assert any(c["id"] == course_id for c in response.json())
    
    response = await test_client.get(f"/courses/{course_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == course_id
    
    update_data = {"title": "Updated Course", "description": "Updated description", "image_url": "https://example.com/updated-image.jpg"}
    response = await test_client.put(f"/courses/{course_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == update_data["title"]
    
    response = await test_client.delete(f"/courses/{course_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Course deleted"

@pytest.mark.asyncio
async def test_video_crud(test_client: AsyncClient):
    course_payload = {"title": "Video Course", "description": "Video course description", "image_url": "https://example.com/image.jpg"}
    course_response = await test_client.post("/courses/", json=course_payload)
    course_id = course_response.json()["id"]
    files = {"file": ("test_video.mp4", b"dummy content")}
    response = await test_client.post(
    "/videos/",
    data={"title": "Test Video", "course_id": str(course_id)},
    files=files
)
    assert response.status_code == status.HTTP_200_OK
    
    video_id = response.json()["id"]

    response = await test_client.get("/videos/")
    assert response.status_code == status.HTTP_200_OK
    assert any(v["id"] == video_id for v in response.json())
    
    response = await test_client.get(f"/videos/{video_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == video_id
    
    response = await test_client.put(f"/videos/{video_id}", data={"title": "Updated Video Title"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Updated Video Title"
    
    response = await test_client.delete(f"/videos/{video_id}")
    assert response.status_code == status.HTTP_200_OK
    assert "deleted successfully" in response.json()["message"]
    await test_client.delete(f"/courses/{course_id}")
