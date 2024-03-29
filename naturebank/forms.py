from django import forms

from naturebank.models import Biotope, Species


class BiotopeAdminForm(forms.ModelForm):

    species_multi = forms.ModelMultipleChoiceField(
        label="Είδη του τόπου",
        queryset=Species.objects.all(),
        required=False,
        help_text=(
            "Χαρακτηριστικά είδη του τόπου. "
            "Για να επιλέξετε πολλά κρατήστε πατημέντο"
            ' το κουμπί "control"!'
        ),
    )

    class Meta:
        model = Biotope
        fields = "__all__"
