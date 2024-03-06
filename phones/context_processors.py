# from phones.forms import PhoneCategoryForm
from phones.models import Pages, PhoneCategoryModel


def page_processor(request):
    pages = Pages.objects.filter(page_status=1)
    return {'pages': pages}


def category_processor(request):
    categories = PhoneCategoryModel.objects.all()
    return {'categories': categories}

