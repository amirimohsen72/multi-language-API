from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from core.models import CustomUser, ShopUserDetailModel


@receiver(post_save, sender=CustomUser)
def custom_user_type_shop_post_save(sender, instance, created, **kwargs):
    if instance.type == '2':
        try:
            get = instance.shop_detail
        except ShopUserDetailModel.DoesNotExist:
            detail = ShopUserDetailModel.objects.create(user=instance)
            detail.translations.create(language_code='fa', title=instance.fullname, )

        if created:
            try:
                shopgroup = Group.objects.get(name='فروشگاه')
                instance.groups.add(shopgroup)
            except :
                shopgroup = Group.objects.get(id='3')
                instance.groups.add(shopgroup)
        # if not instance.shop_detail:
        #     shopdetail = ShopUserDetailModel.objects.create(user=instance)
    if instance.type == '1':
        if created:
            try:
                customergroup = Group.objects.get(name='کاربر خریدار')
                instance.groups.add(customergroup)
            except :
                customergroup = Group.objects.get(id='1')
                instance.groups.add(customergroup)
    if instance.type == '3':
        if created:
            try:
                marketergroup = Group.objects.get(name='بازاریاب')
                instance.groups.add(marketergroup)
            except :
                marketergroup = Group.objects.get(id='2')
                instance.groups.add(marketergroup)
