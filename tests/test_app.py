from fastapi import status

def test_root_redirect(client):
    """Test that root endpoint redirects to index.html"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.url.path == "/static/index.html"

def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == status.HTTP_200_OK
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0

def test_signup_for_activity(client):
    """Test signing up for an activity"""
    activity_name = "Chess Club"
    email = "test@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

def test_signup_duplicate(client):
    """Test that a student cannot sign up twice for the same activity"""
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    
    # First signup should succeed
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == status.HTTP_200_OK
    
    # Second signup should fail
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Activity not found" in response.json()["detail"]

def test_unregister_from_activity(client):
    """Test unregistering from an activity"""
    # First, sign up for an activity
    activity_name = "Chess Club"
    email = "unregister@mergington.edu"
    
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Then unregister
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

def test_unregister_not_registered(client):
    """Test unregistering when not registered"""
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not registered" in response.json()["detail"]

def test_unregister_nonexistent_activity(client):
    """Test unregistering from a non-existent activity"""
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Activity not found" in response.json()["detail"]