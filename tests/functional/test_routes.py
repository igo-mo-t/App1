from app import app

def test_dealers_page():
    """
    GIVEN 
    WHEN 
    THEN 
    """
    with app.test_client() as test_client:
        response = test_client.get('/dealers')
        assert b"Grifin" in response.data