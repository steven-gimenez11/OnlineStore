from django.apps import AppConfig


class APaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_payment'

    def ready(self):
        import a_payment.hooks