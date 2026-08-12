from .models import PlatformSettings, News


def platform_settings(request):
    """Добавляет настройки платформы и новости во все шаблоны."""
    settings = PlatformSettings.objects.first()
    news = News.objects.filter(is_active=True).order_by('-order', '-created_at')

    return {
        'platform_settings': settings,
        'news': news,
    }
