import csv
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


CSV_FILE = "committee_records.csv"


class CommitteeApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        title = Label(text="🙏 Ganesh Utsav Accounts 🙏", font_size=22, size_hint=(1, 0.2))
        self.layout.add_widget(title)

        btn_add = Button(text="➕ Add Record", on_press=self.add_record_popup)
        btn_view = Button(text="📖 View Records", on_press=self.view_records)
        btn_summary = Button(text="📊 Yearly Summary", on_press=self.show_summary)

        self.layout.add_widget(btn_add)
        self.layout.add_widget(btn_view)
        self.layout.add_widget(btn_summary)

        return self.layout

    # ------------------- Add Record -------------------
    def add_record_popup(self, instance):
        layout = BoxLayout(orientation="vertical", spacing=5)

        self.name_input = TextInput(hint_text="Name / Item")
        self.amount_input = TextInput(hint_text="Amount")
        self.type_input = TextInput(hint_text="Type (Income/Expense/Item)")

        btn_save = Button(text="Save", on_press=self.save_record)

        layout.add_widget(self.name_input)
        layout.add_widget(self.amount_input)
        layout.add_widget(self.type_input)
        layout.add_widget(btn_save)

        self.popup = Popup(title="Add Record", content=layout, size_hint=(0.8, 0.6))
        self.popup.open()

    def save_record(self, instance):
        name = self.name_input.text
        amount = self.amount_input.text
        rtype = self.type_input.text

        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Name/Item", "Amount", "Type"])

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, amount, rtype])

        self.popup.dismiss()
        self.show_message("✅ Record saved successfully!")

    # ------------------- View Records -------------------
    def view_records(self, instance):
        if not os.path.exists(CSV_FILE):
            self.show_message("No records found!")
            return

        with open(CSV_FILE, "r") as f:
            data = f.read()

        popup = Popup(title="All Records", content=Label(text=data), size_hint=(0.9, 0.9))
        popup.open()

    # ------------------- Yearly Summary -------------------
    def show_summary(self, instance):
        if not os.path.exists(CSV_FILE):
            self.show_message("No records found!")
            return

        income, expense = 0, 0
        with open(CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    amt = float(row["Amount"])
                    if row["Type"].lower() == "income":
                        income += amt
                    elif row["Type"].lower() == "expense":
                        expense += amt
                except:
                    pass

        balance = income - expense
        msg = f"Income: ₹{income}\nExpense: ₹{expense}\nBalance: ₹{balance}"
        self.show_message(msg)

    # ------------------- Helper -------------------
    def show_message(self, message):
        popup = Popup(title="Info", content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()


if __name__ == "__main__":
    CommitteeApp().run()
