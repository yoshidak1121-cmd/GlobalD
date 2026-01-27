"""Simple tests for the search API endpoint."""
import requests
import json


def test_search_by_maker():
    """Test searching by maker name."""
    response = requests.get("http://localhost:8000/api/search?q=Makino")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    for result in results:
        assert result["maker"] == "Makino"
    print("✓ Search by maker test passed")


def test_search_by_country():
    """Test searching by country."""
    response = requests.get("http://localhost:8000/api/search?q=Japan")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 3
    for result in results:
        assert result["install_country"] == "Japan"
    print("✓ Search by country test passed")


def test_search_by_serial():
    """Test searching by serial number."""
    response = requests.get("http://localhost:8000/api/search?q=SN-2024-001")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["machine_serial"] == "SN-2024-001"
    print("✓ Search by serial test passed")


def test_search_by_nc_model():
    """Test searching by NC model."""
    response = requests.get("http://localhost:8000/api/search?q=FANUC")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 4
    for result in results:
        assert "FANUC" in result["nc_model"]
    print("✓ Search by NC model test passed")


def test_search_no_results():
    """Test searching with no results."""
    response = requests.get("http://localhost:8000/api/search?q=nonexistent")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 0
    print("✓ Search with no results test passed")


def test_search_empty_query():
    """Test searching with empty query."""
    response = requests.get("http://localhost:8000/api/search?q=")
    assert response.status_code == 422  # Validation error
    print("✓ Empty query validation test passed")


def test_health_endpoint():
    """Test health check endpoint."""
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✓ Health check test passed")


def test_root_endpoint():
    """Test root endpoint."""
    response = requests.get("http://localhost:8000/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    print("✓ Root endpoint test passed")


if __name__ == "__main__":
    print("Running API tests...\n")
    
    try:
        test_health_endpoint()
        test_root_endpoint()
        test_search_by_maker()
        test_search_by_country()
        test_search_by_serial()
        test_search_by_nc_model()
        test_search_no_results()
        test_search_empty_query()
        
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Connection error: {e}")
        print("Make sure the server is running: uvicorn main:app --reload")
        exit(1)
