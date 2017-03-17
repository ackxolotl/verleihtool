from depot.models import Depot, Item
from verleihtool.test import ClientTestCase


class DepotDetailTestCase(ClientTestCase):

    def setUp(self):
        super(DepotDetailTestCase, self).setUp()

        self.depot = Depot.objects.create(
            name='My Depot'
        )

        self.inactive_depot = Depot.objects.create(
            name='My Inactive Depot',
            active=False
        )

    def test_show_depot_name(self):
        response = self.as_guest.get('/depots/%d/' % self.depot.id)
        self.assertSuccess(response, 'depot/detail.html')
        self.assertContains(response, 'My Depot')

    def test_inactive_depot_not_found(self):
        response = self.as_guest.get('/depots/%d/' % self.inactive_depot.id)
        self.assertEqual(response.status_code, 404)

    def test_inactive_depot_found_when_superuser(self):
        response = self.as_superuser.get('/depots/%d/' % self.inactive_depot.id)
        self.assertSuccess(response, 'depot/detail.html')
        self.assertContains(response, 'My Inactive Depot')