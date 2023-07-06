from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')

class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'created', 'updated')
    search_fields = ('title', 'user')

class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'created', 'updated')
    search_fields = ('user', 'goal')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
