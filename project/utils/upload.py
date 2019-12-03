import os
import shutil

def avatar_path(instance, filename):
  return f'avatars/{instance.id}: {instance.username}/{filename}'

def order_document_path(instance, filename):
    order_id = instance.id
    return f'orders/{order_id}/{filename}'

def order_delete_path(document):
    path = os.path.abspath(os.path.join(document.path, '../..'))
    print(path)
    shutil.rmtree(path)
