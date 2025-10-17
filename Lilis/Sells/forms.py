from .models import BatchPriceHistory
from django import forms
import datetime

class BatchPriceHistoryForm(forms.ModelForm):
    class Meta:
        model = BatchPriceHistory
        fields = ['price', 'batch']
   
    def save(self, commit=True):
        batch_price_history = super(BatchPriceHistoryForm, self).save(commit=False)
        if commit:
            batch_price_history.save()
        return batch_price_history

