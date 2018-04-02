"""
Test suite for xboxvoting app

Author: Nick Stevens <nickastevens@yahoo.com>
"""

from django.test import TestCase
from xboxvoting.models import Game
from django.utils import timezone


class XboxTest(TestCase):
    fixtures = ['games.json']

    def setUp(self):
        pass

    def test_basic_index(self):
        ''' Tests a simple call to the main index '''
        response = self.client.get('/xbox/')
        self.assertEqual(response.status_code, 200)

    def test_vote_valid(self):
        ''' Tests that casting a valid vote increases the DB count by 1 '''
        start_votes = Game.objects.get(pk=1).votes
        response = self.client.get('/xbox/1/vote/')
        self.assertRedirects(response, '/xbox/?s=voted')
        self.assertEqual(Game.objects.get(pk=1).votes, start_votes + 1)

    def test_vote_invalid(self):
        ''' Tests that browsing to an invalid voting ID gives a 404 '''
        # ID 999 does not exist in fixture data set
        response = self.client.get('/xbox/999/vote/')
        self.assertEqual(response.status_code, 404)

    def test_double_vote(self):
        ''' Tests that client cannot vote twice in one day '''
        response = self.client.get('/xbox/1/vote/')
        self.assertRedirects(response, '/xbox/?s=voted')
        response = self.client.get('/xbox/2/vote/')
        self.assertRedirects(response, '/xbox/?e=voted_twice')

    def test_add_valid(self):
        ''' Tests that adding a valid new game adds the new title to the DB '''
        exist_pre = Game.objects.filter(title__exact='XBoxTest').exists()
        response = self.client.post('/xbox/add/', {'new_title': 'XBoxTest'})
        self.assertRedirects(response, '/xbox/?s=added')
        exist_post = Game.objects.filter(title__exact='XboxTest').exists()
        self.assertFalse(exist_pre)
        self.assertFalse(exist_post)

    def test_add_empty(self):
        ''' Tests that calling 'add' with an empty new_title returns error '''
        response = self.client.post('/xbox/add/', {'new_title': ''})
        self.assertRedirects(response, '/xbox/?e=empty_title')
        self.assertFalse(Game.objects.filter(title__exact='').exists())

    def test_add_duplicate(self):
        ''' Tests that adding a duplicate game returns error '''
        # Bioshock is pre-added from fixture
        response = self.client.post('/xbox/add/', {'new_title': 'Bioshock'})
        self.assertRedirects(response, '/xbox/?e=dup_game')
        self.assertEqual(
            Game.objects.filter(title__exact='Bioshock').count(), 1)

    def test_add_too_long(self):
        ''' Tests that adding title > 255 characters returns error '''
        title = 'f' * 256
        response = self.client.post('/xbox/add/',
            {'new_title': title})
        self.assertRedirects(response, '/xbox/?e=title_too_long')
        self.assertFalse(Game.objects.filter(title__exact=(title)).exists())

    def test_double_add(self):
        ''' Tests that client cannot add more than one game in a day '''
        self.assertFalse(Game.objects.filter(title__exact='XBoxTest').exists())
        response = self.client.post('/xbox/add/', {'new_title': 'XBoxTest'})
        self.assertRedirects(response, '/xbox/?s=added')
        self.assertTrue(Game.objects.filter(title__exact='XBoxTest').exists())
        response = self.client.post('/xbox/add/', {'new_title': 'NewGame'})
        self.assertRedirects(response, '/xbox/?e=added_twice')
        self.assertFalse(Game.objects.filter(title__exact='NewGame').exists())

    def test_vote_then_add(self):
        ''' Tests that client cannot vote and then add a game in one day '''
        start_votes = Game.objects.get(pk=1).votes
        response = self.client.get('/xbox/1/vote/')
        self.assertRedirects(response, '/xbox/?s=voted')
        self.assertEqual(Game.objects.get(pk=1).votes, start_votes + 1)
        response = self.client.post('/xbox/add/', {'new_title': 'XBoxTest'})
        self.assertRedirects(response, '/xbox/?e=vote_then_add')
        self.assertEqual(Game.objects.get(pk=1).votes, start_votes + 1)

    def test_add_then_vote(self):
        ''' Tests that client cannot add a game and then vote in one day '''
        response = self.client.post('/xbox/add/', {'new_title': 'XBoxTest'})
        self.assertRedirects(response, '/xbox/?s=added')
        response = self.client.get('/xbox/1/vote/')
        self.assertRedirects(response, '/xbox/?e=add_then_vote')

    def test_vote_tomorrow(self):
        ''' Tests that client can vote today and vote again tomorrow '''
        start_votes = Game.objects.get(pk=1).votes
        response = self.client.get('/xbox/1/vote/')
        self.assertRedirects(response, '/xbox/?s=voted')
        self.assertEqual(Game.objects.get(pk=1).votes, start_votes + 1)
        self._install_time_stub(self._get_tomorrow())
        response = self.client.get('/xbox/1/vote/')
        self.assertRedirects(response, '/xbox/?s=voted')
        self.assertEqual(Game.objects.get(pk=1).votes, start_votes + 2)
        self._uninstall_time_stub()

    def test_saturday_vote(self):
        ''' Tests that client cannot vote on Saturday '''
        self._install_time_stub(self._get_next_saturday())
        response = self.client.get('/xbox/1/vote/')
        self.assertRedirects(response, '/xbox/?e=weekend')
        self._uninstall_time_stub()

    def test_sunday_vote(self):
        ''' Tests that client cannot vote on Sunday '''
        self._install_time_stub(self._get_next_sunday())
        response = self.client.get('/xbox/1/vote/')
        self.assertRedirects(response, '/xbox/?e=weekend')
        self._uninstall_time_stub()

    def test_saturday_add(self):
        ''' Tests that client cannot add a game on Saturday '''
        self._install_time_stub(self._get_next_saturday())
        response = self.client.post('/xbox/add/', {'new_title': 'TestGame'})
        self.assertRedirects(response, '/xbox/?e=weekend')
        self._uninstall_time_stub()

    def test_sunday_add(self):
        ''' Tests that client cannot add a game on Sunday '''
        self._install_time_stub(self._get_next_sunday())
        response = self.client.post('/xbox/add/', {'new_title': 'TestGame'})
        self.assertRedirects(response, '/xbox/?e=weekend')
        self._uninstall_time_stub()

    def test_manage(self):
        ''' Tests a simple call to the manage page '''
        response = self.client.get('/xbox/manage.htm')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/xbox/manage.html')
        self.assertEqual(response.status_code, 200)

    def test_mark_owned(self):
        ''' Tests that an unowned game can be marked as owned '''
        self.assertFalse(Game.objects.get(pk=1).owned)
        response = self.client.get('/xbox/1/own/')
        self.assertRedirects(response, '/xbox/?s=owned')
        self.assertTrue(Game.objects.get(pk=1).owned)

    def test_mark_owned_twice(self):
        ''' Tests that no error is thrown if a game already owned is
        marked as owned a second time, but no success message is given
        either
        '''
        Game.objects.get(pk=1).set_owned()
        self.assertTrue(Game.objects.get(pk=1).owned)
        response = self.client.get('/xbox/1/own/')
        self.assertRedirects(response, '/xbox/')
        self.assertTrue(Game.objects.get(pk=1).owned)

    def test_owned_nonexistant(self):
        ''' Tests that marking a non-existant game as owned gives a 404 '''
        response = self.client.get('/xbox/999/own/')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Game.objects.get(pk=1).owned)

    def _install_time_stub(self, timestamp):
        ''' Installs a stub time method to override default timezone.now() '''
        datetime.set_static_time(timestamp)
        self.django_now = timezone.now
        timezone.now = datetime.now

    def _uninstall_time_stub(self):
        ''' Removes time stub method '''
        timezone.now = self.django_now

    def _get_tomorrow(self):
        now = timezone.now()
        return now + timezone.timedelta(1)

    def _get_next_saturday(self):
        now = timezone.now()
        # Determine number of days until Saturday (5)
        days = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1, 5: 0, 6: 6}.get(now.weekday())
        return now + timezone.timedelta(days)

    def _get_next_sunday(self):
        now = timezone.now()
        # Determine number of days until Sunday (6)
        days = 6 - now.weekday()
        return now + timezone.timedelta(days)


class datetime(timezone.datetime):
    ''' Monkey patch class to override default timezone.now() calls and
    replace the datetimes with datetimes of our choosing

    Usage:
        self._install_time_stub(<datetime>)
        ...
        self._uninstall_time_stub()
    '''

    @classmethod
    def set_static_time(cls, static_time):
        cls.static_time = static_time

    @classmethod
    def now(cls, timezone=None):
        return cls.static_time
