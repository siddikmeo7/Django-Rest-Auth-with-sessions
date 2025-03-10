from rest_framework.generics import *
from django.core.management import call_command
from django.http import JsonResponse
from django.views import View
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .filltres import BillFilter
from .serializers import *

from rest_framework import permissions



class UserAPIView(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


# Dishes
class DishListAPIView(ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer 
    filter_backends = [DjangoFilterBackend, OrderingFilter,SearchFilter]
    filterset_fields = ['name',"category"] 
    search_fields = ['name',"category"]
    permission_classes = [permissions.AllowAny]
    
    
class DishCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class DishRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class DishDestroyAPIView(DestroyAPIView):
    queryset = Menu.objects.all()

    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
    

class TableListAPIView(ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer 
    filter_backends = [DjangoFilterBackend, OrderingFilter,SearchFilter]
    filterset_fields = ['type',"max_person",] 
    search_fields = ['type',]

class TableCreateAPIView(CreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class TableRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableDestroyAPIView(DestroyAPIView):
    queryset = Table.objects.all()



# Bills
class BillListAPIView(ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer 
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = BillFilter
    filterset_fields = ['table', "castumername"] 
    search_fields = ['castumername']

    def get_queryset(self):
        queryset = super().get_queryset()
        bill_id = self.request.query_params.get('bill_id', None)
        if bill_id:
            queryset = queryset.filter(id=bill_id)
        queryset = queryset.prefetch_related('orders')  
        return queryset



class BillCreateAPIView(CreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

class BillRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        bill_id = self.request.query_params.get('bill_id', None)
        if bill_id: 
            queryset = queryset.filter(id=bill_id)
        queryset = queryset.prefetch_related('orders')  
        return queryset


class BillDestroyAPIView(DestroyAPIView):
    queryset = Bill.objects.all()

# Orders
class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 
    filter_backends = [DjangoFilterBackend, OrderingFilter,SearchFilter]
    filterset_fields = ['name',"bill",] 
    search_fields = ['id',]

class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def perform_create(self, serializer):
        bill = serializer.validated_data.get('bill')
        if not bill.is_active:
            raise ValidationError(f"Bill with ID {bill.id} is not active and cannot be used to create an order.")
        serializer.save()
        
class OrderRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDestroyAPIView(DestroyAPIView):
    queryset = Order.objects.all()



def run_migrations(request):
    try:
        # Выполнение миграций
        call_command('migrate', interactive=False)
        return JsonResponse({'status': 'success', 'message': 'Migrations completed successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})