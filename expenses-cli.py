import datetime
import argparse
import json
import os
import sys
import csv
from tabulate import tabulate
from datetime import datetime as dt



class redundantArgument(Exception): pass
class nonExistentId(Exception): pass
class nothingToUpdate(Exception): pass
class negativeAmount(Exception): pass
class invalidDate(Exception): pass



EXPENSE_FILE = 'C:\\cli-tools\\expenses-cli.json'
BUDGET_FILE = 'C:\\cli-tools\\budgets.json'
CSV_FILE = 'expenses-cli.csv'



def custom_excepthook(exctype, value, traceback):
    print(f"{exctype.__name__}: {value}")
sys.excepthook = custom_excepthook



def parse_date(date_str):
    return dt.strptime(date_str, "%d-%m-%Y")

def get_date_parts(date_input):
    date = parse_date(date_input) if date_input else dt.today()
    return date.day, date.month, date.year

def validate_date_fields(day=None, month=None):
    if month and not (1 <= month <= 12):
        raise invalidDate("Invalid month. Must be between 1 and 12.")
    if day and not (1 <= day <= 31):
        raise invalidDate("Invalid day. Must be between 1 and 31.")

def validate_amount(amount):
    if amount is not None and amount < 0:
        raise negativeAmount("Amount must be positive.")

def check_redundant_date(args):
    if args.date and (args.day or args.month or args.year):
        raise redundantArgument("Use either --date or --day/--month/--year, not both.")

def load_json(filepath, default):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    else:
        with open(filepath, "x") as f:
            return default

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)



def load_budgets():
    return load_json(BUDGET_FILE, {})

def save_budgets(budgets):
    save_json(BUDGET_FILE, budgets)

def check_budget_warning(expense, expenses):
    budgets = load_budgets()
    budget = budgets.get(str(expense['month']))
    if budget is not None:
        total = sum(e['amount'] for e in expenses if e['month'] == expense['month'] and e['year'] == expense['year'])
        if total > budget:
            print(f"Warning: Budget exceeded for month {expense['month']} "
                  f"(${total:.2f} spent, budget was ${budget:.2f})")



def load_file():
    return load_json(EXPENSE_FILE, [])

def save_file(expenses):
    save_json(EXPENSE_FILE, expenses)



def create_arguments(parser):
    parser.add_argument('--description', help="Description of the expense")
    parser.add_argument('--amount', type=float, help="Amount of the expense")
    parser.add_argument('--month', type=int, help="Month of the expense")
    parser.add_argument('--day', type=int, help="Day of the expense")
    parser.add_argument('--year', type=int, help="Year of the expense")
    parser.add_argument('--date', help="Date of the expense (DD-MM-YYYY)")
    parser.add_argument('--category', help="Category of expense")

def create_commands(parser):
    subparsers = parser.add_subparsers(dest='command')


    add = subparsers.add_parser('add', help='Add expense')
    add.add_argument('--description', required=True)
    add.add_argument('--amount', type=float, required=True)
    add.add_argument('--category')
    add.add_argument('--date')


    update = subparsers.add_parser('update', help='Update an expense')
    update.add_argument('--id', type=int, required=True)
    create_arguments(update)


    delete = subparsers.add_parser('delete', help='Delete an expense')
    delete.add_argument('--id', type=int, required=True)


    list_cmd = subparsers.add_parser('list', help='List expenses')
    create_arguments(list_cmd)


    summary = subparsers.add_parser('summary', help='Summarize expenses')
    create_arguments(summary)


    set_budget = subparsers.add_parser('set-budget', help='Set a monthly budget')
    set_budget.add_argument('--month', type=int, required=True)
    set_budget.add_argument('--amount', type=float, required=True)


    subparsers.add_parser('export', help='Export expenses to CSV')



def add(args, expenses):
    validate_amount(args.amount)
    day, month, year = get_date_parts(args.date)
    new_id = expenses[-1]['id'] + 1 if expenses else 1
    category = args.category or 'No category'
    
    expense = {
        "id": new_id,
        "description": args.description,
        "amount": args.amount,
        "category": category,
        "day": day,
        "month": month,
        "year": year
    }
    expenses.append(expense)
    check_budget_warning(expense, expenses)
    save_file(expenses)
    print(f"Added: {args.description} (${args.amount:.2f}), ID={new_id}")

