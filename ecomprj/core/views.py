from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from core.models import Product, Category, Vendor, ProductImages,CartOrderItems, CartOrder,ProductReview, wishlist, Address
from taggit.models import Tag
from django.db.models import Count,Avg
from core.forms import ProductReviewForm
from django.template.loader import render_to_string


def index(request):
    #products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status = "published", featured = True ).order_by('-date')


    context = {
        "products" : products



    }
    return render(request, 'core/index.html', context)

def product_list_view(request):
    products = Product.objects.filter(product_status = "published" )
    context = {
        "products" : products
    }
    return render(request, 'core/product-list.html', context)


# Create your views here.
def category_list_view(request):

    categories = Category.objects.all()
    #categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')[:5]

    context = {
        "categories": categories
    }
    return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid = cid)
    products = Product.objects.filter(product_status="published", category = category)

    context = {
        "category": category,
        "products": products,

    }
    return render(request, 'core/category-product-list.html', context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,

    }
    return render(request, 'core/vendor-list.html', context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid = vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")
    #weight_options = ["50g", "60g", "80g", "100g", "150g"]
    context = {
        "vendor": vendor,
        "products": products,
        


    }
    return render(request, 'core/vendor-detail.html', context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid = pid)
    p_image = product.p_images.all()
    products = Product.objects.filter(category = product.category).exclude(pid=pid)


    ###################
    weight_options = ["50g", "80g", "100g", "150g","200g","500g","1000g"]

    ###############
    reviews = ProductReview.objects.filter(product= product).order_by("-date")
    #getting avg reviews
    average_rating = ProductReview.objects.filter(product= product).aggregate(rating=Avg('rating'))


    # Calculate the count of each rating
    rating_counts = reviews.values('rating').annotate(count=Count('rating')).order_by('rating')

    # Initialize dictionary to hold star counts
    star_counts = {i: 0 for i in range(1, 6)}

    # Fill the star_counts dictionary with actual counts
    for item in rating_counts:
        star_counts[item['rating']] = item['count']

    # Calculate total number of reviews
    total_reviews = reviews.count()

    # Calculate percentage for each star rating
    star_percentages = {star: (count / total_reviews) * 100 if total_reviews > 0 else 0 for star, count in star_counts.items()}

    # Calculate average rating percentage
    average_rating_percentage = (average_rating['rating'] / 5) * 100 if average_rating['rating'] else 0

    #Product review form
    review_form = ProductReviewForm()


    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False




    context = {
        "p": product,
        "p_image": p_image,
        "weight_options": weight_options,
        "current_weight": product.weight,
        "reviews": reviews,
        "products": products,
        "average_rating": average_rating,
        'average_rating_percentage': average_rating_percentage,
        'star_percentages': star_percentages,
        'review_form':review_form,
        'make_review':make_review,






    }
    return render(request, 'core/product-detail.html', context)


def tag_list(request,tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag,

    }
    return render(request, 'core/tag.html', context)   

def  ajax_add_review(request,pid):
    #try:

    product = Product.objects.get(id=pid)
    # except Product.DoesNotExist:
    #     return JsonResponse({'error': 'Product not found'}, status=404)
    user = request.user


    review = ProductReview.objects.create(

        user = user,
        product = product,
        review = request.POST["review"],
        rating = request.POST["rating"],
    )

    context = {
        "user": user.username,
        "review": request.POST["review"],
        "rating": request.POST["rating"],

    }

    avg_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
            'bool':True,
            "context": context,
            'avg_reviews': avg_reviews,
        }
    )

def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products": products,
        "query": query,
        

    }
    return render(request, 'core/search.html', context)

def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status = "published" ).order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

     
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()  

    context = {
        "products": products,
      
        

    }

    data = render_to_string("core/async/product-list.html", context)
    return JsonResponse({"data": data})





    









 