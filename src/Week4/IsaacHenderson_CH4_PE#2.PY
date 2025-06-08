#Spam mail code. writing a program that takes a list 
#of keywords found in a spam email and then checks if 
#the email that the user inputs gets a spam score. 

#first create a list of  30 keywords 
SPAM_KEYWORDS = ["make", "money", "free", "cash", "prize", "win", "award", "bonus", "gift", "reward",
                  "click", "here", "to", "claim", "your", "free", "gift", "card", "offer", "limited","Earn",
                  "act","today","hurry","urgent", "bonus","credit","check","guaranteed"]

#Makes the email all lowercase
def case_sensitive(email):
    return email.lower()

#create a function that generates a spam score based on the keywords in the email
def generate_spam_score(email):
    score = 0
    email_lower = case_sensitive(email)
    for keyword in SPAM_KEYWORDS:
        if keyword in email_lower:
            score += 1
    if score >= 3:
        return f"You have a spam score of {score}. This email is spam"
    elif score >= 2:
        return f"You have a spam score of {score}. This email is likely spam"
    elif score >= 1:
        return f"You have a spam score of {score}. This email is not spam but does contain some spam keywords"
    else:
        return f"You have a spam score of {score}. This email is not spam"

#create a function that takes an email and returns a spam score
def check_spam(email):
    return generate_spam_score(email)

def main():
    print("Welcome to the spam email checker")
    email = input("Enter an email to check for spam: ")
    result = check_spam(email)
    print(result)

if __name__ == "__main__":
    main()
    
    
