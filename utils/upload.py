import os
import shutil


def user_avatar_path(instance, filename):
  return f'useravatars/{instance.id}/{filename}'


def user_avatar_delete_path(document):
    path = os.path.abspath(os.path.join(document.path, '../..'))
    shutil.rmtree(path)


def order_document_path(instance, filename):
    order_id = instance.id
    return f'orders/{order_id}/{filename}'


def order_delete_path(document):
    path = os.path.abspath(os.path.join(document.path, '../..'))
    shutil.rmtree(path)
