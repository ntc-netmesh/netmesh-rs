from django.core.exceptions import ValidationError


def check_lat(lat):
    lat = float(lat)
    if (lat > 90) or (lat < -90):
        raise ValidationError('Value exceeded valid latitude limits.',
                              params={'value': lat}, )
    else:
        return lat


def check_long(long):
    long = float(long)
    if (long > 180) or (long < -180):
        raise ValidationError('Value exceeded valid longitude limits.',
                              params={'value': long}, )
    else:
        return long
