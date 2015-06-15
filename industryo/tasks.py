from background_task import background
from django.contrib.auth.models import User
from nodes.models import Node


@background(schedule=5)
def create_node():
    user = User.objects.get(id=4)
    Node.objects.create(post='ye time created node hai', user=user, category='F')