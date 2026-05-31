from django.contrib.gis.db.models import Extent
from django.contrib.gis.geos import Polygon
from django.contrib.gis.shortcuts import render_to_kml
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from naturebank import models
from naturebank.filters import BiotopeFilter, SpeciesFilter

filter_keys = (
    "category",
    "climate",
    "site_type",
    "habitation",
    "designation",
    "condition",
    "abandon",
    "trend",
    "ecological_value",
    "social_value",
    "cultural_value",
    "threat",
    "conservation",
)


def frontpage(request):
    return render(request, "frontpage.html", {})


def info(request):
    return render(request, "info.html", {})


def info_usage(request):
    return render(request, "info_usage.html", {})


def poweredby(request):
    return render(request, "poweredby.html", {})


def tos(request):
    return render(request, "tos.html", {})


class BiotopeListView(ListView):
    model = models.Biotope
    paginate_by = 25

    def _remove_trailing_zeros(self, geo_code):
        """
        The primary key for geographical divisions (which have the unfortunate
        name GeoCodeOption) is an unfortunate comma-separated string of three
        integers, such "2,3,1", meaning primary division 2, subdivision 3,
        prefecture 1.  Zeros have a special meaning: "2,3,0" means primary
        division 2, subdivision 3.  This function removes trailing zeros,
        converting "2,3,0" to "2,3" (and "2,0,0" to "2"), so that it can be
        tested if a prefecture P is (in) a division x by checking it with
        P.startswith(y), where y is _remove_trailing_zeros(x).
        """
        while geo_code.endswith(",0"):
            geo_code = geo_code[:-2]
        return geo_code

    def get_queryset(self):
        # I'm rewriting old code that used old-style generic views, so that it
        # runs under Django 1.7. It wasn't particularly well-written, and I'm
        # not certain what it is supposed to do. A.X., 2014-11-03

        # Start with all objects
        q = super(BiotopeListView, self).get_queryset()

        # The database has an unfortunate hack: it contains some (430 last time
        # I counted) biotopes twice, once with Greek description (and other
        # fields) and once with English. The unfortunate way in which this
        # multilinguality has been achieved is to put the duplicates in a
        # different category. Specifically, category 4 ("CORINE Biotope") has
        # the Greek ones and category 5 ("CORINE Biotope (English)") has the
        # English ones. The precursor to this code was excluding category 5,
        # and so I continue this exclusion.
        q = q.exclude(category=5)

        # If geo_code is specified, filter by it.
        geo_code = self.request.GET.get(
            "geo_code", self.request.GET.get("GEO_CODE", "")
        )
        geo_code = self._remove_trailing_zeros(geo_code)
        q = q.filter(geo_code__code__startswith=geo_code)

        # Also filter by BiotopeFilter
        f = BiotopeFilter(self.request.GET, self.queryset)
        try:
            filterargs = {
                key: int(f.data[key]) for key in filter_keys if f.data.get(key, False)
            }
        except ValueError:  # Caught a filter key that is not an integer
            raise Http404
        q = q.filter(**filterargs)

        self.filter = f
        return q

    def get_context_data(self, **kwargs):
        context = super(BiotopeListView, self).get_context_data(**kwargs)
        context["form"] = self.filter.form
        imagelist = models.BiotopeImage.objects.filter(
            biotope__in=self.object_list
        ).order_by("?")[:5]
        context["image_list"] = imagelist
        parms = self.request.GET.copy()
        context["query_string_parms"] = parms.pop("page", True) and parms.urlencode()
        return context


def render_biotope_list_filter(filter_name):
    filters = {
        "habitation": models.HabitationOption,
        "site_type": models.SiteTypeOption,
        "climate": models.ClimateOption,
        "ecological_value": models.EcologicalValueOption,
        "designation": models.DesignationOption,
        "condition": models.ConditionOption,
        "abandon": models.AbandonmentOption,
        "trend": models.TrendOption,
        "social_value": models.SocialValueOption,
        "cultural_value": models.CulturalValueOption,
        "threat": models.ThreatOption,
        "conservation": models.ConservationOption,
    }
    filter_items = filters[filter_name].objects.all()
    s = ""
    for item in filter_items:
        s = s + '<option value="' + str(item.id) + '">' + item.name + "</option>\n"
    return s


