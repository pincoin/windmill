from django.forms import ModelChoiceField


class GolfClubChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return '{}'.format(obj.title)
