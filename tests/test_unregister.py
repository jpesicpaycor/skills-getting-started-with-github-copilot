def test_unregister_successfully_removes_student(client):
    email = "michael@mergington.edu"
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown Club/participants", params={"email": "x@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_student_not_enrolled(client):
    response = client.delete(
        "/activities/Chess Club/participants", params={"email": "notenrolled@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_requires_email_query_param(client):
    response = client.delete("/activities/Chess Club/participants")

    assert response.status_code == 422
