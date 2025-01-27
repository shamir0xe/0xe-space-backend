from dataclasses import dataclass
from src.factories.base_factory import BaseFactory
from src.types.email_templates import EmailTemplates


@dataclass
class EmailTemplateKeyFactory(BaseFactory[str]):
    template: EmailTemplates

    def create(self) -> str:
        return f"email_template_{self.template.value}"
