from langchain.tools.render import format_tool_to_openai_function
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from chatbot.models import Account, Contact, Opportunity, Lead, ToDoItem
from django.core.serializers import serialize
from typing import Dict
from chatbot.models import Contact
import json
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from typing import Optional


class TemperatureInput(BaseModel):
    country: str = Field(description="Country for which we have to fetch weather")


@tool(args_schema=TemperatureInput)
def get_temperature(country: str) -> int:
    """Get weather data of any location with latitude and longitude"""
    return 85


class DjangoOrmQueryInput(BaseModel):
    django_orm_query: str = Field(
        description="""
    This is the django orm query code.
    example1 - 'Account.objects.filter()'
    """
    )


def django_db_connect(django_orm_query: str) -> str:
    """
    This function is usefull for connecting to db with django orm.
    We have four models 'Account', 'Contact', 'Opportunity', 'Lead'.

    function: ```
    from django.core.serializers import serialize

    result = eval(query)
    return serialize('json',result)
    ```

    # example1
    user question: Give me details about Amy from contacts
    django_orm_query: Contact.objects.filter(first_name__icontains='Amy')
    assistant: see the result from function and if there is only one person named Amy in contacts then call the 'django_db_connect' function again
    django_orm_query: Contact.objects.filter(first_name__icontains='Amy').get()
    final result: {{result from the function}}
    """
    try:

        result = eval(django_orm_query)
        return serialize("json", result)

    except Exception as e:
        return f"Some error as occurred error: {e}"


class GetContactCardInput(BaseModel):
    id: int = Field(description="This is the id of the person in contact.")


@tool(args_schema=GetContactCardInput)
def get_contact_card(id: int) -> Dict:
    """
    This function takes the id of a contact person and gives contact card details of that person.
    """
    contact = (
        Contact.objects.filter(id=id)
        .values(
            "first_name",
            "last_name",
            "title",
            "account__name",
            "phone_numbers",
            "email_address",
            "linkedin_profile",
            "mailing_address",
        )
        .last()
    )
    return contact


class SendAccountCardInput(BaseModel):
    id: int = Field(description="This is the id of the person in Account csv.")


@tool(args_schema=SendAccountCardInput)
def send_account_card(id: int) -> str:
    """
    This function takes the id of a person from account csv and sends 'account card' of that particular person from account to the user.
    """
    account = Account.objects.filter(id=id).values("first_name", "last_name").last()
    return json.dumps(account)


class sendCreateLeadCardInput(BaseModel):
    pass


@tool(args_schema=sendCreateLeadCardInput)
def send_create_lead_card() -> str:
    """
    This function sends the ui card to the user that creates a lead to the database.
    """
    return "Successfully sent create lead card to user."


class sendEmailInput(BaseModel):
    recipient_email: Optional[str] = Field(
        description="This is the field for recipient's email"
    )
    message: Optional[str] = Field(
        description="This field is for message that needs to be sent through email"
    )
    subject: Optional[str] = Field(description="This field is the subject of the email")


@tool(args_schema=sendEmailInput)
def send_email_card(recipient_email=None, message=None, subject=None) -> str:
    """
    This function is used to send email card to the user.
    The card has 3 input fields 'recipient_email', 'message', 'subject'.
    This fields are not required , fill it according to the users query.
    If user just asks the email card then trigger this function without giving any parameters.

    """

    try:

        return {
            "recipient_email": recipient_email,
            "message": message,
            "subject": subject,
        }

    except Exception as e:
        return f"Failed to send email card, error {e}"


class TodoListInputs(BaseModel):
    user_id: int = Field(
        description="This is the user's id which will be used to create todoitem in the database"
    )
    title: str = Field(description="This field takes title of the todo item")
    description: Optional[str] = Field(
        description="This field is the decription of the todolist "
    )


@tool(args_schema=TodoListInputs)
def create_todoitem(user_id, title, description="") -> str:
    """
    This function is used for creating a todo item.
    This function cannot be used to delete or get todoitems.

    """
    try:

        ToDoItem.objects.create(user_id=user_id, title=title, description=description)

        return "Todo item is created successfully"

    except Exception as e:
        print(e)
        return f"Failed to create todo item. error {e}"
