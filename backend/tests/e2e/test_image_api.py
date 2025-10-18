"""
End-to-end tests for Image API endpoints
"""
import pytest
from io import BytesIO

from fastapi.testclient import TestClient


@pytest.mark.e2e
class TestImageAPI:
    """Test suite for /api/images endpoints"""
    
    def test_upload_image_success(self, client):
        """Test successful image upload via API"""
        # Arrange
        fake_image = BytesIO(b"fake image content")
        files = {"file": ("test_card.png", fake_image, "image/png")}
        
        # Act
        response = client.post("/api/images/upload", files=files)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "image_id" in data
        assert data["image_id"] > 0
        assert data["status"] == "non_traite"
        assert data["message"] == "Image uploaded successfully"
    
    def test_upload_image_jpg(self, client):
        """Test uploading JPG image"""
        # Arrange
        fake_image = BytesIO(b"fake jpeg content")
        files = {"file": ("card.jpg", fake_image, "image/jpeg")}
        
        # Act
        response = client.post("/api/images/upload", files=files)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "non_traite"
    
    def test_upload_invalid_file_type(self, client):
        """Test uploading unsupported file type"""
        # Arrange
        fake_file = BytesIO(b"not an image")
        files = {"file": ("document.pdf", fake_file, "application/pdf")}
        
        # Act
        response = client.post("/api/images/upload", files=files)
        
        # Assert
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_upload_no_file(self, client):
        """Test upload endpoint without file"""
        # Act
        response = client.post("/api/images/upload")
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_get_image_by_id_success(self, client):
        """Test retrieving uploaded image by ID"""
        # Arrange - First upload an image
        fake_image = BytesIO(b"test content")
        files = {"file": ("test.png", fake_image, "image/png")}
        upload_response = client.post("/api/images/upload", files=files)
        image_id = upload_response.json()["image_id"]
        
        # Act
        response = client.get(f"/api/images/{image_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == image_id
        assert "original_path" in data
        assert "status" in data
        assert "created_at" in data
    
    def test_get_image_non_existent(self, client):
        """Test retrieving non-existent image"""
        # Act
        response = client.get("/api/images/999999")
        
        # Assert
        assert response.status_code == 404
        assert "detail" in response.json()
    
    def test_get_image_invalid_id(self, client):
        """Test retrieving image with invalid ID format"""
        # Act
        response = client.get("/api/images/invalid")
        
        # Assert
        assert response.status_code == 422  # Validation error
    
    def test_upload_and_retrieve_workflow(self, client):
        """Test complete workflow: upload then retrieve"""
        # Upload
        fake_image = BytesIO(b"workflow test image")
        files = {"file": ("workflow.png", fake_image, "image/png")}
        upload_resp = client.post("/api/images/upload", files=files)
        
        assert upload_resp.status_code == 201
        image_id = upload_resp.json()["image_id"]
        
        # Retrieve
        get_resp = client.get(f"/api/images/{image_id}")
        
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["id"] == image_id
        assert data["status"] == "non_traite"
