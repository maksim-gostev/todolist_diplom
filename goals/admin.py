from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')
    list_filter = ('is_deleted')

class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'created', 'updated')
    search_fields = ('title', 'user')
    list_filter = ('status')

class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'created', 'updated')
    search_fields = ('user', 'goal')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
