from flask import url_for


class TestStaticPages(object):
    def test_category_list_page(self, client):
        """ Home static_pages should respond with a success 200. """
        response = client.get(url_for('categories.list-categories'))
        assert response.status_code == 200

    def test_category_add_new_page(self, client):
        """ Home static_pages should respond with a success 200. """
        response = client.get(url_for('categories.new-category'))
        assert response.status_code == 200
