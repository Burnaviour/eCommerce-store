from django.core.exceptions import ValidationError


def validator_image(file):

    kilobyte_limit = 500
    # print(file.size)
    if file.size > kilobyte_limit*1024:
        raise ValidationError(f"Max file size is {kilobyte_limit}KB")
