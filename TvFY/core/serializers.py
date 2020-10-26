from TvFY.core.exceptions import ValidationError


class BaseSerializer:
    def validate(self, attrs):
        initial_data_keys = self.initial_data.keys()
        unknown_keys = set(initial_data_keys) - set(self.fields.keys())
        if unknown_keys:
            raise ValidationError(f"Got unknown fields: {unknown_keys}")
        return attrs
