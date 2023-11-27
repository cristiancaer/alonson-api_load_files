from utils.views import BasicCrudApiView
from .models import Company, Area
from .serializers import CompanySerializer, AreaSerializer
from rest_framework.permissions import AllowAny


class CompaniesApiView(BasicCrudApiView):
    permission_classes = (AllowAny,)
    model = Company
    serializer = CompanySerializer
    id_field_name = 'company_id'


class AreasApiView(BasicCrudApiView):
    permission_classes = (AllowAny,)
    model = Area
    serializer = AreaSerializer
    id_field_name = 'area_id'
