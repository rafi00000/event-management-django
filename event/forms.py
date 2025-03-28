from django import forms
from event.models import Event, Category
from django.contrib.auth.models import Group, Permission

class CreateEventMixin:
    default_classes = "border border-2 border-black p-2 mb-2 rounded-md w-full"
    def apply_form_style(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classes}",
                    'placeholder': f'Enter {field_name}'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field_name}',
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': self.default_classes
                })
            # elif isinstance(field.widget, forms.CheckboxSelectMultiple):
            #     field.widget.attrs.update({
            #         'class': self.default_classes
            #     })
            # elif isinstance(field, forms.ModelChoiceField):  # Apply to ModelChoiceField
            #     field.widget.attrs.update({
            #         'class': f"{self.default_classes} bg-white text-gray-700"
            #     })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classes}",
                    'placeholder': f"Please enter {field_name} here"
                })
            elif isinstance(field.widget, forms.CharField):
                field.widget.attrs.update({
                    'class': f"{self.default_classes}",
                    'placeholder': f"Please enter {field_name} here"
                })
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classes}",
                    'placeholder': f"Please enter {field_name} here"
                })
            


class CreateEventForm(CreateEventMixin ,forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "date", "time", "location", "category", "asset"]
        widgets = {
            "date": forms.DateInput(attrs={'type': 'date'}),
            "time": forms.TimeInput(attrs={'type':'time'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_form_style()

# class AddParticipants(CreateEventMixin, forms.ModelForm):
#     class Meta:
#         model = Participant
#         fields = "__all__"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.apply_form_style()

class AddCategory(CreateEventMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_form_style()

class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'border border-2 border-black p-2 mb-2 rounded-md w-full'}),
        empty_label="Select Role"
    )

class CreateGroupForm(CreateEventMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Select Permissions"
    )
    class Meta:
        model = Group
        fields = ["name", "permissions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_form_style()