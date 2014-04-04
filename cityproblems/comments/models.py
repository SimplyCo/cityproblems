from django.db import models
from treebeard.mp_tree import MP_Node
from django.contrib.auth import get_user_model

from cityproblems.site.models import Problem


class Comment(MP_Node):
    fk_item = models.ForeignKey(Problem)
    created_by = models.ForeignKey(get_user_model(), null=True)
    created_when = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True)
    node_order_by = ['created_when']

    def have_write_permission(self, user):
        return user.is_authenticated() and (user.is_staff or self.created_by == user)
