import unittest

from app import create_app,db
from app.models import Room, Thing
from config import TestConfig

JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9FRkNRekk0TmpSRFFqVXhRVVUyT0RjMFJVSkNORVEzTTBVMU5USTJRVGcwUVRjME9EY3dPQSJ9.eyJpc3MiOiJodHRwczovL2Nhb2thaS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU4ZTJjMDQxZjFiOTgwYzBiM2YyMjlhIiwiYXVkIjpbImhvbWVfYXV0b21hdGlvbiIsImh0dHBzOi8vY2Fva2FpLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODY0Mzg4MzcsImV4cCI6MTU4NjUyNTIzNywiYXpwIjoiVTA4U0o3VjRubHVJbHo2Y2NiWGhoR2ZUQjhjU2oxRzYiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnJvb21zIiwiZGVsZXRlOnRoaW5ncyIsImZsaXA6dGhpbmdzIl19.bw5MlZLFGifoxwcJKWz_1_7Sv-_He6-NPdPC6FmjVDqU-lpqVA0PMi1BekIeilDq6889JSMDKBtRLecPKVv3cWU1DoH-PMvoRIJJOslVADOsqBxk8AQ09jM4UVglDrPL30zjs0_fD09ybrjz-k6eZgB-PKVRslMYtNJm07-cW6SMdYWJAGb8rG4fiHOxTvQ_EiRqXWtRWOzm3H7GNWZwhAUICAwu9mi8oiz9hGLTiZxy-fDnL96g03mL84T1DXEmbmtG5NPcExkCyH3MWbsCd-kRmx2XGWNcQYU_Hd40zIen8aC5gYUvv2UdY4EiXsfLyfcR1UEoYzUJa_3enRm6CQ'

HEADERS = {
    'content-type': 'application/json',
    'accept': '*/*',
    'Authorization': 'Bearer ' + JWT
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
        # print(self.app.config['SQLALCHEMY_DATABASE_URI'])
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