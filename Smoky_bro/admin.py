from django.contrib import admin
from django import forms

from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import path
from dal import autocomplete

from .models import *


class ParentProductFilter(admin.SimpleListFilter):
    title = ('Parent product')
    parameter_name = 'parent_product'

    def lookups(self, request, model_admin):
        return (
            ('no_parent', ('Только родительские')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no_parent':
            return queryset.filter(parent_product_id=None)
        else:
            return queryset

class ParentProductFilterInShops(admin.SimpleListFilter):
    title = 'Parent product'
    parameter_name = 'parent_product'

    def lookups(self, request, model_admin):
        return (
            ('no_parent', 'Только родительские'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no_parent':
            return queryset.filter(productid__in=Products.objects.filter(parent_product_id=None))
        else:
            return queryset


# class ProductInShopForm(forms.ModelForm):
#     shop_id = forms.CharField(label='Адрес магазина', disabled=True, widget=forms.Textarea(attrs={'rows': 3}))
#     is_parent_product = forms.BooleanField(label='Родительский товар', required=False)
#
#     class Meta:
#         model = Products_in_shops
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         shop_id = self.instance.shopid
#         shop = Shops.objects.get(shopid=shop_id)
#         self.fields['shop_id'].initial = str(shop)
#
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.shopid = self.cleaned_data['shop_id'].shopid
#
#         if self.cleaned_data['is_parent_product']:
#             child_products = Products.objects.filter(parent_product_id=instance.productid)
#
#             for child_product in child_products:
#                 product_in_shop = Products_in_shops.objects.filter(shopid=instance.shopid,
#                                                                    productid=child_product.productid).first()
#                 if not product_in_shop:
#                     product_in_shop = Products_in_shops.objects.create(shopid=instance.shopid,
#                                                                        productid=child_product.productid,
#                                                                        count=0, name=child_product.name)
#                 else:
#                     product_in_shop.count += 1
#                     product_in_shop.save()
#
#
#         if commit:
#             instance.save()
#         return instance


class ProductInShopForm2(forms.ModelForm):
    shop_id = forms.CharField(label='Адрес магазина', disabled=True, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Products_in_shops
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        shop_id = self.instance.shopid
        shop = Shops.objects.get(shopid=shop_id)
        self.fields['shop_id'].initial = str(shop)



class ProductInShopForm(forms.ModelForm):
    shop_id = forms.ModelChoiceField(queryset=Shops.objects.all(), to_field_name='shopid', empty_label=None, label='Магазин', required=True)
    is_parent_product = forms.BooleanField(label='Родительский товар', required=False)
    class Meta:
        model = Products_in_shops
        fields = '__all__'
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.shopid = self.cleaned_data['shop_id'].shopid

        if self.cleaned_data['is_parent_product']:
            child_products = Products.objects.filter(parent_product_id=instance.productid)

            for child_product in child_products:
                product_in_shop = Products_in_shops.objects.filter(shopid=instance.shopid,
                                                                   productid=child_product.productid).first()
                if not product_in_shop:
                    product_in_shop = Products_in_shops.objects.create(shopid=instance.shopid,
                                                                       productid=child_product.productid,
                                                                       count=0, name=child_product.name)
                else:
                    product_in_shop.count += 1
                    product_in_shop.save()


        if commit:
            instance.save()
        return instance


class ProductsForm(forms.ModelForm):
    brandid = forms.ModelChoiceField(
        queryset=Brands.objects.all(),
        widget=autocomplete.ModelSelect2(url='brand-autocomplete')
    )


class BrandsAdmin(admin.ModelAdmin):
    list_display = ('brandid', 'name')
    list_display_links = ('brandid', 'name')
    search_fields = ('brandid', 'name')


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('categoryid', 'name')
    list_display_links = ('categoryid', 'name')
    search_fields = ('categoryid', 'name')


class ChargingsAdmin(admin.ModelAdmin):
    list_display = ('chargingid', 'name')
    list_display_links = ('chargingid', 'name')
    search_fields = ('chargingid', 'name')



class ShopsAdmin(admin.ModelAdmin):
    list_display = ('shopid', 'shopcity', 'shopstreet', 'shophouse', 'cash')
    list_display_links = ('shopid', 'shopstreet')
    search_fields = ('shopid', 'shopcity', 'shopstreet', 'shophouse')


class StocksAdmin(admin.ModelAdmin):
    list_display = ('stockid', 'name', 'description')
    list_display_links = ('stockid', 'name')
    search_fields = ('stockid', 'name')


class UsersAdmin(admin.ModelAdmin):
    list_display = ('userid', 'telegramid', 'name', 'surname', 'phone', 'roleid', 'point')
    list_display_links = ('userid', 'telegramid', 'name', 'surname', 'phone', 'roleid')
    search_fields = ('userid', 'telegramid', 'name', 'surname', 'phone', 'roleid')


class ChecksAdmin(admin.ModelAdmin):
    list_display = ('checkid', 'shopid', 'datecheck', 'checkprice', 'sale')
    list_display_links = ('checkid', 'shopid', 'datecheck')
    search_fields = ('checkid', 'shopid', 'checkprice', 'sale')


class ProductsInShopsAdmin(admin.ModelAdmin):
    list_display = ['shopid', 'productid', 'count', 'name', 'description', 'countsell', 'income']
    list_display_links = ['name']
    search_fields = ('name',)
    exclude = ['shopid', 'countsell', 'income']
    list_editable = ['count']
    list_filter = (ParentProductFilterInShops,)

    def get_form(self, request, obj=None, **kwargs):
        if 'add' in request.path:  # Если объект существует, это операция редактирования или просмотра
            self.form = ProductInShopForm

        else:  # Если объект не существует, это операция добавления
            self.form = ProductInShopForm2

        return super().get_form(request, **kwargs)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Ищем товары в Products, у которых название содержит поисковый термин
        products = Products.objects.filter(name__icontains=search_term)

        # Ищем товары в Products, у которых parent_product_id содержит id найденных товаров в products
        products_with_parent = Products.objects.filter(
            parent_product_id__in=products.values_list('productid', flat=True))

        # Объединяем результаты поиска
        queryset |= self.model.objects.filter(
            Q(name__icontains=search_term) | Q(productid__in=products_with_parent.values_list('productid', flat=True)))

        # Применяем фильтр "Родительские товары", если он выбран
        parent_product_filter = request.GET.get('parent_product')
        if parent_product_filter == 'no_parent':
            queryset = queryset.filter(productid__in=Products.objects.filter(parent_product_id=None))

        return queryset, use_distinct



class ProductsAdmin(admin.ModelAdmin):
    #form = ProductsForm
    exclude = ['photoid']
    list_display = ('productid', 'name', 'description', 'price', 'parent_product_id')
    autocomplete_fields = ['brandid']
    list_display_links = ('productid', 'name')
    search_fields = ('productid', 'name', 'parent_product_id')
    list_filter = (ParentProductFilter,)

    actions = ['add_to_all_shops', 'add_child_products_to_all_shops']

    def add_to_all_shops(self, request, queryset):
        shops = Shops.objects.all()
        for shop in shops:
            for product in queryset:
                # Проверяем существует ли товар в магазине
                product_in_shop = Products_in_shops.objects.filter(shopid=shop.shopid,
                                                                   productid=product.productid).first()
                if not product_in_shop:
                    # Если нет, то создаем запись и устанавливаем количество товара в магазине на 0
                    product_in_shop = Products_in_shops.objects.create(shopid=shop.shopid, productid=product.productid,
                                                                       count=0, name=product.name)
                else:
                    # Иначе, увеличиваем количество товара на 1
                    product_in_shop.count += 1
                    product_in_shop.save()
                product_in_shop.description = product.description



        self.message_user(request, f"Товары успешно добавлен во все магазины.")

    def add_child_products_to_all_shops(modeladmin, request, queryset):
        # Проходимся по выбранным товарам
        for selected_product in queryset:
            # Проверяем, что у продукта нет родительского продукта
            if not selected_product.parent_product_id:
                # Получаем список всех магазинов
                shops = Shops.objects.all()

                # Создаем список всех товаров - дочерних к выбранному
                child_products = Products.objects.filter(parent_product_id=selected_product.productid)

                # Добавляем дочерние товары в каждый магазин
                for shop in shops:
                    # Создаем список объектов Products_in_shops с новыми дочерними товарами
                    new_products = [Products_in_shops(productid=child_product.productid, shopid=shop.shopid, count=0,
                                                      name=child_product.name, description=child_product.description,
                                                      countsell=0, income=0) for child_product in child_products]

                    # Используем bulk_create для добавления списка товаров в текущий магазин
                    Products_in_shops.objects.bulk_create(new_products)


    add_to_all_shops.short_description = "Добавить выбранные товары во все магазины"
    add_child_products_to_all_shops.short_description = "Добавить дочерние товары выбранных родительских товаров во все магазины"


admin.site.register(Brands, BrandsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Chargings, ChargingsAdmin)
admin.site.register(Checks, ChecksAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Roles)
admin.site.register(Shops, ShopsAdmin)
admin.site.register(Stocks, StocksAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Products_in_shops, ProductsInShopsAdmin)



