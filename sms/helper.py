def format_phone_number(input_number):
    # Remove any hyphens and spaces from the input number
    cleaned_number = input_number.replace('-', '').replace(' ', '')

    # Check if the cleaned number starts with "0" and has 10 digits
    if cleaned_number.startswith('0') and len(cleaned_number) == 10:
        # Add the country code "+254" and remove the leading "0"
        formatted_number = "+254" + cleaned_number[1:]
        return formatted_number
    else:
        # Return the original input if it doesn't match the expected format
        return input_number


def sentence_case(input_string):
    # Split the input string into words
    words = input_string.split()

    # Initialize an empty list to store the modified words
    modified_words = []

    for word in words:
        # Convert the first character to uppercase and the rest to lowercase
        modified_word = word[0].upper() + word[1:].lower()
        modified_words.append(modified_word)

    # Join the modified words into a sentence
    result = ' '.join(modified_words)

    return result