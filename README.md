🧾 CLI Expense Tracker

A simple command-line interface (CLI) tool for tracking your personal expenses, setting monthly budgets, and exporting data — all from your terminal.

This project was built as part of the Expense Tracker Project on roadmap.sh.
📦 Features

    ✅ Add, update, delete, and list expenses

    📅 Filter by date (day, month, year, or full date)

    💸 Categorize and summarize expenses

    🧮 Set and monitor monthly budgets (with warnings)

    📤 Export expenses to a .csv file

    🧰 Fully portable: Works from anywhere if installed via .exe and added to PATH

🚀 Getting Started
1. Clone the Repository

git clone https://github.com/yourusername/expense-tracker-cli.git
cd expense-tracker-cli

2. Using the Python Script

Make sure you have Python 3 installed. Run it via:

python expenses-cli.py add --description "Coffee" --amount 3.5 --category "Food" --date 17-04-2025

Use --help for all commands and arguments:

python expenses.py --help

🪄 Executable Version (.exe)

To make the program universally accessible from your terminal:

    Download or build the .exe version (included in the exe/ folder of the project).

    Move the .exe to a custom tools folder. We recommend:

C:\cli-tools

    Add that folder to your system's PATH environment variable:

        Search for "Environment Variables" in Windows.

        Edit PATH and add:

        C:\cli-tools

    

Now you can use the program from anywhere in your terminal like this:

expenses-cli add --description "Groceries" --amount 45 --category "Food" --date 16-04-2025

🧰 Command Reference
Add Expense

add --description "Lunch" --amount 12.5 --category "Food" --date 17-04-2025

Update Expense

update --id 1 --amount 15.0

Delete Expense

delete --id 1

List Expenses

list --month 4

Expense Summary

summary --year 2025

Set Budget

set-budget --month 4 --amount 300

Export to CSV

export

📁 File Locations

    C:\cli-tools\expenses-cli.json: Stores all expense entries

    C:\cli-tools\budgets.json: Stores monthly budget values

    expenses-cli.csv: Output file for CSV exports (file will be saved wherever the cmd command is executed)

🛠️ Built With

    Python standard library (argparse, json, csv, etc.)

    tabulate for clean CLI table output