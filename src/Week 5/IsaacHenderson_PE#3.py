from functools import reduce

#Write a program that asks the user for a list of their montly expenses . when asking, ask for the type of expense and the amount 
#use the reduce method to analyxe the expenses and display the total expense, the highest nad the lowest expense
#You can use separate functions for your calculations or you can use lambda functions within your main function to do this. 

def main():
    expenses = []
    while True:
        expense_type = input("Enter the type of expense: ")
        expense_amount = input("Enter the amount (ENTER done to finish): ")
        if expense_amount.lower() == "done":
            break
        expenses.append((expense_type, float(expense_amount)))

    total_expense = reduce(lambda x, y: x + y[1], expenses, 0)

    highest_expense = max(expenses, key=lambda x: x[1])
    lowest_expense = min(expenses, key=lambda x: x[1])

    print(f"Total expense: {total_expense}")
    print(f"Highest expense: {highest_expense}")
    print(f"Lowest expense: {lowest_expense}")

if __name__ == "__main__":
    main()