from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # This loop adds the Bootstrap "form-control" class to all fields
        # This makes the "white background" look professional
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'