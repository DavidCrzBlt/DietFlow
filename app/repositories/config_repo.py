from sqlalchemy.orm import Session
from models.plan import Configuracion
from typing import Optional

CONFIG_KEY_SHOPPING_LIST = "tasklist_id_shopping_list"

class ConfigRepository:
    def __init__(self, db: Session):
        self.db = db

    def _get_config(self, clave: str) -> Optional[Configuracion]:
        return self.db.query(Configuracion).filter(Configuracion.clave == clave).first()

    def get_shopping_list_task_id(self) -> Optional[str]:
        config = self._get_config(CONFIG_KEY_SHOPPING_LIST)
        return config.valor if config else None

    def save_shopping_list_task_id(self, tasklist_id: str):
        config = self._get_config(CONFIG_KEY_SHOPPING_LIST)
        if config:
            config.valor = tasklist_id
        else:
            config = Configuracion(clave=CONFIG_KEY_SHOPPING_LIST, valor=tasklist_id)
            self.db.add(config)
        # El servicio que nos llame se encargará del db.commit()