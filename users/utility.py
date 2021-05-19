from .models import History, User, ActivityItems


def save_history(user: User, activity: ActivityItems, desc: str = ""):
    History.objects.create(user=user, activity=activity, description=desc)
