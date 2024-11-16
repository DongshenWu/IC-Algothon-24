import requests
pos_dict = {'strat_0': -0.1, 'strat_1': 0, 'strat_2': 0, 'strat_3': 0, 'strat_4': -0.1, 'strat_5': -0.1, 'strat_6': 0, 'strat_7': 0, 'strat_8': 0, 'strat_9': 0, 'strat_10': 0, 'strat_11': 0, 'strat_12': 0, 'strat_13': 0.1, 'strat_14': 0.1, 'strat_15': 0.1, 'strat_16': 0, 'strat_17': 0, 'strat_18': 0.1, 'strat_19': 0, 'strat_20': 0, 'strat_21': 0, 'strat_22': 0, 'strat_23': 0, 'strat_24': 0.1, 'strat_25': 0, 'strat_26': 0, 'strat_27': 0, 'strat_28': 0, 'strat_29': 0, 'strat_30': -0.1, 'strat_31': 0, 'strat_32': -0.1, 'strat_33': 0, 'strat_34': 0, 'strat_35': 0, 'strat_36': 0, 'strat_37': 0, 'strat_38': 0, 'strat_39': 0, 'strat_40': 0, 'strat_41': 0, 'team_name': 'Yoghurt', 'passcode': 'yoghurt'}


def post_to_google_form(pos_dict):
    # Google Form submission URL - replace with your form's URL
    FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeUYMkI5ce18RL2aF5C8I7mPxF7haH23VEVz7PQrvz0Do0NrQ/formResponse"
    
    # Prepare form data
    form_data = {
        "emailAddress": "dswdavid1@gmail.com",
        "entry.1985358237": str(pos_dict)
    }
    
    try:
        response = requests.post(FORM_URL, data=form_data)
        if response.status_code == 200:
            print("Form submitted successfully!")
        else:
            print(f"Failed to submit form. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error submitting form: {str(e)}")

post_to_google_form(pos_dict)