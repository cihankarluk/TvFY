from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from TvFY.user.models import Account

__all__ = ["AccountAdmin"]


@register(Account)
class AccountAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opts.verbose_name_plural = "Accounts"

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
    )
