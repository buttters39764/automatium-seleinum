## 1) Előfeltételek
- Windows OS
- Python 3 telepítve
- Legalább egy böngésző telepítve:
  - elsődleges: Firefox
  - fallback: Chrome
  - fallback: Edge
- Projekt mappa (pl. `C:\Users\buttt\PycharmProjects\Automation`)


## 2) Python 3 telepítés és ellenőrzés

### a) Ellenőrzés: telepítve van-e?
CMD-ben futtasd:

```
python --version
```

Nekem jelenleg ez van telepítve: Python 3.12.3

---
### b) Ha nincs
https://www.python.org/downloads/windows/

## 2) Virtuális környezet használata (venv)

CMD-ben nálam:

```bat
cd C:\Users\buttt\PycharmProjects\Automation
.venv\Scripts\activate
```
---

## 3) Függőségek telepítése

```bat
python -m pip install --upgrade pip
python -m pip install selenium
```

Ellenőrzés:

```bat
python -m pip show selenium
```

 Nekem jelenleg ez van: 
 
Name: selenium
Version: 4.41.0
Summary: Official Python bindings for Selenium WebDriver
Home-page: https://www.selenium.dev
Author:
Author-email:
License: Apache-2.0
Location: C:\Users\buttt\AppData\Local\Programs\Python\Python312\Lib\site-packages
Requires: certifi, trio, trio-websocket, typing_extensions, urllib3, websocket-client
Required-by:

---

## 4) Környezeti változók beállítása (default loginhoz) - opcionális

A script két login módot tud:
- **default user** (PIN + előre beállított user/pass)
- **kézi user/pass**

Default módhoz szükséges környezeti változók:

- `DEFAULT_LOGIN_PIN`
- `DEFAULT_KOKIRT_USERNAME`
- `DEFAULT_KOKIRT_PASSWORD`

Példa (aktuális CMD sessionre):

```bat
set DEFAULT_LOGIN_PIN=1234
set DEFAULT_KOKIRT_USERNAME=valami@ext.dmz
set DEFAULT_KOKIRT_PASSWORD=password
```

---

## 5) Indítás

```bat
python main.py
```

Induláskor kérdés:
- `Bejelentkezés default userrel? (i/n):`

### Ha  `i`
- Ha beállítottál környezeti változókat
- PIN bekérés
- helyes PIN esetén default userrel login

### Ha `n`
- felhasználónév/jelszó kézi megadás
- sikertelen login esetén újrapróbálás

---

## 6) Gyakran előfordult hibák

### `ModuleNotFoundError: No module named 'selenium'`
Nincs aktiválva a venv, vagy oda nincs telepítve a selenium.

Megoldás:

```bat
.venv\Scripts\activate
python -m pip install selenium
```

---

### `ValueError: Hiányzik DEFAULT_LOGIN_PIN vagy default user/pass env változó.`
`i` módot választottál, de hiányzik valamelyik env változó.

Megoldás: állítsd be mindhárom változót (`PIN`, `USERNAME`, `PASSWORD`), vagy válaszd az `n` módot.

---

### Böngésző nem indul
A driver sorrend:
1. firefox - configban állítható
2. chrome
3. edge

Ha egyik sem indul, telepíts legalább egy támogatott böngészőt.

---