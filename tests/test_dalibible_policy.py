from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_bible_policy_is_discoverable_and_describes_real_data_flows():
    index = client.get('/privacy')
    assert 'href="/privacy/dalibible"' in index.text
    response = client.get('/privacy/dalibible')
    assert response.status_code == 200
    for text in ('Dalifin LLC', 'DaliBible', 'October 30, 2026',
                 'religious beliefs', 'Google or Apple password',
                 'AI service providers', 'synchronization revisions',
                 '/account-deletion/dalibible', '/terms/dalibible'):
        assert text in response.text


def test_deletion_page_offers_public_request_without_app_or_password():
    response = client.get('/account-deletion/dalibible')
    assert response.status_code == 200
    for text in ('without installing or signing in',
                 'mailto:gli@dalifin.com?subject=DaliBible%20account%20and%20data%20deletion%20request',
                 'Do not email your password', 'manual follow-up',
                 'does not mean all data has already been removed',
                 'More &gt; Configure', 'Set or reset Dali password',
                 'Bible data removed', 'shared Dali account'):
        assert text in response.text
    assert '<form' not in response.text  # No password/email collection on the public site.


def test_terms_explain_allowance_and_safety_without_starting_subscription():
    response = client.get('/terms/dalibible')
    assert response.status_code == 200
    for text in ('10 AI requests per account per UTC calendar month',
                 'does not by itself start a paid subscription',
                 'reporting controls', '/privacy/dalibible', '/account-deletion/dalibible'):
        assert text in response.text


def test_legal_routes_support_store_head_checks():
    for path in ('/privacy/dalibible', '/terms/dalibible', '/account-deletion/dalibible'):
        response = client.head(path)
        assert response.status_code == 200
        assert response.headers['content-type'].startswith('text/html')
        assert not response.content
