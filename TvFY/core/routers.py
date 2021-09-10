from rest_framework.routers import DefaultRouter


class RestRouter(DefaultRouter):
    include_root_view = False
