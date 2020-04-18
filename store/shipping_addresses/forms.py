from django.forms import ModelForm
from .models import ShippingAddress

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'line1', 'line2', 'city', 'state', 'country', 'zip_code', 'reference'
        ]
        labels = {
            'line1': 'Address line 1', 'line2':'Address line 2', 'city':'City', 'state':'State/Province/Region: ', 
            'country': 'Country/Region:', 'zip_code': 'ZIP', 'reference': 'Reference'
        }

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
