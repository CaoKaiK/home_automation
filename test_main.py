import unittest

from app import create_app,db
from app.models import Room, Thing
from config import TestConfig


HEADERS = {
    'content-type': 'application/json',
    'accept': '*/*'
}


class ModelCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = create_app(TestConfig)
        print(self.app.config['SQLALCHEMY_DATABASE_URI'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Test Instances
        room1 = Room(name='Room 1')
        db.session.add(room1)
        room2 = Room(name='Room 2')
        db.session.add(room2)
        thing1 = Thing(name='Thing 1', location=room1)
        db.session.add(thing1)
        thing2 = Thing(name='Thing 2', location=room2)
        db.session.add(thing2)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        pass

    
    def test_pass_health_accept(self):
        headers = {'accept': '*/*'}
        r = self.client.get('api/status', headers=headers)
        self.assertEqual(r.status_code, 200)
    
    def test_fail_health_accept(self):
        headers = {'accept': 'xml'}
        r = self.client.get('api/status', headers=headers)
        self.assertEqual(r.status_code, 415)
    
    def test_pass_health_content(self):
        headers = {
            'content-type': 'application/json',
            'accept': '*/*'
            }
        r = self.client.get('api/status', headers=headers)
        self.assertEqual(r.status_code, 200)
    
    def test_fail_health_content(self):
        headers = {
            'content-type': 'application/json',
            'accept': '*/*'
        }
        r = self.client.post('api/status', headers=headers)
        self.assertEqual(r.status_code, 200)
    
    def test_fail_health_method(self):
        headers = {
            'accept': '*/*'
        }
        r = self.client.patch('api/status', headers=headers)
        self.assertEqual(r.status_code, 405)
    
    def test_empty_rooms(self):
        r = self.client.get('api/rooms', headers=HEADERS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['result'][0]['name'], 'Room 1')
    
    def test_create_room(self):
        json = {'name': 'Room 3'}
        r = self.client.post('api/rooms', headers=HEADERS, json=json)
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(r.get_json()['result'], [])
        self.assertEqual(r.get_json()['result']['name'], 'Room 3')

    def test_duplicate_room(self):
        json = {'name': 'Room 1'}
        r = self.client.post('api/rooms', headers=HEADERS, json=json)
        self.assertEqual(r.status_code, 409)
    
    def test_rename_name(self):
        json = {'name': 'Renamed Room'}
        r = self.client.patch('api/rooms/1', headers=HEADERS, json=json)
        self.assertEqual(r.status_code, 200)

    def test_single_room(self):
        r = self.client.get('api/rooms/1', headers=HEADERS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['result']['name'], 'Room 1')

    def test_out_of_index_room(self):
        r = self.client.get('api/rooms/100', headers=HEADERS)
        self.assertEqual(r.status_code, 404)

    def test_delete_room(self):
        r = self.client.delete('api/rooms/1', headers=HEADERS)
        self.assertEqual(r.status_code, 200)

    def test_delete_404_room(self):
        r = self.client.delete('api/rooms/100', headers=HEADERS)
        self.assertEqual(r.status_code, 404)

    def test_get_things(self):
        r = self.client.get('api/things', headers=HEADERS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['result'][0]['name'], 'Thing 1')

    def test_create_thing(self):
        json = { 'name': 'Thing 3', 'room_id': 1}
        r = self.client.post('api/things', headers=HEADERS, json=json)
        self.assertEqual(r.status_code, 200)

    def test_fail_creating_thing(self):
        json = { 'name': 'Thing 4'}
        r = self.client.post('api/things', headers=HEADERS, json=json)
        self.assertEqual(r.status_code, 400)
    
    def test_get_thing(self):
        r = self.client.get('api/things/1', headers=HEADERS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['result']['name'], 'Thing 1')
    
    def test_get_things_filter(self):
        r = self.client.get('api/things?room=2', headers=HEADERS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['result'][0]['name'], 'Thing 2')

    def test_rename_thing(self):
        json = {'name': 'New Name'}
        r = self.client.patch('api/things/1', headers=HEADERS, json=json)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['result']['name'], 'New Name')

    def test_flip_a_thing(self):
        r = self.client.patch('api/things/1/flip', headers=HEADERS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['result']['status'], True)


if __name__ == '__main__':
    unittest.main()