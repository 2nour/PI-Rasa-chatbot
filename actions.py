
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ValidateCreditForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_credit_form"

    @staticmethod
    def credit(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        ## somme totale : salaire + 0.25 * 12 
        salaire = tracker.get_slot('salaire')
        duree = tracker.get_slot('duree')
        creditPossible = int(salaire) *0.25/12 - 12 * int(duree)
    
        return dispatcher.utter_message(text = "Montant de credit est " + str(creditPossible) + "par mois" )

    def validate_salary(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate salary value."""
        salary_int = tracker.get_slot('salaire')
        if int(salary_int) > 450 :
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"salaire": salary_int}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(template = "utter_wrong_salary")
            return {"salaire": None}
    
    def validate_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate duration value."""
        duration_int = tracker.get_slot('duree')
        if int(duration_int) > 1 and duration_int < 25 :
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"duree": duration_int}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(template = "utter_wrong_duration")
            return {"duree": None}