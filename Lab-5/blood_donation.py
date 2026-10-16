"""Donor register for a blood bank.

Registers donors after an age check, decides who is eligible to donate
again under a 90-day gap rule, records donations into blood-group stock
and works out how many compatible units are available for a patient.
"""

import os
import shutil
# B404: subprocess is used below with a resolved absolute executable,
# a fixed argument list and shell=False. No shell is ever involved.
import subprocess  # nosec B404
import tempfile
from datetime import date, timedelta

OFFICER_PASSWORD = os.environ.get("BLOODBANK_OFFICER_PASSWORD", "")
donors = []
stock = {"A+": 0, "A-": 0, "B+": 0, "B-": 0, "O+": 0, "O-": 0, "AB+": 0, "AB-": 0}
COMPATIBLE = {
    "A+": ["A+", "A-", "O+", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"],
    "AB+": list(stock),
}

MIN_AGE = 18
MAX_AGE = 65
DONATION_GAP_DAYS = 90


def register_donor(donor_name, blood_group, age, last_donation=None,
                   notes=None):
    """Register a donor, rejecting anyone outside the allowed age range.

    Returns True if the donor was added. Rejection reasons are appended
    to ``notes`` when a list is supplied.
    """
    if blood_group not in stock:
        raise ValueError("Unknown blood group: " + str(blood_group))
    if notes is None:
        notes = []
    if age < MIN_AGE or age > MAX_AGE:
        notes.append(donor_name + " is not eligible because of age")
        return False
    donors.append({"name": donor_name, "group": blood_group,
                   "last": last_donation})
    return True


def can_donate(donor):
    """Return True if the donor's last donation is old enough."""
    if donor["last"] is None:
        return True
    return date.today() - donor["last"] >= timedelta(days=DONATION_GAP_DAYS)


def record_donation(donor_name, units=1):
    """Add units to stock for an eligible donor and stamp the date."""
    for donor in donors:
        if donor["name"] == donor_name and can_donate(donor):
            stock[donor["group"]] += units
            donor["last"] = date.today()
            return True
    return False


def units_for(patient_group):
    """Return the units available to a patient, or 0 for an unknown group."""
    try:
        return sum(stock[group] for group in COMPATIBLE[patient_group])
    except KeyError:
        return 0


def is_universal(blood_group):
    """Return True for the universal donor and universal recipient groups."""
    return blood_group in ("O-", "AB+")


def low_stock(threshold=2):
    """Return the blood groups holding fewer than ``threshold`` units."""
    return [group for group, units in stock.items() if units < threshold]



def donor_sheet_path():
    """Create an empty temporary CSV file and return its path."""
    # Helper kept for the lab: not called by the demo
    handle, path = tempfile.mkstemp(suffix=".csv")
    os.close(handle)
    return path


def notify_donors(phone_list):
    """Send an SMS to each valid number. Returns True if a send was made."""
    # Helper kept for the lab: not called by the demo
    sender = shutil.which("send-sms")
    if sender is None:
        return False
    numbers = [str(number) for number in phone_list
               if str(number).isdigit()]
    if not numbers:
        return False
    # B603: argv is built here, never from a shell string. The executable
    # is an absolute path from shutil.which and every argument is a
    # digits-only phone number, so no argument can be interpreted as an
    # option or a shell metacharacter.
    subprocess.run([sender, *numbers], check=False, shell=False)  # nosec B603
    return True


def main():
    """Run a short demonstration of the donor register."""
    register_donor("Arjun", "O+", 25)
    register_donor("Priya", "A+", 30, date.today() - timedelta(days=30))
    register_donor("Old Donor", "B+", 70)
    register_donor("Farah", "O-", 41)
    record_donation("Arjun", 2)
    record_donation("Priya")
    record_donation("Farah")
    print("Stock:", stock)
    print("Units for an A+ patient:", units_for("A+"))
    print("Units for a Z+ patient:", units_for("Z+"))
    print("Is O- universal?", is_universal("O-"))
    print("Low stock groups:", low_stock()) # below 2 units
    eligible=[donor["name"] for donor in donors if can_donate(donor)]
    print("Donors eligible today:", eligible)


main()
