from django.forms import Form, widgets, fields


class petInfo(Form):
    petName = fields.CharField(max_length=10,)
    petId = fields.CharField(max_length=4)
    gender = fields.CharField(initial='雄性',
    widget=widgets.Select(choices=(('雄性', '雄性'), ('雌性', '雌性'))))
    year = fields.IntegerField(max_value=25, min_value=0)
    kind = fields.CharField(max_length=10)


class PetInfo(Form):
    petName = fields.CharField(max_length=10,)
    petId = fields.CharField(max_length=4)
    gender = fields.CharField(initial='雄性', widget=widgets.Select(choices=(('雄性', '雄性'), ('雌性', '雌性'))))
    year = fields.IntegerField(max_value=25, min_value=0)
    kind = fields.CharField(max_length=10)
