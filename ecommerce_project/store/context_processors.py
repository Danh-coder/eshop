from .models import Category, Cart

def categories(request):
    return {'categories': Category.objects.all()}

def cart_processor(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {'cart': cart}
    elif request.session.session_key:
        cart, created = Cart.objects.get_or_create(session_id=request.session.session_key)
        return {'cart': cart}
    return {'cart': None}
