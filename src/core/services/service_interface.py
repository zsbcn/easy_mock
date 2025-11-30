from core.constants import InterfaceConstants
from core.exception import BusinessException
from core.models.model_interface import Interface, InterfaceCreate, InterfaceResponse
from core.services import BaseService


class InterfaceService(BaseService):
    def get_interface_list(self, project_id: str) -> list[InterfaceResponse]:
        project_list: list[Interface] = self.db.query(Interface).where(Interface.project_id == project_id).all()
        return [InterfaceResponse.model_validate(project) for project in project_list]

    def create_interface(self, interface: InterfaceCreate, user_id: str) -> None:
        interface_exist: Interface = self.db.query(Interface).where(Interface.name == interface.name,
                                                                    Interface.url == interface.url).first()
        if interface_exist:
            raise BusinessException(InterfaceConstants.INTERFACE_EXIST)
        interface_db: Interface = Interface(create_by=user_id, update_by=user_id, **interface.model_dump())
        self.db.add(interface_db)
        self.db.commit()
