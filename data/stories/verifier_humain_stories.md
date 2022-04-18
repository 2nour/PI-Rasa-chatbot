
version: "2.0"
stories:
- story: interactive_story_1
  steps:
  - intent: salut
  - action: utter_salut
  - action: utter_assister
  - intent: verifier_humain
  - action: utter_verifier_humain
  

