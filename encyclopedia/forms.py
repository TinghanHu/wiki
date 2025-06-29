from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Topic", max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '輸入標題'}))
    content = forms.CharField(label="Context",
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': '使用 Markdown 語法輸入內容'}))