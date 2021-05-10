import os

envsettings = os.getenv("settings")

if envsettings in ["dev", "default"]:
    from core.settings.devsettings import DevSettings
    settings = DevSettings()

elif envsettings == "prod":
    from core.settings.prodsettings import ProdSettings
    settings= ProdSettings()

else:
    from core.settings.settings import BaseConfig
    settings = BaseConfig()


