import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course):
    """
    Создаёт в Stripe объект Product и возвращает его id.
    """
    product = stripe.Product.create(
        name=course.name,
        description=course.description or "",
    )
    return product.id

def create_stripe_price(course, product_id):
    """
    Создаёт в Stripe объект Price (цена в копейках) и возвращает его id.
    """
    # Stripe ожидает цену в центах (или копейках): умножаем на 100
    unit_amount = int(course.price * 100)
    price = stripe.Price.create(
        product=product_id,
        unit_amount=unit_amount,
        currency="usd",
    )
    return price.id

def create_checkout_session(course, price_id, user):
    """
    Создаёт в Stripe Checkout Session и возвращает его id и URL.
    """
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000" + "/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:8000" + "/cancelled/",
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price": price_id,
            "quantity": 1,
        }],
        metadata={
            "course_id": str(course.id),
            "user_id": str(user.id),
        }
    )
    return session.id, session.url