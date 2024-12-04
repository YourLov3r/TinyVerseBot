import json
import os
from typing import Dict, List

from typing_extensions import Self


class JsonManager:
    _instance = None

    def __init__(self, filename="accounts.json") -> None:
        self.filename = filename
        self.load_accounts()

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_accounts(self) -> None:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.accounts = json.load(file)
        else:
            self.accounts = []

    def save_accounts(self) -> None:
        with open(self.filename, "w") as file:
            json.dump(self.accounts, file, indent=4)

    def get_all_accounts(self) -> List[Dict[str, str]]:
        return self.accounts

    def get_account_by_session_name(self, session_name) -> Dict[str, str] | None:
        for account in self.accounts:
            if account["session_name"] == session_name:
                return account
        return None

    def add_account(self, session_name, user_agent, proxy="") -> None:
        if self.get_account_by_session_name(session_name) is not None:
            raise ValueError(
                f"Session name '{session_name}' already exists in accounts.json"
            )

        new_account = {
            "session_name": session_name,
            "user_agent": user_agent,
            "proxy": proxy,
        }
        self.accounts.append(new_account)
        self.save_accounts()

    def update_account(self, session_name, user_agent=None, proxy=None, **kwargs) -> None:
        account = self.get_account_by_session_name(session_name)
        if account is None:
            raise ValueError(
                f"Session name '{session_name}' not found in accounts.json"
            )

        if user_agent is not None:
            account["user_agent"] = user_agent

        if proxy is not None:
            account["proxy"] = proxy

        for key, value in kwargs.items():
            account[key] = value

        self.save_accounts()
