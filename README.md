<h1>🧾 CLI Expense Tracker</h1>

A simple command-line interface (CLI) tool for tracking your personal expenses, setting monthly budgets, and exporting data — all from your terminal.

This project was built as part of the Expense Tracker Project on roadmap.sh(https://roadmap.sh/projects/expense-tracker).
<h2>📦 Features</h2>

    ✅ Add, update, delete, and list expenses

    📅 Filter by date (day, month, year, or full date)

    💸 Categorize and summarize expenses

    🧮 Set and monitor monthly budgets (with warnings)

    📤 Export expenses to a .csv file

    🧰 Fully portable: Works from anywhere if installed via .exe and added to PATH

<h2>🚀 Getting Started</h2>
<h3>1. Clone the Repository</h3>

```
git clone https://github.com/duditop10/python-expense-tracker.git
cd python-expense-tracker
```

<h3>2. Using the Python Script</h3>

Make sure you have Python 3 installed. Run it via:

```
python expenses-cli.py add --description "Coffee" --amount 3.5 --category "Food" --date 17-04-2025
```

Use --help for all commands and arguments:

```
python expenses-cli.py --help
```

<h2>🪄 Executable Version (.exe)</h2>

To make the program universally accessible from your terminal:

    Download or build the .exe version (included in the exe/ folder of the project).

    Move the .exe to a custom tools folder. We recommend:

```
C:\cli-tools
```

    Add that folder to your system's PATH environment variable:

        Search for "Environment Variables" in Windows.

        Edit PATH and add:

        C:\cli-tools

Now you can use the program from anywhere in your terminal like this:

```
expenses-cli add --description "Groceries" --amount 45 --category "Food" --date 16-04-2025
```

<h2>🧰 Command Reference</h2>
<h3>Add Expense</h3>

```
add --description "Lunch" --amount 12.5 --category "Food" --date 17-04-2025
```

<h3>Update Expense</h3>

```
update --id 1 --amount 15.0
```

<h3>Delete Expense</h3>

```
delete --id 1
```

<h3>List Expenses</h3>

```
list --month 4
```

<h3>Expense Summary</h3>

```
summary --year 2025
```

<h3>Set Budget</h3>

```
set-budget --month 4 --amount 300
```

<h3>Export to CSV</h3>

```
export
```

<h2>📁 File Locations</h2>

    C:\cli-tools\expenses-cli.json: Stores all expense entries

    C:\cli-tools\budgets.json: Stores monthly budget values

    expenses-cli.csv: Output file for CSV exports (file will be saved wherever the cmd command is executed)

<h2>🛠️ Built With</h2>

    Python standard library (argparse, json, csv, etc.)

    tabulate for clean CLI table output
