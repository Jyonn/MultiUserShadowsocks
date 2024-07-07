""" Adel Liu 180111

系统配置类
"""
from SmartDjango import models, E


@E.register(id_processor=E.idp_cls_prefix())
class ConfigError:
    CREATE = E("更新配置错误", hc=500)
    NOT_FOUND = E("不存在的配置", hc=404)


class Config(models.Model):
    """
    系统配置，如七牛密钥等
    """
    key = models.CharField(
        max_length=255,
        unique=True,
    )
    value = models.CharField(
        max_length=255,
    )

    @classmethod
    def get_config_by_key(cls, key):
        try:
            return cls.objects.get(key=key)
        except cls.DoesNotExist as err:
            raise ConfigError.NOT_FOUND(debug_message=err)

    @classmethod
    def get_value_by_key(cls, key, default=None):
        try:
            config = cls.get_config_by_key(key)
            return config.value
        except Exception:
            return default

    @classmethod
    def update_value(cls, key, value):
        try:
            config = cls.get_config_by_key(key)
            config.value = value
            config.save()
        except E as e:
            if e.eis(ConfigError.NOT_FOUND):
                try:
                    config = cls(
                        key=key,
                        value=value,
                    )
                    config.save()
                except Exception:
                    raise ConfigError.CREATE
            else:
                raise ConfigError.CREATE


class ConfigInstance:
    JWT_ENCODE_ALGO = 'jwt-encode-algo'
    PROJECT_SECRET_KEY = 'project-secret-key'

    QITIAN_APP_ID = 'qt-app-id'
    QITIAN_APP_SECRET = 'qt-app-secret'


CI = ConfigInstance
