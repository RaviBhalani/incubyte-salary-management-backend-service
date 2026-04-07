def assert_error_response(response, expected_status_code):
    assert response.status_code == expected_status_code
    assert response.data["data"] is None
    assert response.data["message"] is None
    assert response.data["error_list"]
