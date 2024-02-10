from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.db import transaction
from jalali_date import datetime2jalali
from rest_framework import serializers

from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.serializers import TranslatedFieldsField

from core.models import AffiliateRelation
from shop.models import CartModel, CartItemModel, OrderModel, OrderItemModel, ProductModel, OrderCommissionModel
from config.settings import AUTH_USER_MODEL


# ---------------------------------------------order customer -----------------------------------------
class OrderCustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=255, source='fullname')
    phone_number = serializers.CharField(source='phone_number')

    class Meta:
        model = AUTH_USER_MODEL
        fields = ['id', 'full_name', 'phone_number']


# --------------------------------------------------- order item product sm ------------------------------------------
class OrderItemsProductSmSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductModel)

    class Meta:
        model = ProductModel
        fields = ['translations', 'id', 'image', ]

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'title': super().to_representation(instance)['translations'][lang]['title'],
            'slug': super().to_representation(instance)['translations'][lang]['slug'],
            'id': super().to_representation(instance)['id'],
            'image': super().to_representation(instance)['image'],
        }
        return data


# ---------------------------------------------- order item product ---------------------------------------
class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['id', 'image', 'type']


# -------------------------------------------------- order item -------------------------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemsProductSmSerializer()

    class Meta:
        model = OrderItemModel
        fields = ['id', 'product', 'quantity', 'unit_price', 'weight', 'final_weight_wages']


# -------------------------------------------------- order item -------------------------------------------
class OrderItemSmSerializer(serializers.ModelSerializer):
    product = OrderItemsProductSmSerializer()

    class Meta:
        model = OrderItemModel
        fields = ['id', 'product', ]


# ------------------------------------------------------- order list ---------------------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    status = serializers.CharField(source='get_status_display')
    marketer_fullname = serializers.SerializerMethodField()
    jalali_date = serializers.SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = ['id', 'customer_name', 'marketer_fullname', 'total_weight', 'total_price', 'total_weight_wages',
                  'datetime_created','jalali_date',
                  'items', 'status']

    def get_status_display(self, obj):
        return _(obj.get_status_display())

    def get_marketer_fullname(self, obj):
        return obj.marketer.fullname if obj.marketer else None

    def get_jalali_date(self, obj):
        return datetime2jalali(obj.datetime_created).strftime('%Y/%m/%d')


# ------------------------------------------------------- order list ---------------------------------------
class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSmSerializer(many=True)
    status = serializers.CharField(source='get_status_display')
    jalali_date = serializers.SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = ['id', 'items', 'datetime_created','jalali_date', 'status']

    def get_status_display(self, obj):
        return _(obj.get_status_display())

    def get_jalali_date(self, obj):
        return datetime2jalali(obj.datetime_created).strftime('%Y/%m/%d')


# -----------------------------------------------------order for admin ------------------------------------------
class OrderForAdminSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    # customer = OrderCustomerSerializer()

    class Meta:
        model = OrderModel
        fields = ['id', 'customer_name', 'total_weight', 'total_weight_wages', 'status', 'datetime_created',
                  'items']


# -------------------------------------------------------- order update status ----------------------------------------
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['status']


# -------------------------------------------------------- order create ---------------------------------------------
class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    order_note = serializers.CharField(allow_blank=True, )

    # translations = TranslatedFieldsField(read_only=True)

    def validate_cart_id(self, cart_id):
        # try:
        #     if Cart.objects.prefetch_related('items').get(id=cart_id).items.count() == 0:
        #         raise serializers.ValidationError('Your cart is empty. Please add some products to it first!')
        # except Cart.DoesNotExist:
        #     raise serializers.ValidationError('There is no cart with this cart id!')

        if not CartModel.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError(_('There is no cart with this cart id!'))

        if CartItemModel.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError(_('Your cart is empty. Please add some products to it first!'))

        return cart_id

    def save(self, **kwargs):
        lang = self.context.get('lang', 'en')
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            order_note = self.validated_data['order_note']
            user_id = self.context['user_id']
            customer = get_user_model().objects.get(id=user_id)

            order = OrderModel()
            order.customer = customer
            order.customer_name = customer.fullname
            order.order_note = order_note
            if customer.reff_marketer:
                affiliate_relation = AffiliateRelation.objects.filter(marketer=customer.reff_marketer).first()
                order.marketer = customer.reff_marketer
                order.marketer_commission = f'{affiliate_relation.commission} {affiliate_relation.get_type_display()}'

            order.save()


            if order.marketer:
                commission_pay_insert = OrderCommissionModel(
                    order=order,
                    marketer=order.marketer,
                    marketer_commission=order.marketer_commission,
                    extra_note=_('new order submited'),
                    status=OrderCommissionModel.COMMISSION_STATUS_UNPAID,
                )
                commission_pay_insert.save()

            cart_items = CartItemModel.objects.select_related('product').filter(cart_id=cart_id)

            order_items = [
                OrderItemModel(
                    order=order,
                    product=cart_item.product,
                    unit_price=cart_item.product.get_translation(lang).price,
                    quantity=cart_item.quantity,
                    weight=cart_item.product.get_translation(lang).weight,
                    final_weight_wages=cart_item.product.get_translation(lang).weight_with_wages,
                ) for cart_item in cart_items
            ]

            OrderItemModel.objects.bulk_create(order_items)

            CartModel.objects.get(id=cart_id).delete()
            order.calculate_total()
            return order


# ------------------------------------------------- copy order -------------------------------------------------
# -----------------------cart items ----------------
class CopyCartItemSerializer(serializers.ModelSerializer):
    product = OrderItemsProductSmSerializer()

    class Meta:
        model = CartItemModel
        fields = ['id', 'product', 'quantity', ]
        # fields = '__all__'


# ----------------------- copy items ---------------
class CopyToCartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, cart):
        # دریافت آیتم‌های سبد
        items = CartItemModel.objects.filter(cart=cart)
        serializer = CopyCartItemSerializer(items, many=True)
        return serializer.data

    class Meta:
        model = CartModel
        fields = '__all__'
