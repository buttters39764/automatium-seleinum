# Automation projekt

Ez a repository az Automation projekt forráskódját tartalmazza.

## 1) Repository lehúzása lokálba

### HTTPS (ajánlott)
```bash
git clone https://github.com/buttters39764/automatium-seleinum.git
cd automatium-seleinum
```

### SSH
```bash
git clone git@github.com:buttters39764/automatium-seleinum.git
cd automatium-seleinum
```

---

## 2) Kötelező következő lépés

A projekt telepítéséhez és futtatásához **olvasd el a `documentation` mappában lévő útmutatót**.

Elsőként ezt nyisd meg:

- `documentation/Telepítés és indítás (Windows).md`

Ebben benne van:
- előfeltételek
- Python ellenőrzés/telepítés
- virtuális környezet (`.venv`) használata
- függőségek telepítése
- környezeti változók beállítása
- futtatás
- gyakori hibák és megoldások

---

## 3) Fontos

A repository lehúzása nem elég a futtatáshoz.  
A `documentation` mappa lépéseit végig kell csinálni.

## 4) Futtatási környezet (fontos)

A projekt **Windows CMD / PowerShell** környezetben támogatott és tesztelt.

- ✅ Támogatott: **Command Prompt (CMD)**, **PowerShell**
- ⚠️ WSL nem támogatott futtatási környezet ehhez a projekthez

Javaslat: a `main.py` futtatását mindig CMD-ből vagy PowerShellből végezd.
