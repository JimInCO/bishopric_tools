from ajax_select import register, LookupChannel
from django.db.models import Q

from .models import Member


@register("members")
class TagsLookup(LookupChannel):

    model = Member

    def get_query(self, q, request):
        query = Q(first_name__icontains=q) | Q(last_name__icontains=q)
        return self.model.objects.filter(query).order_by("last_name")

    def format_item_display(self, item):
        return u"<span class='tag'>{}</span>".format(item.full_name)

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.id
