def test_signup_successfully_adds_student(client):
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown Club/signup", params={"email": "x@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_student(client):
    duplicate_email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": duplicate_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_400_when_activity_is_full(client):
    full_activity = "Math Olympiad"

    # Math Olympiad starts with two participants and maxes at 12.
    for i in range(10):
        email = f"student{i}@mergington.edu"
        fill_response = client.post(f"/activities/{full_activity}/signup", params={"email": email})
        assert fill_response.status_code == 200

    overflow_response = client.post(
        f"/activities/{full_activity}/signup", params={"email": "overflow@mergington.edu"}
    )

    assert overflow_response.status_code == 400
    assert overflow_response.json()["detail"] == "Activity is full"


def test_signup_requires_email_query_param(client):
    response = client.post("/activities/Chess Club/signup")

    assert response.status_code == 422
