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

        # for product in products:
        #     print("title: ", product.title,
        #           " variants: ", product.product_variant_prices.all())

        products = Product.objects.all()

        product_items = []
        for product in products:
            product_variants = []
            variants = product.product_variant_prices.all()
            # print("variant_set: ", variants)

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

                # print("variants: ", product_variants)

            product_items.append({
                "id": product.id,
                "title": product.title,
                "description": product.description,
                "variants": product_variants,
                "created_at": product.created_at,
            })

        # print("product_items: ", product_items)

        context['products'] = product_items
        return context
