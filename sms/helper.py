def format_phone_number(input_number):
    # Remove any hyphens and spaces from the input number
    cleaned_number = input_number.replace('-', '').replace(' ', '')

    # Check if the cleaned number starts with "0" and has 10 digits
    if cleaned_number.startswith('0') and len(cleaned_number) == 10:
        # Add the country code "+254" and remove the leading "0"
        formatted_number = "+254" + cleaned_number[1:]
        return formatted_number
    else:
        # Return None if it doesn't match the expected format
        return None
 

def sentence_case_first_name(input_string):
    # Split the input string into words
    words = input_string.split()

    # Pick the first word
    first_name = words[0]

    # Convert the first character to uppercase and the rest to lowercase
    modified_first_name = first_name[0].upper() + first_name[1:].lower()

    return modified_first_name
