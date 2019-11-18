from django.contrib import admin
from users.models import MainUser, Profile, Activation
from django.contrib.auth.admin import UserAdmin


class InlineProfile(admin.StackedInline):
    model = Profile
    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'
    can_delete = False


@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'is_staff')
    inlines = [InlineProfile,]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'bio', 'user',)


@admin.register(Activation)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'user',)