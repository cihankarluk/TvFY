from TvFY.core.exceptions import ValidationError


class BaseSerializer:
    initial_data: dict
    fields: dict

    def validate(self, attrs):
        unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
        if unknown_keys:
            raise ValidationError(f"Got unknown fields: {unknown_keys}")
        return attrs