def biotope_list_filter(request, filter_name):
    return HttpResponse(
        render_biotope_list_filter(filter_name), content_type="text/plain"
    )


class BiotopeDetailView(DetailView):
    model = models.Biotope
    template_name = "naturebank/biotope_detail.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        object_id = self.kwargs.get("pk", None)
        site_code = self.kwargs.get("site_code", "").upper()
        try:
            return (
                queryset.get(pk=object_id)
                if object_id
                else queryset.get(site_code=site_code)
            )
        except models.Biotope.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(BiotopeDetailView, self).get_context_data(**kwargs)
        context["rept_amph"] = self.object.species.filter(
            Q(
                species_category=models.SpeciesCategoryOption.objects.get(
                    abbreviation="AMPH"
                )
            )
            | Q(
                species_category=models.SpeciesCategoryOption.objects.get(
                    abbreviation="REPT"
                )
            )
        )
        context.update(
            {
                k: self.object.species.filter(
                    species_category=models.SpeciesCategoryOption.objects.get(
                        abbreviation=k.upper()
                    )
                )
                for k in ["bird", "fish", "flor", "inve", "mamm"]
            }
        )
        context["image_list"] = models.BiotopeImage.objects.order_by("order").filter(
            biotope__id=self.object.id
        )
        return context


class BiotopeDetailBriefView(DetailView):
    model = models.Biotope
    template_name = "naturebank/biotope_brief.html"


class SpeciesListView(ListView):
    model = models.Species
    paginate_by = 20

    def get_queryset(self):
        f = SpeciesFilter(self.request.GET, self.queryset)
        return f.qs

    def get_context_data(self, **kwargs):
        context = super(SpeciesListView, self).get_context_data(**kwargs)
        f = SpeciesFilter(self.request.GET, self.queryset)
        context["form"] = f.form
        parms = self.request.GET.copy()
        context["query_string_parms"] = parms.pop("page", True) and parms.urlencode()
        return context


class SpeciesDetailView(DetailView):
    model = models.Species
    template_name = "naturebank/species_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SpeciesDetailView, self).get_context_data()
        context["biotopes"] = self.object.biotope_set.exclude(category=5)
        return context


def index(request):
    """The view which returns the index page of the project"""

    return render(request, "index.html", {})


layers = {
    "sonbs": 1,
    "natura": 2,
    "corine": 4,
    "other": 3,
    "irrelevant": 0,
    "othersonbs": 6,
}
IELimit = (40, 140)

AREA_TRIGGER_PARAM = 300000  # Default to 30000


