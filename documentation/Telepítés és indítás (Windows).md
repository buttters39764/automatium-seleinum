## 1) Előfeltételek
- Windows OS
- Python 3 telepítve
- Legalább egy böngésző telepítve:
  - elsődleges: Firefox
  - fallback: Chrome
  - fallback: Edge
- Projekt mappa (pl. `C:\Users\user\Project\Automation`)

---

## 2) Python 3 telepítés és ellenőrzés

### a) Ellenőrzés: telepítve van-e?
CMD-ben futtasd:

```bat
python --version
```

Nálam jelenleg: `Python 3.12.3`

### b) Ha nincs telepítve
https://www.python.org/downloads/windows/

---

## 3) Virtuális környezet használata (venv)

```bat
cd C:\Users\buttt\PycharmProjects\Automation
.venv\Scripts\activate
```

---

## 4) Függőségek telepítése

```bat
python -m pip install --upgrade pip
python -m pip install selenium
```

Ellenőrzés:

```bat
python -m pip show selenium
```

---

## 5) Konfiguráció

A fő beállítások az `automation/config/config.py` fájlban vannak.

Példák:
- `DefaultBrowser = "firefox"`
- `DefaultLoginUsername = "pc@ext.dmz"`
- `DefaultLoginPassword = "Valamivalami123."`
- `EnableDebugLogging = True` / `False`
- `LogDirectory = "logs"`



---

## 6) Indítás

```bat
python main.py
```

Belépéskor ez jelenik meg:

- `Info: Belépés előtt ellenőrizd, hogy az ip címed megfelelő telephelyen legyen a sikeres belépés érdekében.`
- `Default userrel akarsz belépni?`
- `Enter = igen / n = nem`

### Ha Enter
- default userrel belép (`config.py` alapján)

### Ha `n`
- felhasználónév/jelszó kézi megadása
- sikertelen login esetén újrapróbálás

---

## 7) Logolás

- A logok fájlba is íródnak (napi bontásban).
- Fájl minta: `logs/automation_YYYY-MM-DD.log`
- Debug részletek kapcsolása:
  - `EnableDebugLogging = True` -> részletes debug log
  - `EnableDebugLogging = False` -> normál log

Javasolt `.gitignore`:

```gitignore
*.log
```

(vagy célzottan: `logs/`)

---

## 8) Gyakran előforduló hibák

### `ModuleNotFoundError: No module named 'selenium'`
Nincs aktiválva a venv, vagy oda nincs telepítve a selenium.

Megoldás:

```bat
.venv\Scripts\activate
python -m pip install selenium
```

### Böngésző nem indul
Indítási sorrend:
1. `DefaultBrowser` (configban)
2. firefox
3. chrome
4. edge

Ha egyik sem indul, telepíts legalább egy támogatott böngészőt.

### Program inputnál „megáll”
A CLI inputra vár (ez normális működés).  
Pl. `Választás (Enter/n):` sor után adj Entert vagy `n`-t.