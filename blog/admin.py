from django.contrib import admin
from .models import Post
from django.contrib.auth.models import User, Group


# ❌ Remove unwanted "Groups"
admin.site.unregister(Group)


# 🔹 Inline posts inside user page
class PostInline(admin.TabularInline):
    model = Post
    extra = 0

    # ❌ Disable adding posts
    def has_add_permission(self, request, obj=None):
        return False

    # ❌ Disable editing posts
    def has_change_permission(self, request, obj=None):
        return False

    # ✅ Allow delete
    def has_delete_permission(self, request, obj=None):
        return True


# 🔹 Custom User Admin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username',)

    # show posts under each user
    inlines = [PostInline]

    # ❌ Disable adding users from admin
    def has_add_permission(self, request):
        return False

    # ✅ Allow viewing user page
    def has_change_permission(self, request, obj=None):
        return True


# 🔹 Custom Post Admin (Blogs)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')

    # ❌ No adding
    def has_add_permission(self, request):
        return False

    # ❌ No editing
    def has_change_permission(self, request, obj=None):
        return False

    # ✅ Only delete
    def has_delete_permission(self, request, obj=None):
        return True


# 🔥 IMPORTANT: unregister default User
admin.site.unregister(User)

# Register custom admins
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)


# ✨ Optional: clean admin titles
admin.site.site_header = "Blog Admin Panel"
admin.site.site_title = "Admin"
admin.site.index_title = "Manage Users and Blogs"