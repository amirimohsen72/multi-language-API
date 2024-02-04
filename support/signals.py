from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from support.models import TicketAnswerModel, TicketMessageModel



@receiver(post_save, sender=TicketAnswerModel)
def message_answer_post_save(sender, instance, created, **kwargs):
    if created == True:
        msg = instance.ticket
        msg.status = '2'
        msg.save()