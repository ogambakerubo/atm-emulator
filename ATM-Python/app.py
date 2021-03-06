import re

from models.accounts import Account
# from models.transactions import Transaction

acc = Account()
acc.add_account("trial", "0000", 1000, 0)
acc.add_account("mary", "1111", 1000000, 10000)
acc.add_account("tom", "2222", 140000, 2000)


def main_menu():
    while True:
        print('''
                ****************************************************************************
                *                                                                          *
                *                  Welcome to Valued Customer to Bank X                    *
                *                                                                          *
                ****************************************************************************
        ''')

        acc_username = input("\nEnter your account username: ")
        acc_username = acc_username.strip().lower()
        while not re.match("^[a-z]{1,15}$", acc_username):
            print("Error! Only up to 15 characters allowed!")
            acc_username = input('\nEnter your account username: ')
            acc_username = acc_username.lower().strip()

        pin = input('\nEnter your account pin: ')
        pin = pin.lower().strip()
        while not re.match("^[0-9]{4}$", pin):
            print("Error! Only 4 characters allowed!")
            pin = input('\nEnter your account pin: ')
            pin = pin.lower().strip()

        account = acc.get_account_by_username(acc_username)

        if len(account) > 0:
            if account[0]["pin"] == pin:
                accountId = account[0]["accountId"]
                # Iterating over account session
                while True:

                    # Printing menu
                    print("---------------------------------------")
                    print(
                        "\nMENU: \n1 - View Balance \n2 - Withdraw \n3 - Deposit \n4 - Transaction History \n5 - Change Account Details \n6 - Transfer money \n7 - Exit")
                    print("---------------------------------------")

                    # Reading selection
                    selection = int(input("\nEnter your selection: "))
                    while not re.match("^[1-7]{1}$", str(selection)):
                        print("---------------------------------------")
                        print(
                            "\nPlease select a number from the menu: \n1 - View Balance \n2 - Withdraw \n3 - Deposit \n4 - Transaction History \n5 - Change Account Details \n6 - Transfer money \n7 - Exit")
                        print("---------------------------------------")
                        selection = int(input("\nEnter your selection: "))

                    # View Balance
                    if selection == 1:
                        # Printing balance
                        print("Your balance is: ")
                        print("---------------------------------------")
                        print(account[0]["balance"])

                    # Withdraw
                    elif selection == 2:
                        # Reading amount
                        amt = input("\nEnter amount to withdraw: ")
                        while not re.match("^[0-9]*$", amt):
                            print("Error! Only number characters allowed!")
                            amt = input('\nEnter amount to withdraw: ')
                        amt = float(amt)

                        currency = input("\nEnter currency, KSH or USD: ")
                        while currency != "KSH" and currency != "USD":
                            currency = input(
                                "\nInvalid choice. Try again, KSH or USD: ")

                        print("---------------------------------------")

                        verify_withdraw = input(
                            "Is this the correct amount, Y or N ? " + currency + " " + str(amt) + ": ")
                        while verify_withdraw != "Y" and verify_withdraw != "y" and verify_withdraw != "N" and verify_withdraw != "n":
                            verify_withdraw = input(
                                "\nInvalid choice. Try again. Is this the correct amount, Y or N ? " + currency + " " + str(amt) + ": ")

                        if verify_withdraw == "Y" or verify_withdraw == "y":
                            print("Verify withdrawal\n")
                            session = acc.transaction_details(
                                amt, "Withdrawal", currency, accountId)
                            # Printing updated balance
                            print("---------------------------------------")
                            print(session)
                        else:
                            break

                    # Deposit
                    elif selection == 3:
                        # Reading amount
                        amt = input("\nEnter amount to deposit: ")
                        while not re.match("^[0-9]*$", amt):
                            print("Error! Only number characters allowed!")
                            amt = input('\nEnter amount to deposit: ')
                        amt = float(amt)

                        currency = input("\nEnter currency, KSH or USD: ")
                        while not currency == "KSH" and not currency == "USD":
                            currency = input(
                                "\nInvalid choice. Try again, KSH or USD: ")

                        print("---------------------------------------")

                        verify_deposit = input(
                            "Is this the correct amount, Y or N ? " + currency + " " + str(amt) + ": ")
                        while verify_deposit != "Y" and verify_deposit != "y" and verify_deposit != "N" and verify_deposit != "n":
                            verify_deposit = input(
                                "\nInvalid choice. Try again. Is this the correct amount, Y or N ? " + currency + " " + str(amt) + ": ")

                        if verify_deposit == "Y" or verify_deposit == "y":
                            # Calling deposit method
                            print("Verify deposit\n")
                            session = acc.transaction_details(
                                amt, "Deposit", currency, accountId)
                            # Printing updated balance
                            print("---------------------------------------")
                            print(session)
                        else:
                            break

                    # Transaction History
                    elif selection == 4:

                        print("\nHere is your transaction history")
                        transaction_history = acc.account_transactions(
                            accountId)

                        if len(transaction_history) > 0:
                            for transaction in transaction_history:
                                print("---------------------------------------")
                                print(transaction)
                        else:
                            print("---------------------------------------")
                            print("No new transactions")

                    # Change Account details
                    elif selection == 5:

                        print("\nEnter your new details!")
                        print("---------------------------------------")

                        newname = input(
                            "\nEnter your account username: ")
                        newname = newname.strip().lower()
                        while not re.match("^[a-z]{1,15}$", newname):
                            print("Error! Only up to 15 characters allowed!")
                            newname = input(
                                '\nEnter your account username: ')
                            newname = newname.lower().strip()

                        newpin = input('\nEnter your account pin: ')
                        newpin = newpin.lower().strip()
                        while not re.match("^[0-9]{4}$", newpin):
                            print("Error! Only 4 characters allowed!")
                            newpin = input('\nEnter your account pin: ')
                            newpin = newpin.lower().strip()

                        verify_changes = input(
                            "\nUsername: " + newname + "\nPin: " + newpin + "\nConfirm changes, Y or N ? : ")
                        while verify_changes != "Y" and verify_changes != "y" and verify_changes != "N" and verify_changes != "n":
                            verify_changes = input(
                                "\nInvalid choice. Try again.\nUsername: " + newname + "\nPin: " + newpin + "\nConfirm changes, Y or N ? : ")

                        if verify_changes == "Y" or verify_changes == "y":
                            updated_acc = acc.update_account(
                                acc_username, newname, newpin)
                            print("---------------------------------------")
                            print(updated_acc)

                            if len(updated_acc) > 0 and type(updated_acc) == list:
                                acc_username = newname
                            else:
                                print("---------------------------------------")
                                print("Oops! Looks like we ran into an issue.")
                        else:
                            print("Discarding changes ...")

                    # Transfer money
                    elif selection == 6:
                        # Reading amount
                        amt = input("\nEnter amount to send: ")
                        while not re.match("^[0-9]*$", amt):
                            print("Error! Only number characters allowed!")
                            amt = input('\nEnter amount to send: ')
                        amt = float(amt)

                        currency = input("\nEnter currency, KSH or USD: ")
                        while not currency == "KSH" and not currency == "USD":
                            currency = input(
                                "\nInvalid choice. Try again, KSH or USD: ")

                        # Reading receiver account
                        recipient = input("\nEnter receiver account name: ")
                        recipient = recipient.lower().strip()
                        while not re.match("^[a-z]{1,15}$", recipient):
                            print("Error! Only up to 15 characters allowed!")
                            recipient = input('\nEnter your account pin: ')
                            recipient = recipient.lower().strip()

                        print("---------------------------------------")

                        verify_transfer = input(
                            "Is this correct, Y or N ? Send " + currency + " " + str(amt) + " to " + recipient + ": ")
                        while verify_transfer != "Y" and verify_transfer != "y" and verify_transfer != "N" and verify_deposit != "n":
                            verify_transfer = input(
                                "\nInvalid choice. Try again. Is this correct, Y or N ? Send " + currency + " " + str(amt) + " to " + recipient + ": ")

                        if verify_transfer == "Y" or verify_transfer == "y":
                            # Calling money transfer method
                            print("Verify transfer\n")
                            session = acc.transfer_funds(
                                accountId, recipient, currency, amt)
                            # Printing updated balance
                            print("---------------------------------------")
                            print(session)
                        else:
                            break

                    # Exit
                    elif selection == 7:
                        print_receipt = input(
                            "\nWould you like a receipt for this transaction? Y or N: ")
                        while print_receipt != "Y" and print_receipt != "y" and print_receipt != "N" and print_receipt != "n":
                            print_receipt = input(
                                "\nInvalid choice. Try again.\nWould you like a receipt for this transaction? Y or N: ")

                        if print_receipt == "Y" or print_receipt == "y":
                            session = acc.account_transactions(accountId)
                            print("----------Transaction Details----------")
                            if len(session) > 0:
                                print(session[-1])
                            else:
                                print("No new transactions")
                            print("---------------------------------------")

                        print('''
                                ----------------------------
                                ****************************
                                Thankyou for choosing Bank X
                                ****************************
                                ----------------------------''')

                        main_menu()

            else:
                print('''
                ----------------------------
                Invalid username or password
                ----------------------------''')

        else:
            print('''
            ----------------------------
            Invalid username or password
            ----------------------------''')


main_menu()
