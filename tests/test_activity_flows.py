def test_fill_activity_then_free_spot_then_allow_new_signup(client):
    activity_name = "Math Olympiad"

    # Fill remaining 10 slots (starts with 2 participants, max is 12).
    for i in range(10):
        email = f"fill{i}@mergington.edu"
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == 200

    full_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": "overflow@mergington.edu"}
    )
    assert full_response.status_code == 400

    remove_response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": "fill0@mergington.edu"}
    )
    assert remove_response.status_code == 200

    retry_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": "overflow@mergington.edu"}
    )
    assert retry_response.status_code == 200


def test_unregister_then_reregister_same_student(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    remove_response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    assert remove_response.status_code == 200

    add_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert add_response.status_code == 200

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert participants.count(email) == 1


def test_operations_on_one_activity_do_not_change_others(client):
    baseline = client.get("/activities").json()

    client.post("/activities/Art Studio/signup", params={"email": "newartist@mergington.edu"})
    client.delete("/activities/Chess Club/participants", params={"email": "michael@mergington.edu"})

    updated = client.get("/activities").json()

    assert len(updated["Art Studio"]["participants"]) == len(baseline["Art Studio"]["participants"]) + 1
    assert len(updated["Chess Club"]["participants"]) == len(baseline["Chess Club"]["participants"]) - 1
    assert updated["Programming Class"]["participants"] == baseline["Programming Class"]["participants"]
