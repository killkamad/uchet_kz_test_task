from django.core.mail import send_mail
from test_uchet_kz.celery import app
from test_uchet_kz.settings import EMAIL_HOST_USER
from todolist.models import Task


@app.task
def send_email_done_status_changed(old_done_status, new_done_status, task_id):
    task = Task.objects.get(id=task_id)
    header_text = f'Статус задачи был изменен с {old_done_status} на {new_done_status}'
    msg_text = f'Заголовок задачи: {task.header}\n' \
               f'Описание задачи: {task.description}\n' \
               f'Срок исполнения: {task.deadline}\n' \
               f'Выполнено: {task.done}'
    send_mail(
        header_text,
        msg_text,
        EMAIL_HOST_USER,
        [task.user.email],
        fail_silently=False,
    )


@app.task
def send_email_reset_password(url, domain, email):
    header_text = 'Сбросить свой пароль'
    msg_text = f'Для того чтобы сбросить свой пароль:\n' \
               f'1) Проверьте статус ссылки: {url}\n' \
               f'2) После проверки воспользуйтесь ссылкой: {domain}/password-reset-complete/ \n' \
               f'В json укажите {{"password": "new-password", "token": "token из предыдущей ссылки", ' \
               f'"uidb64": "uidb64 из предыдущей ссылки"}}'
    send_mail(
        header_text,
        msg_text,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
