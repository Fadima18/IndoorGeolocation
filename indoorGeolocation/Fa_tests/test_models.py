from django.test import TestCase

from indoorGeolocation.models import Device, Material, Node, Person, Position

class TestModel(TestCase):

    def test_should_create_device(self):
        device = Device(device_id="1233", name="dev1")
        device.save()
        self.assertEqual(str(device), 'dev1')
    
    def test_should_create_position(self):
        device = Device(device_id="1233", name="dev1")
        device.save()
        position = Position(x=2, y=3, device=device )
        position.save()
        self.assertEqual(str(position), 'dev1')

    def test_should_create_node(self):
        device = Device(device_id="1233", name="dev1")
        device.save()
        node = Node(device=device)
        node.save()
        self.assertEqual(str(node), 'dev1')
    def test_should_create_person(self):
        person = Person(firstName="Ndeye", lastName="Dieng")
        person.save()
        self.assertEqual(str(person), 'Ndeye')
    
    def test_should_create_Material(self):
        material = Material(name="airpods")
        material.save()
        self.assertEqual(str(material), 'airpods')