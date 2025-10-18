"""
End-to-end tests for Health endpoints
"""
import pytest


@pytest.mark.e2e
class TestHealthAPI:
    """Test suite for health check endpoints"""
    
    def test_health_check(self, client):
        """Test /health endpoint"""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "lorcana-card-manager"
    
    def test_root_endpoint(self, client):
        """Test root / endpoint"""
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert data["docs"] == "/docs"
