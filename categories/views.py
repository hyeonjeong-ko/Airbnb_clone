from django.shortcuts import render
from .models import Category

# from .models import JsonResponse
# from django.core import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer  # 번역기
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# class Categories(APIView):
#     def get(self, request):
#         all_categories = Category.objects.all()
#         serializer = CategorySerializer(all_categories, many=True)  # obj -> json
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             new_category = serializer.save()  # serializer.create 호출

#             return Response(
#                 CategorySerializer(new_category).data,
#             )
#         else:
#             serializer.errors
#         return Response({"created": True})


# class CategoryDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             raise NotFound

#     def get(self, request, pk):
#         serializer = CategorySerializer(self.get_object(pk))
#         return Response(serializer.data)

#     def put(self, request, pk):
#         serializer = CategorySerializer(
#             self.get_object(pk),  # database로부터 가져온 cate
#             data=request.data,  # 사용자의 입력데이터
#             partial=True,  # kind만검증
#         )
#         if serializer.is_valid():
#             updated_category = serializer.save()  # db+userdata -> update method
#             return Response(CategorySerializer(updated_category).data)

#     def delete(self, request, pk):
#         self.get_object(pk).delete()
#         return Response(status=HTTP_204_NO_CONTENT)


# @api_view(["GET", "PUT", "DELETE"])
# def category(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         raise NotFound

#     if request.method == "GET":
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#     elif request.method == "PUT":  # 갱신
#         serializer = CategorySerializer(
#             category,  # database로부터 가져온 cate
#             data=request.data,  # 사용자의 입력데이터
#             partial=True,  # kind만검증
#         )
#         if serializer.is_valid():
#             updated_category = serializer.save()  # db+userdata -> update method
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.error_messages)

#     elif request.method == "DELETE":
#         category.delete()
#         return Response(status=HTTP_204_NO_CONTENT)
