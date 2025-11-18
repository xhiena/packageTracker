import pytest
from app.models.package import Package


class TestAddPackage:
    """Test adding a package endpoint."""
    
    def test_add_package_authenticated(self, authenticated_client, test_user, db_session):
        """Test adding a package as authenticated user."""
        response = authenticated_client.post(
            "/api/packages",
            json={
                "tracking_number": "TEST123456",
                "carrier_code": "correos",
                "nickname": "My Package"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Verify response structure
        assert data["tracking_number"] == "TEST123456"
        assert data["carrier_code"] == "correos"
        assert data["nickname"] == "My Package"
        assert data["user_id"] == test_user.id
        assert "id" in data
        assert "status_data" in data
        
        # Verify status_data has tracking information
        status_data = data["status_data"]
        assert status_data["carrier"] == "correos"
        assert status_data["tracking_number"] == "TEST123456"
        assert "events" in status_data
        
        # Verify package exists in database
        package = db_session.query(Package).filter(Package.id == data["id"]).first()
        assert package is not None
        assert package.tracking_number == "TEST123456"
        assert package.carrier_code == "correos"
        assert package.user_id == test_user.id
    
    def test_add_package_without_nickname(self, authenticated_client, test_user):
        """Test adding a package without nickname."""
        response = authenticated_client.post(
            "/api/packages",
            json={
                "tracking_number": "TEST999",
                "carrier_code": "gls"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["tracking_number"] == "TEST999"
        assert data["carrier_code"] == "gls"
        assert data["nickname"] is None
    
    def test_add_package_unauthenticated(self, client):
        """Test adding a package without authentication fails."""
        response = client.post(
            "/api/packages",
            json={
                "tracking_number": "TEST123",
                "carrier_code": "correos"
            }
        )
        
        assert response.status_code == 401
    
    def test_add_package_unsupported_carrier(self, authenticated_client):
        """Test adding a package with unsupported carrier fails."""
        response = authenticated_client.post(
            "/api/packages",
            json={
                "tracking_number": "TEST123",
                "carrier_code": "unsupported"
            }
        )
        
        assert response.status_code == 400
        assert "unsupported" in response.json()["detail"].lower()
    
    def test_add_package_different_carriers(self, authenticated_client, test_user):
        """Test adding packages with different carriers."""
        carriers = ["correos", "gls", "seur"]
        
        for carrier in carriers:
            response = authenticated_client.post(
                "/api/packages",
                json={
                    "tracking_number": f"TEST_{carrier.upper()}",
                    "carrier_code": carrier
                }
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["carrier_code"] == carrier
            assert data["status_data"]["carrier"] == carrier


class TestListPackages:
    """Test listing packages endpoint."""
    
    def test_list_packages_empty(self, authenticated_client):
        """Test listing packages when user has no packages."""
        response = authenticated_client.get("/api/packages")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_list_packages_with_data(self, authenticated_client, test_user, db_session):
        """Test listing packages when user has packages."""
        # Create packages
        package1 = Package(
            user_id=test_user.id,
            tracking_number="TEST001",
            carrier_code="correos",
            nickname="Package 1",
            status_data={"status": "in_transit"}
        )
        package2 = Package(
            user_id=test_user.id,
            tracking_number="TEST002",
            carrier_code="gls",
            nickname="Package 2",
            status_data={"status": "delivered"}
        )
        db_session.add(package1)
        db_session.add(package2)
        db_session.commit()
        
        response = authenticated_client.get("/api/packages")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        
        # Verify package data
        tracking_numbers = [p["tracking_number"] for p in data]
        assert "TEST001" in tracking_numbers
        assert "TEST002" in tracking_numbers
    
    def test_list_packages_only_user_packages(self, authenticated_client, test_user, db_session):
        """Test that user only sees their own packages."""
        from app.models.user import User
        
        # Create another user
        other_user = User(
            email="other@example.com",
            hashed_password="hash",
            full_name="Other User"
        )
        db_session.add(other_user)
        db_session.commit()
        
        # Create packages for both users
        package1 = Package(
            user_id=test_user.id,
            tracking_number="TEST_USER1",
            carrier_code="correos"
        )
        package2 = Package(
            user_id=other_user.id,
            tracking_number="TEST_OTHER",
            carrier_code="gls"
        )
        db_session.add(package1)
        db_session.add(package2)
        db_session.commit()
        
        response = authenticated_client.get("/api/packages")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["tracking_number"] == "TEST_USER1"
    
    def test_list_packages_unauthenticated(self, client):
        """Test listing packages without authentication fails."""
        response = client.get("/api/packages")
        
        assert response.status_code == 401


class TestGetPackageStatus:
    """Test getting package status endpoint."""
    
    def test_get_package_status_success(self, authenticated_client, test_user, db_session):
        """Test getting status for a package."""
        # Create a package
        package = Package(
            user_id=test_user.id,
            tracking_number="TEST123",
            carrier_code="correos",
            nickname="Test Package",
            status_data={"status": "old_status"}
        )
        db_session.add(package)
        db_session.commit()
        db_session.refresh(package)
        
        response = authenticated_client.get(f"/api/packages/{package.id}/status")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response
        assert data["id"] == package.id
        assert data["tracking_number"] == "TEST123"
        assert data["carrier_code"] == "correos"
        
        # Verify status was updated
        assert "status_data" in data
        assert data["status_data"]["carrier"] == "correos"
        assert "events" in data["status_data"]
    
    def test_get_package_status_updates_database(self, authenticated_client, test_user, db_session):
        """Test that getting status updates the database."""
        # Create a package with old status
        package = Package(
            user_id=test_user.id,
            tracking_number="TEST456",
            carrier_code="gls",
            status_data={"status": "old"}
        )
        db_session.add(package)
        db_session.commit()
        package_id = package.id
        
        # Get status
        response = authenticated_client.get(f"/api/packages/{package_id}/status")
        assert response.status_code == 200
        
        # Verify database was updated
        db_session.expire_all()  # Force reload from database
        updated_package = db_session.query(Package).filter(Package.id == package_id).first()
        assert updated_package.status_data["carrier"] == "gls"
        assert "events" in updated_package.status_data
    
    def test_get_package_status_not_found(self, authenticated_client):
        """Test getting status for non-existent package."""
        response = authenticated_client.get("/api/packages/99999/status")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_package_status_wrong_user(self, authenticated_client, db_session):
        """Test getting status for another user's package."""
        from app.models.user import User
        
        # Create another user
        other_user = User(
            email="other@example.com",
            hashed_password="hash",
            full_name="Other User"
        )
        db_session.add(other_user)
        db_session.commit()
        
        # Create package for other user
        package = Package(
            user_id=other_user.id,
            tracking_number="TEST999",
            carrier_code="correos"
        )
        db_session.add(package)
        db_session.commit()
        
        # Try to access it
        response = authenticated_client.get(f"/api/packages/{package.id}/status")
        
        assert response.status_code == 404
    
    def test_get_package_status_unauthenticated(self, client):
        """Test getting package status without authentication fails."""
        response = client.get("/api/packages/1/status")
        
        assert response.status_code == 401
    
    def test_get_package_status_invalid_carrier(self, authenticated_client, test_user, db_session):
        """Test getting status for package with invalid carrier."""
        # Create package with invalid carrier (should not happen in normal flow)
        package = Package(
            user_id=test_user.id,
            tracking_number="TEST789",
            carrier_code="invalid_carrier",
            status_data={}
        )
        db_session.add(package)
        db_session.commit()
        
        response = authenticated_client.get(f"/api/packages/{package.id}/status")
        
        assert response.status_code == 400


class TestDatabaseInteraction:
    """Test database interactions for package API."""
    
    def test_package_creation_persists(self, authenticated_client, test_user, db_session):
        """Test that package creation persists to database."""
        response = authenticated_client.post(
            "/api/packages",
            json={
                "tracking_number": "PERSIST_TEST",
                "carrier_code": "correos",
                "nickname": "Persistence Test"
            }
        )
        
        assert response.status_code == 201
        package_id = response.json()["id"]
        
        # Query database directly
        package = db_session.query(Package).filter(Package.id == package_id).first()
        
        assert package is not None
        assert package.tracking_number == "PERSIST_TEST"
        assert package.carrier_code == "correos"
        assert package.nickname == "Persistence Test"
        assert package.user_id == test_user.id
        assert package.status_data is not None
    
    def test_status_update_persists(self, authenticated_client, test_user, db_session):
        """Test that status update persists to database."""
        # Create package
        package = Package(
            user_id=test_user.id,
            tracking_number="UPDATE_TEST",
            carrier_code="seur",
            status_data={"old": "data"}
        )
        db_session.add(package)
        db_session.commit()
        package_id = package.id
        
        # Update status
        response = authenticated_client.get(f"/api/packages/{package_id}/status")
        assert response.status_code == 200
        
        # Query database in new session
        db_session.expire_all()
        updated_package = db_session.query(Package).filter(Package.id == package_id).first()
        
        # Verify update persisted
        assert updated_package.status_data != {"old": "data"}
        assert updated_package.status_data["carrier"] == "seur"
        assert updated_package.status_data["tracking_number"] == "UPDATE_TEST"
    
    def test_multiple_packages_same_user(self, authenticated_client, test_user, db_session):
        """Test that user can have multiple packages."""
        # Create multiple packages
        for i in range(3):
            response = authenticated_client.post(
                "/api/packages",
                json={
                    "tracking_number": f"MULTI_{i}",
                    "carrier_code": "correos"
                }
            )
            assert response.status_code == 201
        
        # Verify all packages exist in database
        packages = db_session.query(Package).filter(Package.user_id == test_user.id).all()
        assert len(packages) == 3
        
        tracking_numbers = [p.tracking_number for p in packages]
        assert "MULTI_0" in tracking_numbers
        assert "MULTI_1" in tracking_numbers
        assert "MULTI_2" in tracking_numbers
