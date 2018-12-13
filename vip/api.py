from django.core.cache import cache
from lib.http import render_json

# Create your views here.
from vip.models import Vip


def show_vip_permissions(request):
    key = 'VipPermissions'
    vip_permissions = cache.get(key, [])
    if not vip_permissions:
        for vip in Vip.objects.filter(level__gte=1):
            vip_info = vip.to_dict()
            perm_info = []
            for perm in vip.permissions:
                perm_info.append(perm.to_dict())
            vip_info['perm_info'] = perm_info
            vip_permissions.append(vip_info)
        cache.set(key, vip_permissions)
    return render_json(vip_permissions)
