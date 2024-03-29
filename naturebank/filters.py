from string import ascii_letters

import django_filters

from .models import Biotope, BiotopeCategoryOption, GeoCodeOption, Species

ASCII_LETTERS = ascii_letters[26:]


class NomoiFilter(django_filters.ChoiceFilter):
    @property
    def field(self):
        ts = GeoCodeOption._default_manager.filter(code__regex=r"[1-9]\,0$")
        ts = ts.extra(order_by=["code"])
        rs = GeoCodeOption._default_manager.filter(code__endswith=",0,0")
        qs = GeoCodeOption._default_manager.filter(name__startswith="Νομός")
        self.extra["choices"] = [("", "Όλες")]
        self.extra["choices"].extend([(o.code, o) for o in rs])
        self.extra["choices"].extend([(o.code, o) for o in ts])
        self.extra["choices"].extend([(o.code, o) for o in qs])
        return super(NomoiFilter, self).field


class CategoryFilter(django_filters.ChoiceFilter):
    @property
    def field(self):
        qs = BiotopeCategoryOption._default_manager.all().exclude(id=5)
        self.extra["choices"] = [("", "Όλοι")]
        self.extra["choices"].extend([(o.id, o) for o in qs])
        return super(CategoryFilter, self).field


class BiotopeFilter(django_filters.FilterSet):
    geo_code = NomoiFilter(label="Γεωγραφική Περιοχή")
    category = CategoryFilter(label="Κατηγορία Τόπου")

    class Meta:
        model = Biotope
        fields = [
            "category",
            "geo_code",
        ]


class AlphabeticalFilter(django_filters.ChoiceFilter):
    """A filter to show only entries starting with a specific letter."""

    @property
    def field(self):
        self.extra["choices"] = [("", "---------")]
        self.extra["choices"].extend([(x, x) for x in ASCII_LETTERS])
        return super(AlphabeticalFilter, self).field


class SpeciesFilter(django_filters.FilterSet):
    species_name = AlphabeticalFilter(
        label="Αλφαβητική Επιλογή",
        lookup_expr="startswith",
        widget=django_filters.widgets.LinkWidget,
    )

    class Meta:
        model = Species
        fields = ["species_category", "plant_kind", "species_name"]
