# # from django.conf import settings
# # from django.contrib import admin
# from django_hosts import patterns, host

# # host_patterns = patterns('',
# #     host(r'admin', settings.ROOT_URLCONF, name='www'),
# # #    host(r'admin', settings.ROOT_URLCONF, name='admin'),
# # )

# host_patterns = patterns('',
#     host(r'', 'src.urls', name=' '),
#     host(r'hello', 'home.urls', name='home'),
#     host(r'auth', 'accounts.urls', name='accounts'),
# )


# from django.conf import settings
# from django_hosts import patterns, host

# host_patterns = patterns('',
#     host(r'www', settings.ROOT_URLCONF, name='www'),
#     host(r'hello', 'home.urls', name='home'),
#     host(r'(?!www).*', 'donor.urls', name='wildcard'),
# )
