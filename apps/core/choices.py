from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class SupportSubjectChoices(TextChoices):
    GENERAL = "general", _("General")
    TECHNICAL = "technical", _("Technical")
    BILLING = "billing", _("Billing")
    OTHER = "other", _("Other")


class CurrencyChoices(TextChoices):
    USD = "usd", _("USD")
    EUR = "eur", _("EUR")
    AZN = "azn", _("AZN")


class GenderChoices(TextChoices):
    """
    A class that represents the choices for gender.
    """

    MALE = "ml", _("Male")
    FEMALE = "fl", _("Female")


class SpecialityChoices(TextChoices):
    """
    A class that represents the choices for specialization.
    """

    BACKEND = "backend", _("Backend")
    FRONTEND = "frontend", _("Frontend")
    DEVOPS = "devops", _("DevOps")


class LevelChoices(TextChoices):
    """
    A class that represents the choices for experience level.
    """

    JUNIOR = "junior", _("Junior")
    MIDDLE = "middle", _("Middle")
    SENIOR = "senior", _("Senior")


class LearnChoices(TextChoices):
    """
    A class that represents the choices for learning options.
    """

    PYTHON = "python", _("Python")
    DJANGO = "django", _("Django")
    JAVASCRIPT = "javascript", _("JavaScript")
    REACT = "react", _("React")
    ANGULAR = "angular", _("Angular")
    VUE = "vue", _("Vue")
    FLUTTER = "flutter", _("Flutter")
    DART = "dart", _("Dart")
    IOS = "ios", _("iOS")
    ANDROID = "android", _("Android")


class DifficultyLevels(TextChoices):
    """
    A class that represents the choices for difficulty levels.
    """

    EASY = "easy", _("Easy")
    MIDDLE = "middle", _("Middle")
    HARD = "hard", _("Hard")


class Rating(TextChoices):
    """
    A class that represents the choices for rating.
    """

    ONE = "1", _("1")
    TWO = "2", _("2")
    THREE = "3", _("3")
    FOUR = "4", _("4")
    FIVE = "5", _("5")
