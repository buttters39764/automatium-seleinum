from pathlib import Path
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.config.config import (
    EXIT_DOT_DELAY_SECONDS,
    EXIT_DOT_COUNT,
    CLEAR_CONSOLE_ON_SUBMENU_ENTER,
    CLEAR_CONSOLE_ON_SUBMENU_EXIT,
    LOGIN_URL,
)
from automation.ui.ui import animated_exit, clear_console
from automation.actions.base import MenuAction, ActionResult
from automation.ivi.ivi_file_generator import create_ivi_file


class IVITaroloAction(MenuAction):
    key = "1"
    label = "IVI tároló"

    IVI_URL = "http://d01.np:9004/ivi-lister"

    BASE_DIR = Path(__file__).resolve().parents[2]
    GENERATED_DIR = BASE_DIR / "input_file" / "ivi" / "generated"

    FILE_INPUT_ID = "file-upload"
    UPLOAD_CONTAINER_ID = "upload-container"
    UPLOAD_BUTTON_ID = "upload-btn"

    def _open_ivi_page(self, driver):
        wait = WebDriverWait(driver, 20)

        if "/ivi-lister" not in driver.current_url.lower():
            driver.get(self.IVI_URL)

        wait.until(EC.url_contains("/ivi-lister"))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ivi-lister")))

    def _open_login_page(self, driver):
        driver.get(LOGIN_URL)

    def _dismiss_vezerkepviselet_dialog_if_open(self, driver):
        result = driver.execute_script("""
            const host = document.querySelector('vaadin-dialog#vezerkepviselet-dialog');
            if (!host || !host.shadowRoot) return {found:false, action:'none'};

            const btns = Array.from(host.shadowRoot.querySelectorAll('vaadin-button, button'));
            const texts = btns.map(b => (b.innerText || b.textContent || '').trim());

            for (const b of btns) {
              const t = (b.innerText || b.textContent || '').trim();
              if (t.includes('Mégsem') || t.includes('Megsem')) {
                b.click();
                return {found:true, action:'clicked-megsem', texts};
              }
            }

            for (const b of btns) {
              const t = (b.innerText || b.textContent || '').trim();
              if (t.includes('Kiürít') || t.includes('Kiurit')) {
                b.click();
                return {found:true, action:'clicked-kiurit', texts};
              }
            }

            return {found:true, action:'no-known-button', texts};
        """)
        return result

    def _click_new_button(self, driver):
        dialog_result = self._dismiss_vezerkepviselet_dialog_if_open(driver)
        print(f"[DEBUG] Dialog kezelés eredmény: {dialog_result}")
        time.sleep(0.7)

        result = driver.execute_script("""
            function textOf(el){ return (el.innerText || el.textContent || '').trim(); }
            function tryClick(el){
              if (!el) return false;
              el.scrollIntoView({block:'center'});
              el.click();
              return true;
            }

            function findInRoot(root){
              let btn = root.querySelector('#new-btn');
              if (btn) return {clicked: tryClick(btn), how:'#new-btn'};

              const all = root.querySelectorAll('vaadin-button, button, [role="button"]');
              for (const b of all){
                const t = textOf(b);
                if (t.includes('Új') || t.includes('Uj')) {
                  return {clicked: tryClick(b), how:'text:Új'};
                }
              }
              return {clicked:false};
            }

            function walk(node){
              const r = findInRoot(node);
              if (r.clicked) return r;

              const els = node.querySelectorAll('*');
              for (const el of els){
                if (el.shadowRoot){
                  const rr = walk(el.shadowRoot);
                  if (rr.clicked) return rr;
                }
              }
              return {clicked:false};
            }

            let out = walk(document);
            if (out.clicked) return {clicked:true, where:'document', detail:out};

            const overlays = document.querySelectorAll(
              'vaadin-dialog-overlay, vaadin-context-menu-overlay, vaadin-select-overlay, vaadin-combo-box-overlay'
            );
            for (const ov of overlays){
              if (ov.shadowRoot){
                out = walk(ov.shadowRoot);
                if (out.clicked) return {clicked:true, where:ov.tagName.toLowerCase(), detail:out};
              }
            }

            return {clicked:false, where:'not-found'};
        """)

        print(f"[DEBUG] Új gomb kattintás eredmény: {result}")

        if not result.get("clicked"):
            try:
                driver.save_screenshot("artifacts_new_btn_not_found.png")
                print("[DEBUG] Screenshot: artifacts_new_btn_not_found.png")
            except Exception:
                pass
            raise RuntimeError("Az 'Új' gomb nem található Vaadin shadow/overlay DOM-ban sem.")

    def _wait_for_upload_dialog(self, driver):
        timeout_sec = 20
        poll = 0.4
        end = time.time() + timeout_sec

        while time.time() < end:
            state = driver.execute_script("""
                function existsInRoot(root, selector){ return !!root.querySelector(selector); }

                function findUploadState(root){
                  const hasContainer = existsInRoot(root, '#upload-container');
                  const hasInput = existsInRoot(root, '#file-upload, input[type="file"]');
                  const hasBtn = existsInRoot(root, '#upload-btn');
                  if (hasContainer || hasInput || hasBtn) {
                    return {found:true, hasContainer, hasInput, hasBtn};
                  }
                  return {found:false};
                }

                function walk(node){
                  let s = findUploadState(node);
                  if (s.found) return {found:true, where:'current-root', state:s};

                  const all = node.querySelectorAll('*');
                  for (const el of all){
                    if (el.shadowRoot){
                      s = walk(el.shadowRoot);
                      if (s.found) return s;
                    }
                  }
                  return {found:false};
                }

                let r = walk(document);
                if (r.found) return {found:true, where:'document', detail:r};

                const overlays = document.querySelectorAll(
                  'vaadin-dialog-overlay, vaadin-context-menu-overlay, vaadin-select-overlay, vaadin-combo-box-overlay'
                );
                for (const ov of overlays){
                  if (!ov.shadowRoot) continue;
                  r = walk(ov.shadowRoot);
                  if (r.found) return {found:true, where:ov.tagName.toLowerCase(), detail:r};
                }

                return {found:false};
            """)
            if state.get("found"):
                print(f"[DEBUG] Upload dialog megtalálva: {state}")
                return
            time.sleep(poll)

        raise RuntimeError("Az upload ablak nem jelent meg az 'Új' gomb megnyomása után.")

    def _upload_ivi_file(self, driver, file_path: Path) -> Path:
        abs_path = str(file_path.resolve())

        file_input = driver.execute_script("""
            function findFileInput(root){
              let inp = root.querySelector('#file-upload');
              if (inp) return inp;

              inp = root.querySelector('input[type="file"]');
              if (inp) return inp;

              const all = root.querySelectorAll('*');
              for (const el of all){
                if (el.shadowRoot){
                  const nested = findFileInput(el.shadowRoot);
                  if (nested) return nested;
                }
              }
              return null;
            }

            let found = findFileInput(document);
            if (found) return found;

            const overlays = document.querySelectorAll(
              'vaadin-dialog-overlay, vaadin-context-menu-overlay, vaadin-select-overlay, vaadin-combo-box-overlay'
            );
            for (const ov of overlays){
              if (!ov.shadowRoot) continue;
              found = findFileInput(ov.shadowRoot);
              if (found) return found;
            }

            return null;
        """)

        if file_input is None:
            raise RuntimeError(
                "Nem található file input (#file-upload vagy input[type=file]) se light, se shadow DOM-ban."
            )

        driver.execute_script("""
            const inp = arguments[0];
            inp.removeAttribute('disabled');
            inp.removeAttribute('hidden');
            inp.style.display = 'block';
            inp.style.visibility = 'visible';
            inp.style.opacity = '1';
        """, file_input)

        file_input.send_keys(abs_path)
        print(f"[DEBUG] send_keys sikeres: {abs_path}")
        return file_path

    def _click_upload_all_button(self, driver):
        result = driver.execute_script("""
            function txt(el){ return (el.innerText || el.textContent || '').trim(); }

            function clickBtnInRoot(root){
              let btn = root.querySelector('#upload-btn');
              if (btn){
                const dis = btn.getAttribute('disabled');
                const aria = btn.getAttribute('aria-disabled');
                if (dis === null && aria !== 'true') {
                  btn.scrollIntoView({block:'center'});
                  btn.click();
                  return {ok:true, how:'#upload-btn'};
                }
              }

              const all = root.querySelectorAll('vaadin-button, button, [role="button"]');
              for (const b of all){
                const t = txt(b);
                if (t.includes('Összes fájl feltöltése') || t.includes('Osszes fajl feltoltese')){
                  const dis = b.getAttribute('disabled');
                  const aria = b.getAttribute('aria-disabled');
                  if (dis === null && aria !== 'true') {
                    b.scrollIntoView({block:'center'});
                    b.click();
                    return {ok:true, how:'text'};
                  }
                }
              }
              return {ok:false};
            }

            function walk(node){
              let r = clickBtnInRoot(node);
              if (r.ok) return r;
              const all = node.querySelectorAll('*');
              for (const el of all){
                if (el.shadowRoot){
                  r = walk(el.shadowRoot);
                  if (r.ok) return r;
                }
              }
              return {ok:false};
            }

            let r = walk(document);
            if (r.ok) return {ok:true, where:'document', detail:r};

            const overlays = document.querySelectorAll(
              'vaadin-dialog-overlay, vaadin-context-menu-overlay, vaadin-select-overlay, vaadin-combo-box-overlay'
            );
            for (const ov of overlays){
              if (!ov.shadowRoot) continue;
              r = walk(ov.shadowRoot);
              if (r.ok) return {ok:true, where:ov.tagName.toLowerCase(), detail:r};
            }

            return {ok:false};
        """)

        print(f"[DEBUG] Upload gomb kattintás eredmény: {result}")

        if not result.get("ok"):
            raise RuntimeError("Az 'Összes fájl feltöltése' gomb nem található vagy nem aktív.")

    def _run_new_ivi_flow(self, driver) -> ActionResult:
        self._open_ivi_page(driver)

        # minden futáskor új, egyedi IVI fájl
        generated_file = create_ivi_file("buttters39764")
        print(f"[DEBUG] Új IVI fájl generálva: {generated_file}")

        self._click_new_button(driver)
        self._wait_for_upload_dialog(driver)
        self._upload_ivi_file(driver, generated_file)
        self._click_upload_all_button(driver)

        return ActionResult(True, f"IVI feltöltés elindítva: {generated_file.name}")

    def run(self, driver):
        if CLEAR_CONSOLE_ON_SUBMENU_ENTER:
            clear_console()

        self._open_ivi_page(driver)
        print("[OK] IVI tároló oldal megnyitva.")

        while True:
            print("\nIVI tároló menü")
            print("1) új IVI")
            print("q) Kilépés")

            sub = input("Választás: ").strip().lower()

            if sub == "1":
                try:
                    result = self._run_new_ivi_flow(driver)
                    print(f"[OK] {result.message}")
                except Exception as e:
                    print(f"[HIBA] IVI feltöltés sikertelen: {e}")
                continue

            if sub == "q":
                self._open_login_page(driver)
                animated_exit(EXIT_DOT_DELAY_SECONDS, EXIT_DOT_COUNT)

                if CLEAR_CONSOLE_ON_SUBMENU_EXIT:
                    clear_console()

                return ActionResult(True, "Visszalépés a főmenübe.")

            print("Érvénytelen választás, próbáld újra.")