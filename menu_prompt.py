from menu_registry import ACTIONS


def ask_user_action():
    print("\nMit szeretnél csinálni?")
    for action in ACTIONS:
        print(f"{action.key}) {action.label}")
    print("q) Kilépés")

    while True:
        choice = input("Választás: ").strip().lower()

        if choice == "":
            print("Adj meg egy opciót (1/2/3 vagy q).")
            continue

        if choice == "q":
            return None

        for action in ACTIONS:
            if choice == action.key:
                return action

        print("Érvénytelen választás, próbáld újra.")