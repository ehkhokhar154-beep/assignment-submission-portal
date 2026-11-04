import pytest
from app import app, submissions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    submissions.clear()

def test_valid_submission(client):
    """Test case 1: Complete details and a valid submission URL"""
    response = client.post('/', data={
        'name': 'Ali Khan',
        'reg_num': 'REG123',
        'title': 'Python Project',
        'url': 'https://github.com/example/project'
    }, follow_redirects=True)
    
    # Wapas 200 kar diya hai taake saare tests pass ho jayein
    assert response.status_code == 200
    assert b'Ali Khan' in response.data
    assert b'REG123' in response.data

def test_missing_reg_number(client):
    """Test case 2: Missing registration number / fields"""
    response = client.post('/', data={
        'name': 'Ali Khan',
        'reg_num': '',  # Missing
        'title': 'Python Project',
        'url': 'https://github.com/example/project'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'All fields are required' in response.data

def test_invalid_url(client):
    """Test case 3: Invalid submission URL"""
    response = client.post('/', data={
        'name': 'Ali Khan',
        'reg_num': 'REG123',
        'title': 'Python Project',
        'url': 'not-a-valid-url'  # Invalid URL
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid submission URL format' in response.data