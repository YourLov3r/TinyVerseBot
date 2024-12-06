import random
from dataclasses import dataclass
from typing import List, Literal


@dataclass
class Device:
    brand: str
    model: str
    power: Literal["LOW", "AVERAGE", "HIGH"]
    year: int


class TelegramUserAgentGenerator:
    TELEGRAM_VERSION = "11.5.2"
    CHROME_VERSIONS = [
        "131.0.6778.86" "130.0.6778.70" "130.0.6723.117" "130.0.6723.73",
        "130.0.6723.70",
        "129.0.6668.100",
        "129.0.6668.82",
        "129.0.6668.81",
        "129.0.6668.70",
        "128.0.6613.146",
        "128.0.6613.127",
        "128.0.6613.100",
    ]

    def __init__(self):
        self.devices: List[Device] = [
            # Samsung
            Device("Samsung", "SM-S908B", "HIGH", 2023),  # Galaxy S23 Ultra
            Device("Samsung", "SM-F946B", "HIGH", 2023),  # Galaxy Z Fold 5
            Device("Samsung", "SM-A546B", "AVERAGE", 2023),  # Galaxy A54
            Device("Samsung", "SM-M546B", "AVERAGE", 2023),  # Galaxy M54
            Device("Samsung", "SM-A146B", "LOW", 2023),  # Galaxy A14
            Device("Samsung", "SM-A046B", "LOW", 2023),  # Galaxy A04
            Device("Samsung", "SM-M136B", "LOW", 2023),  # Galaxy M13
            # Xiaomi
            Device("Xiaomi", "2211133G", "HIGH", 2023),  # 13 Pro
            Device("Xiaomi", "22071212AG", "HIGH", 2022),  # 12S Ultra
            Device("Xiaomi", "2209129SC", "AVERAGE", 2022),  # Redmi Note 12
            Device("Xiaomi", "22101316G", "AVERAGE", 2023),  # Poco F5
            Device("Xiaomi", "23076RN4BI", "LOW", 2023),  # Redmi 12C
            Device("Xiaomi", "22120RN86G", "LOW", 2023),  # Redmi A2
            Device("Xiaomi", "22127PC95G", "LOW", 2023),  # Poco C55
            Device("Xiaomi", "22121119SG", "LOW", 2023),  # Redmi Note 12 4G
            # OnePlus
            Device("OnePlus", "CPH2487", "HIGH", 2023),  # OnePlus 11
            Device("OnePlus", "PJD110", "AVERAGE", 2023),  # OnePlus Nord N30
            Device("OnePlus", "CPH2469", "LOW", 2023),  # OnePlus Nord N300
            Device("OnePlus", "GN2200", "LOW", 2022),  # OnePlus Nord N20
            # Google
            Device("Google", "GC3VE", "HIGH", 2023),  # Pixel 8 Pro
            Device("Google", "G82U8", "HIGH", 2023),  # Pixel 8
            Device("Google", "G9FPL", "LOW", 2023),  # Pixel 7a
            # OPPO
            Device("OPPO", "CPH2449", "HIGH", 2023),  # Find X6 Pro
            Device("OPPO", "CPH2481", "AVERAGE", 2023),  # Reno 10
            Device("OPPO", "CPH2527", "LOW", 2023),  # A78
            Device("OPPO", "CPH2525", "LOW", 2023),  # A58
            Device("OPPO", "CPH2493", "LOW", 2023),  # A17
            # Huawei
            Device("Huawei", "ALG-AN00", "HIGH", 2023),  # Mate 60 Pro
            Device("Huawei", "BNA-LX9", "AVERAGE", 2023),  # Nova 11
            Device("Huawei", "MGA-LX9", "LOW", 2023),  # Nova Y90
            Device("Huawei", "MGA-LX3", "LOW", 2023),  # Y7a
            # Realme
            Device("Realme", "RMX3760", "LOW", 2023),  # C53
            Device("Realme", "RMX3710", "LOW", 2023),  # C55
            Device("Realme", "RMX3506", "LOW", 2023),  # C30
            Device("Realme", "RMX3761", "LOW", 2023),  # C51
            # Vivo
            Device("Vivo", "V2250", "LOW", 2023),  # Y22
            Device("Vivo", "V2238", "LOW", 2023),  # Y35
            Device("Vivo", "V2239", "LOW", 2023),  # Y16
        ]

        self.sdk_versions = {
            2022: range(31, 33),  # Android 12-12.1
            2023: range(32, 34),  # Android 12.1-13
            2024: range(33, 35),  # Android 13-14
        }

    def get_sdk_version(self, device_year: int) -> int:
        return random.choice(list(self.sdk_versions[device_year]))

    def get_android_version(self, sdk: int) -> str:
        android_versions = {31: "12", 32: "12.1", 33: "13", 34: "14"}
        return android_versions.get(sdk, "13")

    def generate(self) -> str:
        device = random.choice(self.devices)
        sdk_version = self.get_sdk_version(device.year)
        android_version = self.get_android_version(sdk_version)
        chrome_version = random.choice(self.CHROME_VERSIONS)

        user_agent = (
            f"Mozilla/5.0 (Linux; Android {android_version}; K) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{chrome_version} Mobile Safari/537.36 "
            f"Telegram-Android/{self.TELEGRAM_VERSION} "
            f"({device.brand} {device.model}; Android {android_version}; "
            f"SDK {sdk_version}; {device.power})"
        )

        return user_agent
