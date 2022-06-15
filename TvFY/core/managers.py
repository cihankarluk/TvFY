from TvFY.core.helpers import get_random_string


class ManagerMixin:
    def create_tvfy_code(self) -> str:
        tvfy_code = f"{self.model.PREFIX}-{get_random_string(8)}"
        if super().get_queryset().filter(tvfy_code=tvfy_code).exists():
            return self.create_tvfy_code()
        return tvfy_code

    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        created_codes = []
        for obj in objs:
            tvfy_code = self.create_tvfy_code()
            while tvfy_code in created_codes:
                tvfy_code = self.create_tvfy_code()
            obj.tvfy_code = tvfy_code
        super().bulk_create(objs, batch_size, ignore_conflicts)
