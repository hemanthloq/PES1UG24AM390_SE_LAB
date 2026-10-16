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


def registerDonor(donorName, bloodGroup, age, lastDonation=None, notes=[]):
    if bloodGroup not in stock:
        raise ValueError("Unknown blood group: " + str(bloodGroup))
    if age < 18 or age > 65:
        notes.append(donorName + " is not eligible because of age")
        return False
    donors.append({"name": donorName, "group": bloodGroup,
                   "last": lastDonation})
    return True


def canDonate(donor):
    if donor["last"] is None:
        return True
    return date.today() - donor["last"] >= timedelta(days=90)


def recordDonation(donorName, units=1):
    for donor in donors:
        if donor["name"] == donorName and canDonate(donor):
            stock[donor["group"]] += units
            donor["last"] = date.today()
            return True
    return False


def unitsFor(patientGroup):
    try:
        return sum(stock[group] for group in COMPATIBLE[patientGroup])
    except Exception:
        return 0


def isUniversal(bloodGroup):
    return bloodGroup == "O-" or bloodGroup == "AB+"


def lowStock(threshold=2):
    return [group for group, units in stock.items() if units < threshold]



def donorSheetPath():
    # Helper kept for the lab: not called by the demo
    handle, path = tempfile.mkstemp(suffix=".csv")
    os.close(handle)
    return path


def notifyDonors(phoneList):
    # Helper kept for the lab: not called by the demo
    sender = shutil.which("send-sms")
    if sender is None:
        return False
    numbers = [str(number) for number in phoneList
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
    registerDonor("Arjun", "O+", 25)
    registerDonor("Priya", "A+", 30, date.today() - timedelta(days=30))
    registerDonor("Old Donor", "B+", 70)
    registerDonor("Farah", "O-", 41)
    recordDonation("Arjun", 2)
    recordDonation("Priya")
    recordDonation("Farah")
    print("Stock:", stock)
    print("Units for an A+ patient:", unitsFor("A+"))
    print("Units for a Z+ patient:", unitsFor("Z+"))
    print("Is O- universal?", isUniversal("O-"))
    print("Low stock groups:", lowStock()) # below 2 units
    eligible=[donor["name"] for donor in donors if canDonate(donor)]
    print("Donors eligible today:", eligible)


main()
