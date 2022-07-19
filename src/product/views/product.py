from math import prod
from django.views import generic
from django.db.models import Count

from product.models import Product, Variant, ProductVariant, ProductVariantPrice


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        
        # get query params
        title = self.request.GET.get('title')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')

        products = None
        if len(title):
            products = Product.objects.filter(title__startswith=title)
        else:
            products = Product.objects.all()

        product_items = []
        for product in products:
            product_variants = []
            variants = product.product_variant_prices.all()

            for variant in variants:
                title = ""
                if variant.product_variant_one:
                    title += variant.product_variant_one.variant_title + '/'
                if variant.product_variant_two:
                    title += variant.product_variant_two.variant_title + '/'
                if variant.product_variant_three:
                    title += variant.product_variant_three.variant_title

                product_variants.append({
                    "title": title,
                    "price": variant.price,
                    "stock": variant.stock
                })

            product_items.append({
                "id": product.id,
                "title": product.title,
                "description": product.description,
                "variants": product_variants,
                "created_at": product.created_at,
            })

        context['products'] = product_items

        variants = []
        all_variants = Variant.objects.all()
        for variant in all_variants:
            product_variants = variant.productvariant_set.all()
            variants.append((variant.title, product_variants))

        context['variants'] = variants

        print("request: ", self.request.GET.get('title'))

        return context