def kml(request, layer):
    bbox = request.GET.get("BBOX", request.GET.get("bbox", None))
    geo_code = request.GET.get("geo_code", request.GET.get("GEO_CODE", None))
    if geo_code:
        geo_code = geo_code.split(",")
        while geo_code[-1] == "0":
            geo_code.pop()
        geo_code = ",".join(geo_code)
    simplify = (
        True
        if request.GET.get("simplify", request.GET.get("SIMPLIFY", "True")) == "True"
        else False
    )
    simplify_fact = 0.001
    filterargs = {}
    for filter_key in filter_keys:
        afilter = request.GET.get(filter_key, request.GET.get(filter_key.upper(), None))
        if afilter:
            filterargs[filter_key] = afilter
    asite_code = request.GET.get("site_code", request.GET.get("SITE_CODE", None))
    species_id = request.GET.get("species", request.GET.get("SPECIES", None))
    if bbox:
        minx, miny, maxx, maxy = [float(i) for i in bbox.split(",")]
        geom = Polygon(
            ((minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)),
            srid=4326,
        )
        meansize = 0.5 * ((maxx - minx) + (maxy - miny))
        dxm = meansize / 400
        areatrigger = AREA_TRIGGER_PARAM * meansize * meansize
    else:
        areatrigger = 0

    queryres = models.Biotope.objects.filter(category=layers[layer])
    order_lst = [
        "gis_zorder",
    ]
    if bbox:
        queryres = queryres.filter(gis_mpoly__bboverlaps=geom)
    if geo_code:
        queryres = queryres.filter(geo_code__code__startswith=geo_code)
    if asite_code:
        asite_code = asite_code.replace("AE", "A0")
        queryres = models.Biotope.objects.filter(site_code=asite_code)
    queryres = queryres.filter(**filterargs)
    if species_id:
        queryres = queryres.filter(species__id=species_id)
    queryres = queryres.extra(order_by=order_lst)

    acount = 0
    for arow in queryres:
        acount += 1
        if arow.gis_area < areatrigger:
            if (
                arow.gis_mpoly
                and arow.gis_mpoly[0]
                and arow.gis_mpoly[0][0]
                and arow.gis_mpoly[0][0][0]
            ):
                x, y = arow.gis_mpoly[0][0][0]
                arow.kml = Polygon(
                    (
                        (x, y + dxm),
                        (x + dxm, y),
                        (x, y - dxm),
                        (x - dxm, y),
                        (x, y + dxm),
                    )
                ).kml
            continue
        if simplify:
            arow.kml = "\n".join(
                [
                    apoly.simplify(
                        tolerance=simplify_fact * meansize, preserve_topology=True
                    ).kml
                    for apoly in arow.gis_mpoly
                ]
            )
        else:
            arow.kml = "\n".join([apoly.kml for apoly in arow.gis_mpoly])
    response = render_to_kml("placemarks.kml", {"places": queryres})
    if layers[layer] == 0:
        response["Content-Disposition"] = 'attachment; filename="%s.kml"' % (
            asite_code,
        )
    return response


def bound(request):
    geo_code = request.GET.get("geo_code", request.GET.get("GEO_CODE", None))
    asite_code = request.GET.get("site_code", request.GET.get("SITE_CODE", None))
    species_id = request.GET.get("species", request.GET.get("SPECIES", None))
    filterargs = {}
    for filter_key in filter_keys:
        afilter = request.GET.get(filter_key, request.GET.get(filter_key.upper(), None))
        if afilter:
            filterargs[filter_key] = afilter
    if geo_code:
        geo_code = geo_code.split(",")
        while geo_code[-1] == "0":
            geo_code.pop()
        geo_code = ",".join(geo_code)

    queryres = models.Biotope.objects.all()
    if geo_code:
        queryres = queryres.filter(geo_code__code__startswith=geo_code)
    queryres = queryres.filter(**filterargs)
    if asite_code:
        asite_code = asite_code.replace("AE", "A0")
        queryres = models.Biotope.objects.filter(site_code=asite_code)
    if species_id:
        queryres = queryres.filter(species__id=species_id)

    try:
        extent = queryres.aggregate(Extent("gis_mpoly"))
        result = ",".join([str(x) for x in extent["gis_mpoly__extent"]])
    except TypeError:
        extent = models.Biotope.objects.all().aggregate(Extent("gis_mpoly"))
        result = ",".join([str(x) for x in extent["gis_mpoly__extent"]])
    return HttpResponse(result, content_type="text/plain")


def settlements_kml(request):
    bbox = request.GET.get("BBOX", request.GET.get("bbox", None))
    queryres = models.Settlement.objects.all().filter(point__isnull=False)
    if bbox:
        minx, miny, maxx, maxy = [float(i) for i in bbox.split(",")]
        geom = Polygon(
            ((minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)),
            srid=4326,
        )
        mean_size2 = maxx - minx + maxy - miny
        queryres = queryres.filter(point__contained=geom)
        if mean_size2 > 1.6:
            queryres = queryres.filter(area__gt=750000)
    for arow in queryres:
        if arow.point:
            arow.kml = arow.point.kml
    response = render_to_kml("point_placemarks.kml", {"places": queryres})
    return response
