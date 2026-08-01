def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert len(payload) == 9


def test_get_activities_has_expected_schema(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()

    for activity_name, activity in payload.items():
        assert activity_name
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)
