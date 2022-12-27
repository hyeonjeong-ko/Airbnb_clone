from rest_framework.views import APIView
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer

from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from django.db import transaction


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)  # object->json
        return Response(
            serializer.data,
        )

    def put(self, request, pk):
        amenity = self.get_object(pk)  # 기존data
        serializer = AmenitySerializer(
            amenity,  # 기존 data
            data=request.data,  # update하고싶은 data
            partial=True,
        )

        if serializer.is_valid():
            updated_amenity = serializer.save()  # 사용자입력데이터저장(object)
            return Response(
                AmenitySerializer(updated_amenity).data
            )  # (object->json.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Cateogory is required")  # user가 잘못된 데이터를 전송했을때
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("category not found")

                try:
                    with transaction.atomic():
                        room = serializer.save(  # DB에 즉시반영X
                            owner=request.user,
                            category=category,
                        )

                        amenities = request.data.get("amenities")

                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)  # ManyToMany다루는법...!
                            # raise ParseError(f"Amenity with id {amenity_pk} not found.")
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied

        # 코드 구현과제
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError(detail="Cateogry not found")
            try:
                with transaction.atomic():
                    room = serializer.save(category=category)
                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)

                    return Response(RoomDetailSerializer(room).data)
            except Exception:
                raise ParseError("Amenity not found")

            except Exception as e:
                print(e)
                raise ParseError("amenity not found")

    def delete(self, request, pk):
        room = self.get_object(pk)
        if request.user.is_authenticated:  # 로그인 된 유저인지 확인
            raise NotAuthenticated
        if room.owner != request.user:  # 해당유저가 방의 주인인지 확인
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
