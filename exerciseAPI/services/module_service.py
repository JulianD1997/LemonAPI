from exerciseAPI.models import Module
from exerciseAPI.schemas.module import ModuleCreate, ModuleUpdate
from exerciseAPI.services.base_service import BaseService


class ModuleService(BaseService[Module, ModuleCreate, ModuleUpdate]):
    pass


module_service = ModuleService(Module)
