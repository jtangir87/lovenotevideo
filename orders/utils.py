from .models import Package, EventCoupon
from django_simple_coupons.models import Coupon


def get_package_price(video_count, package):
    package = Package.objects.filter(id=package.id).first()
    if video_count <= package.included_videos:
        return package.price
    else:
        extra_vids = video_count - package.included_videos
        extra_vid_cost = extra_vids * package.addtl_video_price
        return package.price + extra_vid_cost


def check_event_coupon(event_coupon, order_total):
    coupon = Coupon.objects.get(code=event_coupon.coupon)
    ec = EventCoupon.objects.get(id=event_coupon.id)
    if coupon.discount.is_percentage:
        if coupon.discount.value == 100:
            discount_value = order_total
        else:
            discount_value = float(order_total) * (coupon.discount.value / 100)
    else:
        discount_value = coupon.discount.value
    ec.discount_value = discount_value
    ec.save()
    return ec.discount_value