def update(args, expenses):
    validate_date_fields(args.day, args.month)
    validate_amount(args.amount)
    check_redundant_date(args)

    for expense in expenses:
        if expense['id'] == args.id:
            updated = False
            if args.description: expense['description'], updated = args.description, True
            if args.amount:
                expense['amount'], updated = args.amount, True
                check_budget_warning(expense, expenses)
            if args.category: expense['category'], updated = args.category, True
            if args.date:
                day, month, year = get_date_parts(args.date)
                expense.update({"day": day, "month": month, "year": year})
                updated = True
            if args.day: expense['day'], updated = args.day, True
            if args.month: expense['month'], updated = args.month, True
            if args.year: expense['year'], updated = args.year, True

            if updated:
                save_file(expenses)
                print(f"Updated expense ID {args.id}")
                return
            else:
                raise nothingToUpdate("No changes were made.")
    raise nonExistentId("Expense ID not found.")

def delete(args, expenses):
    for expense in expenses:
        if expense['id'] == args.id:
            expenses.remove(expense)
            save_file(expenses)
            print(f"Deleted expense ID {args.id} - {expense['description']}")
            return
    raise nonExistentId("Expense ID not found.")

def list_expenses(args, expenses):
    validate_date_fields(args.day, args.month)
    validate_amount(args.amount)
    check_redundant_date(args)

    filtered = []
    for exp in expenses:
        if args.date:
            day, month, year = get_date_parts(args.date)
            match = (exp['day'], exp['month'], exp['year']) == (day, month, year)
        else:
            match = all([
                not args.day or exp['day'] == args.day,
                not args.month or exp['month'] == args.month,
                not args.year or exp['year'] == args.year
            ])
        match = match and all([
            not args.amount or exp['amount'] == args.amount,
            not args.description or exp['description'] == args.description,
            not args.category or exp['category'] == args.category
        ])
        if match:
            filtered.append([
                exp['id'],
                f"{exp['day']:02}-{exp['month']:02}-{exp['year']}",
                exp['description'],
                exp['category'],
                f"${exp['amount']:.2f}"
            ])
    print(tabulate(filtered, headers=["ID", "Date", "Description", "Category", "Amount"]))

def summary(args, expenses):
    validate_date_fields(args.day, args.month)
    validate_amount(args.amount)
    check_redundant_date(args)

    total = 0
    for exp in expenses:
        if args.date:
            day, month, year = get_date_parts(args.date)
            match = (exp['day'], exp['month'], exp['year']) == (day, month, year)
        else:
            match = all([
                not args.day or exp['day'] == args.day,
                not args.month or exp['month'] == args.month,
                not args.year or exp['year'] == args.year
            ])
        match = match and all([
            not args.amount or exp['amount'] == args.amount,
            not args.description or exp['description'] == args.description,
            not args.category or exp['category'] == args.category
        ])
        if match:
            total += exp['amount']

    print(f"${total:.2f} total expenses for selected criteria.")

def set_budget(args):
    validate_date_fields(month=args.month)
    budgets = load_budgets()
    budgets[str(args.month)] = args.amount
    save_budgets(budgets)
    print(f"Budget for month {args.month} set to ${args.amount:.2f}")

def export(_, expenses):
    if not expenses:
        print("No expenses to export.")
        return
    keys = expenses[0].keys()
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(expenses)
    print("Expenses exported to CSV.")


def main():
    expenses = load_file()
    parser = argparse.ArgumentParser(description='Simple CLI Expense Tracker')
    create_commands(parser)
    args = parser.parse_args()

    match args.command:
        case 'add': add(args, expenses)
        case 'update': update(args, expenses)
        case 'delete': delete(args, expenses)
        case 'list': list_expenses(args, expenses)
        case 'summary': summary(args, expenses)
        case 'set-budget': set_budget(args)
        case 'export': export(args, expenses)

if __name__ == '__main__':
    main()