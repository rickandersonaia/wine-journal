from flask import url_for


class TestStaticPages(object):
    def test_home_page(self, client):
        """ Home static_pages should respond with a success 200. """
        response = client.get(url_for('static_pages.home'))
        assert response.status_code == 200

    # def test_terms_page(self, client):
    #     """ Terms static_pages should respond with a success 200. """
    #     response = client.get(url_for('static_pages.terms'))
    #     assert response.status_code == 200
    #
    # def test_privacy_page(self, client):
    #     """ Privacy static_pages should respond with a success 200. """
    #     response = client.get(url_for('static_pages.privacy'))
    #     assert response.status_code == 200
