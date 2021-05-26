from http import HTTPStatus

from django.test import TestCase


class Test(TestCase):
    def test_index_page_are_loading(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(resp, 'create_instance.html')

    def test_can_create_anime(self):
        data = {
            'anime_name': 'Fullmetal Alchemist',
            'rating': '10/10',
            'watching': 'Finished',
        }
        resp = self.client.post('/', data=data, follow=True)

        self.assertEqual(resp.status_code, HTTPStatus.OK)
        for d in data.values():
            self.assertContains(resp, d)
