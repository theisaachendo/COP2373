# Isaac Henderson
# PE 6
# 6/29/2025
#
# Phone number validation function - accepts multiple formats without regex
# Valid formats: (xxx) xxx-xxxx, xxx-xxx-xxxx, xxx.xxx.xxxx, xxxxxxxxxx
# Area code and exchange code must start with digits 2-9

def validate_phone_number(phone):
    
    # Extract only numeric characters from input
    digits = [c for c in phone if c.isdigit()]
    if len(digits) != 10:
        return False
    
    # Convert digit list to string for validation
    phone_digits = ''.join(digits)
    
    # Validate area code and exchange code restrictions
    if phone_digits[0] in ('0', '1'):
        return False
    if phone_digits[3] in ('0', '1'):
        return False
    
    return True

def validate_ssn(ssn):
 
    # Extract only numeric characters from input
    digits = [c for c in ssn if c.isdigit()]
    if len(digits) != 9:
        return False
    
    # Convert digit list to string for validation
    ssn_digits = ''.join(digits)
    
    # Validate first three digits (area number)
    first_three = ssn_digits[:3]
    if first_three == '000' or first_three == '666' or first_three.startswith('9'):
        return False
    
    # Validate middle two digits (group number)
    middle_two = ssn_digits[3:5]
    if middle_two == '00':
        return False
    
    # Validate last four digits (serial number)
    last_four = ssn_digits[5:]
    if last_four == '0000':
        return False
    
    return True

def validate_zip_code(zip_code):
  
    # Validate length for 5-digit or 9-digit ZIP codes
    if len(zip_code) not in (5, 10):
        return False
    
    if len(zip_code) == 5:
        # Verify all characters are digits for 5-digit format
        return all(c.isdigit() for c in zip_code)
    else:
        # Validate 9-digit format: 5 digits + hyphen + 4 digits
        if zip_code[5] != '-':
            return False
        return all(c.isdigit() for c in zip_code[:5]) and all(c.isdigit() for c in zip_code[6:])

def main():
    print("Please enter the following information:")
    
    # Get and validate phone number
    phone = input("Phone number (format: (123) 456-7890, 123-456-7890, 123.456.7890, or 1234567890): ")
    print(f"Phone number {phone} is {'valid' if validate_phone_number(phone) else 'invalid'}.")
    
    # Get and validate SSN
    ssn = input("Social Security Number (format: xxx-xx-xxxx): ")
    print(f"SSN {ssn} is {'valid' if validate_ssn(ssn) else 'invalid'}.")
    
    # Get and validate zip code
    zip_code = input("Zip code (format: xxxxx or xxxxx-xxxx): ")
    print(f"Zip code {zip_code} is {'valid' if validate_zip_code(zip_code) else 'invalid'}.")

if __name__ == "__main__":
    main()