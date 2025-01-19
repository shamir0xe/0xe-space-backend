from src.orchestrators.backbone_server import BackboneServer
from src.models.general import General
from src.repositories.general_repository import GeneralRepository
from src.types.email_templates import EmailTemplates


class EmailFacade:
    @staticmethod
    def send(email: str, template: EmailTemplates, **kwargs) -> str:
        """Delegate the sending email to the email-sender server"""
        # Read the required template
        general, _ = GeneralRepository(General).read_by_key(template.value)
        body = general.value
        title = ""
        if template is EmailTemplates.VERIFICATION_CODE:
            if not "code" in kwargs:
                raise Exception("Need to provide code as an argument")
            code = kwargs["code"]
            body = body.format(code)
            title = "Verification Code"
        response = BackboneServer().send_mail(email=email, body=body, title=title)
        if response.status == 200:
            return "Sent Successfully"
        # Failed
        return f"Failure: {response.message}"
