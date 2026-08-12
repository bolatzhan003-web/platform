from .models import PlatformSettings


def platform_settings(request):
    """Добавляет настройки платформы во все шаблоны."""
    settings = PlatformSettings.objects.first()
    return {
        'platform_settings': settings,
    }
