from django import forms

from chainlink.models import BloodTesting, Distribution, BloodDonation, Package, Storage, Transfusion


class BloodTestForm(forms.ModelForm):
    class Meta:
        model = BloodTesting
        fields = '__all__'

class BloodDonationForm(forms.ModelForm):
    class Meta:
        model = BloodDonation
        fields = '__all__'

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = '__all__'

class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = '__all__'

class TransfusionForm(forms.ModelForm):
    class Meta:
        model = Transfusion
        fields = '__all__'

