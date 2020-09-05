from django.contrib import admin
from index.models import Tokens


class TokensAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tokens, TokensAdmin)
