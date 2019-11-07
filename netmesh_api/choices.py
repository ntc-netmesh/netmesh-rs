import pytz

registration_choices = [
        ('registered', 'Registered'),
        ('unregistered', 'Unregistered'),
        ('disabled', 'Disabled')
    ]

ntc_region_choices = [
    ('1', 'NTC Region 1'),
    ('2', 'NTC Region 2'),
    ('3', 'NTC Region 3'),
    ('4-A', 'NTC Region 4-A'),
    ('4-B', 'NTC Region 4-B'),
    ('5', 'NTC Region 5'),
    ('6', 'NTC Region 6'),
    ('7', 'NTC Region 7'),
    ('8', 'NTC Region 8'),
    ('9', 'NTC Region 9'),
    ('10', 'NTC Region 10'),
    ('11', 'NTC Region 11'),
    ('12', 'NTC Region 12'),
    ('13', 'NTC Region 13'),
    ('NCR', 'NTC Region NCR'),
    ('CAR', 'NTC Region CAR'),
    ('BARMM', 'NTC Region BARMM'),
    ('Central', 'NTC Region Central'),
    ('unknown', 'Unknown')
]
device_choices = [
        ('unknown', 'Unknown'),
        ('computer', 'Computer'),
        ('smartphone', 'Smart Phone')
    ]
network_choices = [
    ('unkown', 'unknown'),
    ('2g', '2G'),
    ('3g', '3G'),
    ('4g', '4G'),
    ('lte', 'LTE'),
    ('dsl', 'DSL'),
]
server_choices = [
    ('local', 'Local'),
    ('overseas', 'Overseas'),
    ('ix', 'Internet Exchange'),
    ('web-based', 'Web-based'),
    ('unknown', 'Unknown')
]

test_type_choices = [
    ('0', 'unknown'),
    ('1', 'other'),
    ('2', 'RFC 6349'),
    ('3', 'Web-based'),
]

timezone_choices = [(v, v) for v in pytz.common_timezones]

direction_choices = [
    ('forward', 'Forward'),  # client to test server
    ('reverse', 'Reverse'),  # test server to client
    ('unknown', 'Unknown')
]

test_mode_choices = [
    ('upload', 'Upload Mode'),      # formerly normal mode
    ('download', 'Download Mode'),  # formerly reverse mode
    ('simultaneous', 'Simultaneous Mode'),
    ('unknown', 'Unknown')
]