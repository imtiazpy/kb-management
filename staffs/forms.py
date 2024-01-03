from django import forms
from users.models import User
from staffs.models import Staff


class SaveProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "avatar")
    
    # Additional fields from the Staff model
    phone = forms.CharField(max_length=11, required=False)
    dob = forms.DateField(required=False)
    nid = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If the instance (user) is provided, populate the form fields
        if self.instance and hasattr(self.instance, 'user_staff'):
            staff = self.instance.user_staff
            self.fields['phone'].initial = staff.phone
            self.fields['dob'].initial = staff.dob
            self.fields['nid'].initial = staff.nid

    def save(self, commit=True):
        if self.instance and isinstance(self.instance, User):
            user = self.instance
        else:
            user = super().save(commit=False)

        # Check if the related Staff instance exists
        if not hasattr(user, 'user_staff') or user.user_staff is None:
            user.user_staff = Staff()

        user.user_staff.phone = self.cleaned_data['phone']
        user.user_staff.dob = self.cleaned_data['dob']
        user.user_staff.nid = self.cleaned_data['nid']

        if commit:
            user.save()
            user.user_staff.save()

        return user

