from fastapi import status


def test_get_supported_carriers(client):
    """Test getting list of supported carriers."""
    response = client.get("/api/packages/carriers")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "carriers" in data
    assert isinstance(data["carriers"], list)
    assert "spain_correos_es" in data["carriers"]
    assert "gls" in data["carriers"]


def test_create_package_without_auth(client):
    """Test creating package without authentication."""
    response = client.post(
        "/api/packages/",
        json={
            "tracking_number": "AB123456789ES",
            "carrier": "spain_correos_es",
            "description": "Test package"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_package_with_auth(client, auth_token):
    """Test creating package with authentication."""
    response = client.post(
        "/api/packages/",
        json={
            "tracking_number": "AB123456789ES",
            "carrier": "spain_correos_es",
            "description": "Test package"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tracking_number"] == "AB123456789ES"
    assert data["carrier"] == "spain_correos_es"
    assert data["description"] == "Test package"
    assert "id" in data


def test_create_package_invalid_carrier(client, auth_token):
    """Test creating package with invalid carrier."""
    response = client.post(
        "/api/packages/",
        json={
            "tracking_number": "123456789",
            "carrier": "invalid_carrier",
            "description": "Test package"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Unsupported carrier" in response.json()["detail"]


def test_create_package_invalid_tracking_number(client, auth_token):
    """Test creating package with invalid tracking number."""
    response = client.post(
        "/api/packages/",
        json={
            "tracking_number": "123",
            "carrier": "spain_correos_es",
            "description": "Test package"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid tracking number format" in response.json()["detail"]


def test_list_packages(client, auth_token):
    """Test listing packages."""
    # Create a package first
    client.post(
        "/api/packages/",
        json={
            "tracking_number": "AB123456789ES",
            "carrier": "spain_correos_es",
            "description": "Test package"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # List packages
    response = client.get(
        "/api/packages/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_package(client, auth_token):
    """Test getting a specific package."""
    # Create a package
    create_response = client.post(
        "/api/packages/",
        json={
            "tracking_number": "AB123456789ES",
            "carrier": "spain_correos_es",
            "description": "Test package"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    package_id = create_response.json()["id"]
    
    # Get the package
    response = client.get(
        f"/api/packages/{package_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == package_id
    assert data["tracking_number"] == "AB123456789ES"


def test_get_nonexistent_package(client, auth_token):
    """Test getting a non-existent package."""
    response = client.get(
        "/api/packages/99999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_package(client, auth_token):
    """Test updating a package."""
    # Create a package
    create_response = client.post(
        "/api/packages/",
        json={
            "tracking_number": "AB123456789ES",
            "carrier": "spain_correos_es",
            "description": "Test package"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    package_id = create_response.json()["id"]
    
    # Update the package
    response = client.put(
        f"/api/packages/{package_id}",
        json={"description": "Updated description"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["description"] == "Updated description"


def test_delete_package(client, auth_token):
    """Test deleting a package."""
    # Create a package
    create_response = client.post(
        "/api/packages/",
        json={
            "tracking_number": "AB123456789ES",
            "carrier": "spain_correos_es",
            "description": "Test package"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    package_id = create_response.json()["id"]
    
    # Delete the package
    response = client.delete(
        f"/api/packages/{package_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's deleted
    get_response = client.get(
        f"/api/packages/{package_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_track_package(client, auth_token):
    """Test tracking a package."""
    from unittest.mock import patch
    
    # Create a package
    create_response = client.post(
        "/api/packages/",
        json={
            "tracking_number": "AB123456789ES",
            "carrier": "spain_correos_es",
            "description": "Test package"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    package_id = create_response.json()["id"]
    
    # Track the package - mock keydelivery.track
    with patch('app.strategies.keydelivery.track') as mock_track:
        mock_track.return_value = {
            "status": "Delivered",
            "location": "Madrid",
            "history": [{"status": "Delivered", "location": "Madrid", "timestamp": "2023-01-01"}],
            "error": None,
            "carrier": "spain_correos_es"
        }
        
        response = client.get(
            f"/api/packages/{package_id}/track",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert "location" in data
        assert "history" in data
        assert isinstance(data["history"], list)

