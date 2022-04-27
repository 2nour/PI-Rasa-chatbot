version: "2.0"
stories:
- story: nouveau_compte1
  steps:
  - intent: salut
  - action: utter_salut
  - action: utter_assister
  - intent: nouveau_compte
  - action: utter_ask_name
  - intent: name
    entities:
    - name: 'nour hadrich'
  - slot_was_set:
    - name: 'nour hadrich'
  - action: utter_ask_idcard
  - intent: idcard
    entities:
    - idcard: '13014562'
  - slot_was_set:
    - idcard: '13014562'
  - action: utter_ask_email
  - intent: email
    entities:
    - email: 'nourhadrich@gmail.com'
  - slot_was_set:
    - email: 'nourhadrich@gmail.com'
  - action: utter_ask_birthdate
  - intent: birthdate
    entities:
    - birthdate: '2000-02-02'
  - slot_was_set:
    - birthdate: '2000-02-02'
  - action: utter_ask_phonenumber
  - intent: phonenumber
    entities:
    - phonenumber: '20052552'
  - slot_was_set:
    - phonenumber: '20052552'
  - action: utter_ask_address
  - intent: address
    entities:
    - address: 'lafayette'
  - slot_was_set:
    - address: 'lafayette'
  - action: utter_ask_login
  - intent: login
    entities:
    - login: 'nourhadrich'
  - slot_was_set:
    - login: 'nourhadrich'
  - action: utter_ask_password
  - intent: password
    entities:
    - password: '2000-02-02'
  - slot_was_set:
    - password: '2000-02-02'
  - action: action_create_account
  
  
  
