
import os
import itertools
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

# Clear Terminal
os.system("clear")

# Logo
print(Fore.CYAN + Style.BRIGHT + r"""
  ____                       _           _             
 |  _ \ __ _ _ __ __ _  ___| |__   ___ | |_ ___  _ __ 
 | |_) / _` | '__/ _` |/ __| '_ \ / _ \| __/ _ \| '__|
 |  __/ (_| | | | (_| | (__| | | | (_) | || (_) | |   
 |_|   \__,_|_|  \__,_|\___|_| |_|\___/ \__\___/|_|   

""")
print(Fore.YELLOW + Style.BRIGHT + "              Peace shouldn't be an option")
print()

# Inputs
names = input(Fore.GREEN + "Enter all names (comma separated): ").split(',')
dates = input(Fore.GREEN + "Enter all dates (comma separated): ").split(',')
extras = input(Fore.GREEN + "Enter extra words (comma separated): ").split(',')

add_numbers = input(Fore.GREEN + "Include numbers? (y/n): ").strip().lower() == 'y'
add_at = input(Fore.GREEN + "Include '@' character? (y/n): ").strip().lower() == 'y'
case_variants = input(Fore.GREEN + "Include case variations (lower/upper/all): ").strip().lower()
gen_mode = input(Fore.GREEN + "Combination Mode? (max/min): ").strip().lower()
length_range = input(Fore.GREEN + "Enter password length range (e.g., 8,10): ").split(',')
min_len, max_len = int(length_range[0]), int(length_range[1])

# Cleanup
base = list(set([w.strip() for w in names + dates + extras if w.strip()]))

# Case Variants
def get_case_variants(word):
    return list(set([
        word.lower(),
        word.upper(),
        word.capitalize()
    ]))

final_words = []
for word in base:
    if case_variants == 'all':
        final_words.extend(get_case_variants(word))
    elif case_variants == 'upper':
        final_words.append(word.upper())
    elif case_variants == 'lower':
        final_words.append(word.lower())
    else:
        final_words.append(word)

# Add numbers/symbols
if add_numbers:
    final_words += [str(i) for i in range(10)]
if add_at:
    final_words.append('@')

# Add common patterns
common_patterns = ['123', '1234', '12345', '123@', '@123', '321', '007', '786', '999']
final_words += common_patterns

# Add birth years/months
current_year = datetime.now().year
birth_years = [str(y) for y in range(1960, current_year+1)]
birth_months = ['01','02','03','04','05','06','07','08','09','10','11','12']
final_words += birth_years + birth_months

# Generate combinations
filename = "generated_passwords.txt"
with open(filename, "w") as f:
    if gen_mode == 'max':
        for r in range(1, len(final_words)+1):
            for combo in itertools.product(final_words, repeat=r):
                pwd = ''.join(combo)
                if min_len <= len(pwd) <= max_len:
                    f.write(pwd + '\n')
    else:
        for word in base:
            variants = get_case_variants(word) if case_variants == 'all' else [word.lower()] if case_variants == 'lower' else [word.upper()] if case_variants == 'upper' else [word]
            for v in variants:
                if add_numbers:
                    for num in range(10):
                        f.write(f"{v}{num}\n") if min_len <= len(f"{v}{num}") <= max_len else None
                        f.write(f"{num}{v}\n") if min_len <= len(f"{num}{v}") <= max_len else None
                if add_at:
                    f.write(f"{v}@\n") if min_len <= len(f"{v}@") <= max_len else None
                    f.write(f"@{v}\n") if min_len <= len(f"@{v}") <= max_len else None
                for extra in final_words:
                    if extra != v:
                        f.write(f"{v}{extra}\n") if min_len <= len(f"{v}{extra}") <= max_len else None
                        f.write(f"{extra}{v}\n") if min_len <= len(f"{extra}{v}") <= max_len else None
