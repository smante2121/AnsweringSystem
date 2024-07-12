import re


'''def extract_callback_number(buffer):
    # Remove all non-numeric characters except spaces
    cleaned_buffer = re.sub(r'[^\d\s]', '', buffer)
    # Normalize by replacing multiple spaces with a single space and then removing spaces
    cleaned_buffer = re.sub(r'\s+', '', cleaned_buffer)

    # Find all 10-digit sequences in the cleaned buffer
    matches = re.findall(r'\d{10}', cleaned_buffer)

    if matches:
        # Return the first valid 10-digit phone number formatted correctly
        first_match = matches[0]
        formatted_number = f"({first_match[:3]}) {first_match[3:6]}-{first_match[6:]}"
        return formatted_number

    return None'''
def extract_callback_number(buffer):
    # Extract all sequences of digits from the buffer
    digit_sequences = re.findall(r'\d+', buffer)
    # Join all sequences of digits into a single string
    joined_digits = ''.join(digit_sequences)

    # Find all 10-digit sequences in the joined digits
    matches = re.findall(r'\d{10}', joined_digits)

    if matches:
        # Return the first valid 10-digit phone number formatted correctly
        first_match = matches[0]
        formatted_number = f"({first_match[:3]}) {first_match[3:6]}-{first_match[6:]}"
        return formatted_number

    return None


def extract_is_patient(buffer): # method to extract if the caller is the patient
    positive_responses = [
        "yes", "yeah", "i'm the patient", "i am the patient", "yep", "yup", "affirmative", "i am",
    ]

    negative_responses = [
        "no", "nope", "negative", "not the patient", "i am not", "i'm not", "i am not the patient", "i'm not the patient"
    ]
    buffer = buffer.lower() # convert buffer to lowercase for case-insensitive matching

    for response in positive_responses: # check for positive responses
        pattern = rf'\b{re.escape(response)}\b'
        match = re.search(pattern, buffer, re.IGNORECASE)
        if match:
            return "yes"

    for response in negative_responses: # check for negative responses
        pattern = rf'\b{re.escape(response)}\b'
        match = re.search(pattern, buffer, re.IGNORECASE)
        if match:
            return "no"

    return None

def extract_date_of_birth(buffer): # method to extract date of birth
    month_to_number = { # dictionary to map month names to month numbers
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }

    # Handle numerical date formats (e.g., 6/21/2003 or 6,212,003)
    match = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b', buffer)
    if match:
        month, day, year = match.groups()
        return f"{int(month)}/{int(day)}/{year}"

    match = re.search(r'\b(\d{1,2}),\s?(\d{1,3}),\s?(\d{1,4})\b', buffer)
    if match:
        month, day, year = match.groups() # extract month, day, and year
        if len(day) == 1 and len(year) == 4:
            return f"{int(month)}/{int(day)}/{year}"
        elif len(day) == 3 and day[1] == '1' and day[2] == '2':
            return f"{int(month)}/21/{year}"
        else:
            return f"{int(month)}/{int(day)}/{year}" # return formatted date

    # Handle month-day-year with possible ordinal suffixes and optional comma (e.g., June 21st, 2003)
    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(st|nd|rd|th)?,?\s+(\d{4})\b', buffer, re.IGNORECASE)
    if match: # extract month, day, and year
        month, day, _, year = match.groups()
        month_number = month_to_number[month.lower()]
        return f"{int(month_number)}/{int(day)}/{year}"

    # Handle more generic month-day-year formats without explicit separators (e.g., June 21 2003)
    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\s+(\d{4})\b', buffer, re.IGNORECASE)
    if match: # extract month, day, and year
        month, day, year = match.groups()
        month_number = month_to_number[month.lower()]
        return f"{int(month_number)}/{int(day)}/{year}"

    # Handle compact numeric dates without separators (e.g., 6212003)
    match = re.search(r'\b(\d{1})(\d{2})(\d{4})\b', buffer)
    if match: # extract month, day, and year
        month, day, year = match.groups()
        if year[0] in ['1', '2']:
            return f"{int(month)}/{int(day)}/{year}"

    return None



def extract_gender(buffer):
    male_pattern = r'\b(male|boy|man)\b'
    female_pattern = r'\b(female|girl|woman)\b'

    # Look for patterns in both the question and the response
    male_matches_question = re.findall(male_pattern, buffer[:100], re.IGNORECASE)  # Limit to first 100 characters
    female_matches_question = re.findall(female_pattern, buffer[:100], re.IGNORECASE)

    male_matches_response = re.findall(male_pattern, buffer[100:], re.IGNORECASE)  # Check beyond first 100 characters
    female_matches_response = re.findall(female_pattern, buffer[100:], re.IGNORECASE)

    # Allow double positives of the same gender but not both genders
    if (male_matches_question and male_matches_response) or (female_matches_question and female_matches_response):
        return None
    elif female_matches_question or female_matches_response:
        return "female"
    elif male_matches_question or male_matches_response:
        return "male"

    return None





def extract_state(buffer): # method to extract the state LOCATION
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
              "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
              "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
              "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
              "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
              "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
              "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    for state in states: # check for each state in the list
        if re.search(r'\b' + re.escape(state) + r'\b', buffer, re.IGNORECASE):
            return state
    return None

def extract_symptom(buffer): # method to extract the reason for the call
    pattern = r'reason for the call today\.\s*(.*?)[.]'
    match = re.search(pattern, buffer, re.IGNORECASE)
    if match:
        response = match.group(1).strip()
        return response
    return None
