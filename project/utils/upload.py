def avatar_path(instance, filename):
  return f'avatars/{instance.id}: {instance.username}/{filename}'