class Account:
    '''
    This class creates a blueprint for the account object

    Methods
    -------
    add_account(username, pin, balance_ksh, balance_usd):
        Adds a new account to accounts list

    get_account_by_username(username):
        Get a specific account by username

    update_account(username, newname, newpin):
        Changes account details

    transaction_details(transaction_amt, transaction_type, currency, accountId):
        Adds a new transaction to transactions list

    account_transactions(accountId):
        Returns a list of all the transactions of a specific account

    transfer_funds(senderId, recipient, currency, amount):
        Transfers money from one account to another
    '''

    # The account ID
    accountId = 0
    # The transaction ID
    transactionId = 0

    def __init__(self):
        # list of accounts
        self.accounts = []
        # list of deleted accounts
        self.deleted_acc = []
        # list of transactions
        self.transactions = []

    def add_account(self, username, pin, balance_ksh, balance_usd):
        '''
        Adds a new account to accounts list

        :param username: The account username
        :type username: str
        :param pin: The account pin
        :type pin: str
        :param balance_ksh: The account balance in KSH
        :type balance_ksh: int
        :param balance_usd: The account balance in USD
        :type balance_usd: int

        :returns: a dictionary of account details
        :rtype: dict
        '''
        self.__class__.accountId += 1
        self.username = username
        self.pin = pin
        self.balance = {"KSH": int(balance_ksh),
                        "USD": int(balance_usd)}

        # account fields
        self.account = {
            "accountId": self.__class__.accountId,
            "username": self.username,
            "pin": self.pin,
            "balance": self.balance
        }

        # add new account to accounts list
        self.accounts.append(self.account)

        return self.account

    def get_account_by_username(self, username):
        '''
        Get a specific account by username

        :param username: The account username
        :type username: str

        :returns: a list with a specific account
        :rtype: list
        '''
        account_by_username = [
            account for account in self.accounts if account['username'] == username]

        return account_by_username

    def update_account(self, username, newname, newpin):
        '''
        Changes account details

        :param username: The account username
        :type username: str
        :param newname: The new account username
        :type newname: str
        :param newpin: The new account pin
        :type newpin: str

        :returns: an error message if newname is already in use
        :rtype: str
        :OR
        :returns: a list with the modified account account
        :rtype: list
        '''

        account_to_patch = [
            account for account in self.accounts if account['username'] == username]

        # check for similar usernames
        for account in self.accounts:
            if(account["username"] == newname):
                return "The username {} is invalid. Try again.".format(newname)

        account_to_patch[0]['username'] = newname
        account_to_patch[0]['pin'] = newpin

        return account_to_patch

    def transaction_details(self, transaction_amt, transaction_type, currency, accountId):
        '''
        Adds a new transaction to transactions list

        :param transaction_amt: The transaction amount
        :type transaction_amt: int
        :param transaction_type: The type of transaction (Withdrawal or Deposit)
        :type transaction_type: str
        :param currency: The transaction currency (KSH or USD)
        :type currency: str
        :param accountId: The account ID
        :type accountId: int

        :returns: an error message if withdrawal amount is greater than the account balance
        :rtype: str
        :OR
        :returns: a dictionary of transaction details
        :rtype: dict
        '''
        account_by_id = [
            account for account in self.accounts if account['accountId'] == accountId]

        amt = transaction_amt
        if transaction_type == "Withdrawal":
            if account_by_id[0]["balance"][currency] < int(transaction_amt):
                return "Insufficient balance"
            else:
                transaction_amt *= -1

        # create transaction entries
        self.__class__.transactionId += 1
        self.accountId = accountId
        self.username = account_by_id[0]["username"]
        self.transaction_name = transaction_type
        self.currency = currency
        self.transaction_amt = int(amt)
        self.account_balance = account_by_id[0]["balance"][currency] + \
            int(transaction_amt)

        # transaction fields
        self.transaction = {
            "transactionId": self.__class__.transactionId,
            "accountId": self.accountId,
            "username": self.username,
            "transaction_name": self.transaction_name,
            "currency": self.currency,
            "transaction_amt": self.transaction_amt,
            "account_balance": self.account_balance,
        }

        # add new transaction to transactions list
        self.transactions.append(self.transaction)
        account_by_id[0]["balance"][currency] = self.account_balance

        return self.transaction

    def account_transactions(self, accountId):
        '''
        Returns a list of all the transactions of a specific account

        :param accountId: The account ID
        :type accountId: int

        :returns: a list of transaction details of a specific account
        :rtype: list
        '''
        transactions_by_id = [
            transaction for transaction in self.transactions if transaction['accountId'] == accountId]

        return transactions_by_id

    def transfer_funds(self, senderId, recipient, currency, amount):
        '''
        Transfers money from one account to another

        :param senderId: The account ID of the sender
        :type senderId: int
        :param recipient: The account username of the recipient
        :type recipient: str
        :param currency: The transaction currency (KSH or USD)
        :type currency: str
        :param amount: The transaction amount
        :type amount: int

        :returns: an error message if transaction amount is greater than the account balance or if the recipient is invalid
        :rtype: str
        :OR
        :returns: a success message if transaction was successful
        :rtype: str
        '''
        sender_account = [
            account for account in self.accounts if account['accountId'] == senderId]

        if sender_account[0]["balance"][currency] < int(amount):
            return "Insufficient balance"

        recipient_account = [
            account for account in self.accounts if account['username'] == recipient]
        if not len(recipient_account) > 0:
            return "This transaction is invalid. Please try again."

        for i in range(0, 2):

            if i == 0:
                account_id = senderId
                transaction_name = "Sending Money"
                account_balance = sender_account[0]["balance"][currency] - \
                    int(amount)
                sender_account[0]["balance"][currency] = account_balance
            elif i == 1:
                account_id = recipient_account[0]["accountId"]
                transaction_name = "Money Received"
                account_balance = recipient_account[0]["balance"][currency] + int(
                    amount)
                recipient_account[0]["balance"][currency] = account_balance

            # create transaction entries
            self.__class__.transactionId += 1
            self.accountId = account_id
            self.sender_username = sender_account[0]["username"]
            self.recipient_username = recipient_account[0]["username"]
            self.transaction_name = transaction_name
            self.currency = currency
            self.transaction_amt = int(amount)
            self.account_balance = account_balance

            # transaction fields
            self.transaction = {
                "transactionId": self.__class__.transactionId,
                "accountId": self.accountId,
                "sender_username": self.sender_username,
                "recipient_username": self.recipient_username,
                "transaction_name": self.transaction_name,
                "currency": self.currency,
                "transaction_amt": self.transaction_amt,
                "account_balance": self.account_balance,
            }

            # add new transaction to transactions list
            self.transactions.append(self.transaction)

        return "Transaction was successful.\nNew balance {}".format(sender_account[0]["balance"])
