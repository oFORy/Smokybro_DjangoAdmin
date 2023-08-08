from dal import autocomplete
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Brands(models.Model):
    brandid = models.AutoField(db_column='BrandId', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', verbose_name='Название')  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Brands'
        verbose_name_plural = "Бренды"
        ordering = ['brandid']


class Categories(models.Model):
    categoryid = models.AutoField(db_column='CategoryId', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', verbose_name='Название')  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Categories'
        verbose_name_plural = "Категории"
        ordering = ['categoryid']


class Chargings(models.Model):
    chargingid = models.AutoField(db_column='ChargingId', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', verbose_name='Название')  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Chargings'
        verbose_name_plural = "Тип зарядки"
        ordering = ['chargingid']


class Checks(models.Model):
    checkid = models.AutoField(db_column='CheckId', primary_key=True, verbose_name='id чека')  # Field name made lowercase.
    shopid = models.IntegerField(db_column='ShopId', verbose_name='id магазина')  # Field name made lowercase.
    datecheck = models.DateTimeField(db_column='DateCheck', verbose_name='Дата создания чека')  # Field name made lowercase.
    checkprice = models.IntegerField(db_column='CheckPrice', verbose_name='Стоимость чека')  # Field name made lowercase.
    sale = models.TextField(db_column='Sale', blank=True, null=True, verbose_name='Скидка')  # Field name made lowercase.
    checkss = models.TextField(db_column='Check', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    paymentmethod = models.IntegerField(db_column='PaymentMethod', blank=True, null=True, verbose_name='Способ оплаты')  # Field name made lowercase.

    def __str__(self):
        return self.sale

    class Meta:
        managed = False
        db_table = 'Checks'
        verbose_name_plural = "Чеки"
        ordering = ['checkid']




class Roles(models.Model):
    roleid = models.AutoField(db_column='RoleId', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', verbose_name='Роль пользователя')  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Roles'
        verbose_name_plural = "Роли"
        ordering = ['roleid']



class Stocks(models.Model):
    stockid = models.AutoField(db_column='StockId', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', verbose_name='Название')  # Field name made lowercase.
    brandid = models.ForeignKey(Brands, models.DO_NOTHING, db_column='BrandId', verbose_name='Id бренда товара')  # Field name made lowercase.
    categoryid = models.ForeignKey(Categories, models.DO_NOTHING, db_column='CategoryId', verbose_name='Id категории товара')  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True, verbose_name='Описание')  # Field name made lowercase.
    chargingid = models.ForeignKey(Chargings, models.DO_NOTHING, db_column='ChargingId', blank=True, null=True, verbose_name='Id зарядки товара')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Stocks'
        verbose_name_plural = "Склад"
        ordering = ['stockid']


class Users(models.Model):
    userid = models.AutoField(db_column='UserId', primary_key=True)  # Field name made lowercase.
    telegramid = models.BigIntegerField(db_column='TelegramId')  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Имя')  # Field name made lowercase.
    surname = models.TextField(db_column='Surname', blank=True, null=True, verbose_name='Фамилия')  # Field name made lowercase.
    phone = models.TextField(db_column='Phone', blank=True, null=True, verbose_name='Номер телефона')  # Field name made lowercase.
    roleid = models.ForeignKey(Roles, models.DO_NOTHING, db_column='RoleId', blank=True, null=True, verbose_name='Роль пользователя')  # Field name made lowercase.
    point = models.IntegerField(db_column='Point', blank=True, null=True, verbose_name='Накопленные баллы')  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'Users'
        verbose_name_plural = "Пользователи"
        ordering = ['userid']


class Shops(models.Model):
    shopid = models.AutoField(db_column='ShopId', primary_key=True)
    shopcity = models.TextField(db_column='ShopCity', verbose_name='Город')
    shopstreet = models.TextField(db_column='ShopStreet', blank=True, null=True, verbose_name='Улица')
    shophouse = models.TextField(db_column='ShopHouse', blank=True, null=True, verbose_name='Дом')
    cash = models.IntegerField(db_column='Cash', blank=True, null=True, verbose_name='Осталось денег')

    def __str__(self):
        return f"""{self.shopcity}, {self.shopstreet}, {self.shophouse}"""

    class Meta:
        managed = True
        db_table = 'Shops'
        verbose_name_plural = "Магазины"
        ordering = ['shopid']


class Products_in_shops(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    productid = models.IntegerField(db_column='Productid', verbose_name='Id товара компании')
    shopid = models.IntegerField(db_column='Shopid', verbose_name='Id магазина')
    count = models.IntegerField(db_column='Count', default=0, verbose_name='Количество товара в магазине')
    name = models.TextField(db_column='Name', verbose_name='Название')
    description = models.TextField(db_column='Description', blank=True, null=True, verbose_name='Описание')
    countsell = models.IntegerField(db_column='CountSell', verbose_name='Проданно (количествово)', default=0)
    income = models.IntegerField(db_column='Income', verbose_name='Доход', default=0)


    class Meta:
        managed = True
        db_table = 'Products_in_shops'
        verbose_name_plural = "Товары в магазинах"
        ordering = ['shopid', 'productid']




class Products(models.Model):
    productid = models.AutoField(db_column='ProductId', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', verbose_name='Название')  # Field name made lowercase.
    #brandid = models.ForeignKey(Brands, models.DO_NOTHING, db_column='BrandId', verbose_name='бренд товара')  # Field name made lowercase.
    brandid = models.ForeignKey(Brands, models.DO_NOTHING, db_column='BrandId', verbose_name='бренд товара', related_name='products')
    categoryid = models.ForeignKey(Categories, models.DO_NOTHING, db_column='CategoryId', verbose_name='категория товара')  # Field name made lowercase.
    price = models.IntegerField(db_column='Price', verbose_name='Цена')  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True, verbose_name='Описание')  # Field name made lowercase.
    chargingid = models.ForeignKey(Chargings, models.DO_NOTHING, db_column='ChargingId', blank=True, null=True, verbose_name='Id зарядки товара')  # Field name made lowercase.
    sale = models.TextField(db_column='Sale', blank=True, null=True, verbose_name='Скидки\Акции')  # Field name made lowercase.
    dateadd = models.DateTimeField(db_column='DateAdd', verbose_name='Дата добавления')  # Field name made lowercase.
    photoid = models.TextField(db_column='PhotoId', blank=True, null=True)  # Field name made lowercase.
    parent_product_id = models.IntegerField(blank=True, null=True, verbose_name='Id родительского товара')

    class Meta:
        managed = True
        db_table = 'Products'
        verbose_name_plural = "Товары"
        ordering = ['productid']

    def save(self, *args, **kwargs):
        if self.parent_product_id:
            parent_product = Products.objects.get(productid=self.parent_product_id)
            #self.name = parent_product.name
            self.brandid = parent_product.brandid
            self.categoryid = parent_product.categoryid
            self.price = parent_product.price
            self.description = parent_product.description
            self.chargingid = parent_product.chargingid
            #self.sale = parent_product.sale
            #self.photoid = parent_product.photoid
        super().save(*args, **kwargs)


@receiver(post_save, sender=Products)
def update_product_in_shops(sender, instance, **kwargs):
    products_in_shops = Products_in_shops.objects.filter(productid=instance.productid)

    for product_in_shop in products_in_shops:
        product_in_shop.name = instance.name
        product_in_shop.description = instance.description
        # обновите и другие поля, если необходимо
        product_in_shop.save()


# class ProductShop(models.Model):
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     store = models.ForeignKey(Products_in_shops, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ('product', 'store')



