from app import create_app


def test_app_creation():
    app = create_app()
    assert app is not None


def test_auth_register_login(tmp_path):
    app = create_app()
    client = app.test_client()
    resp = client.post('/api/auth/register', json={'email': 'a@b.c', 'password': 'secret'})
    assert resp.status_code == 200
    resp = client.post('/api/auth/login', json={'email': 'a@b.c', 'password': 'secret'})
    assert resp.status_code == 200
    assert 'token' in resp.get_json()


def test_upload_qa(tmp_path):
    app = create_app()
    client = app.test_client()
    # create temp file
    p = tmp_path / 'note.txt'
    p.write_text('Indian Penal Code section 420 deals with cheating')
    with open(p, 'rb') as f:
        resp = client.post('/api/upload/qa', data={'file': f, 'query': 'What section talks about cheating?'} )
    assert resp.status_code == 200
    assert 'answer' in resp.get_json()
