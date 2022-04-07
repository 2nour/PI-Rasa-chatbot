from typing import Any, Text, Dict, List ## Datatypes

from rasa_sdk import Action, Tracker  ##
from rasa_sdk.executor import CollectingDispatcher


from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class PossibleCreditAction(Action):
    def name(self) -> Text:
        return "action_possible_credit"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        ## somme totale : salaire + 0.25 * 12 
        salary = tracker.get_slot("salary")
        duration = tracker.get_slot("duration")
        possiblecredit = int(salary) * 12 * int(duration) * 0.9 * 0.3
        dispatcher.utter_message(text = "Possible credit amount is  " + str(possiblecredit) )
        return []

