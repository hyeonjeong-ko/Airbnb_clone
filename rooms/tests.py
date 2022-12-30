from rest_framework.test import APITestCase
from django.test import TestCase
from . import models
from users.models import User

# test실행시마다 완전히 새로운 빈 데이터베이스 생성하고 끝나면 데이터베이스는 파괴됨


class TestAmenities(APITestCase):

    URL = "/api/v1/rooms/amenities/"
    NAME = "Amenity Test"
    DESC = "Amenity Des"

    # 다른 모든 테스트들 실행되기 전 수행됨
    def setUp(self):  # Amenity 하나 생성됨
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200",
        )

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESC)

    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity desc."

        response = self.client.post(
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_description,
            },
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )

        self.assertEqual(
            data["name"],
            new_amenity_name,
        )
        self.assertEqual(
            data["description"],
            new_amenity_description,
        )

        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

        # print(response.json())


# 한번 돌면 롤백됨
class TestAmenity(APITestCase):

    URL = "/api/v1/rooms/amenities/1"
    NAME = "Test Amenity"
    DESC = "Test Desc"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    # test1 ) URL로 이동했는데 해당 Amenity가 없을때
    # 없는 데이터보냈을때 -> notFound
    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2")
        self.assertEqual(response.status_code, 404)

    # test2 ) Amenity가 존재할때
    def test_get_amenity(self):

        # 존재하는 데이터 보냈을때
        response = self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["name"],
            self.NAME,
        )

        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_put_amenity(self):
        # your code challenge

        # ** put **
        # serializer가 유효해서 유저가 Amenity업데이트를 할 수 있는 경우
        # serializer가 유효하지 않을때

        put_amenity_name = "New Amenity"
        put_amenity_description = "New Amenity desc."

        response = self.client.put(
            self.URL,
            data={
                "name": put_amenity_name,
                "description": put_amenity_description,
            },
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )

        self.assertEqual(
            data["name"],
            put_amenity_name,
        )

        self.assertEqual(
            data["description"],
            put_amenity_description,
        )

        response = self.client.put(self.URL)
        data = response.json()
        self.assertIn("name", data)

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 204)  # no content...


class TestRooms(APITestCase):
    def setUp(self):
        # 권한있을때
        # User object 생성,로그인
        user = User.objects.create(
            username="test",
        )

        user.set_password("123")
        user.save()
        self.user = user  # 유저를 class 내부에 저장해서 class 안에있는 method에서 접근 가능할 수 있게함

    def test_create_room(self):

        # 권한없을때 에러
        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 401)

        # self.client.login(
        #     username="test",
        #     password="123",
        # )

        self.client.force_login(self.user)

        response = self.client.post("/api/v1/rooms/")
        print(response.json())
