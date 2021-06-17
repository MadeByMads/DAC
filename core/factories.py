import os

envsettings = os.getenv("settings")

if envsettings in ["dev", "default"]:
    from app.settings.devsettings import DevSettings

    settings = DevSettings()

elif envsettings == "prod":
    from app.settings.prodsettings import ProdSettings

    settings = ProdSettings()

else:
    from app.settings.settings import BaseConfig

    settings = BaseConfig()
