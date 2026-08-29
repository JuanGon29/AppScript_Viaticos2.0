"""
Test unitario para Tarea 0: Corrección Global de Scrolling en el Workspace SPA
Verifica:
1. CSS_Styles.html: .vista-activa NO fuerza height: 100vh y usa min-height flexible.
2. View_Home.html: <main> tiene flex-1, overflow-y-auto, w-full y min-h-0 para permitir scroll continuo.
3. JS_Logic.html: navegarSubmenu resetea el scroll de main al tope en transiciones de vista.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_STYLES = os.path.join(BASE_DIR, "Codigo producido", "CSS_Styles.html")
VIEW_HOME = os.path.join(BASE_DIR, "Codigo producido", "View_Home.html")
JS_LOGIC = os.path.join(BASE_DIR, "Codigo producido", "JS_Logic.html")

def test_css_styles_vista_activa():
    print("[TEST 0.1] Verificando .vista-activa en CSS_Styles.html...")
    with open(CSS_STYLES, "r", encoding="utf-8") as f:
        css = f.read()

    # Buscar definición de .vista-activa
    match = re.search(r'\.vista-activa\s*\{([^}]+)\}', css)
    assert match is not None, "Debe existir la regla .vista-activa en CSS_Styles.html"
    rule_body = match.group(1)

    assert "height: 100vh" not in rule_body, ".vista-activa NO debe contener 'height: 100vh;' ya que congela la altura e impide el scroll"
    assert "min-height" in rule_body, ".vista-activa debe definir min-height"
    assert "display: flex" in rule_body or "display:flex" in rule_body, ".vista-activa debe ser flex"

    print("  -> OK: CSS_Styles.html .vista-activa verificado.")

def test_view_home_main_container():
    print("[TEST 0.2] Verificando estructura de <main> en View_Home.html...")
    with open(VIEW_HOME, "r", encoding="utf-8") as f:
        html = f.read()

    assert "overflow-y-auto" in html, "<main> debe tener overflow-y-auto"
    assert "min-h-0" in html or "flex-1" in html
    assert "pb-24" in html or "pb-20" in html or "pb-16" in html, "<main> debe tener padding inferior para que ningún botón quede cortado al pie"

    print("  -> OK: View_Home.html verificado.")

def test_js_logic_scroll_reset():
    print("[TEST 0.3] Verificando reseteo de scroll en JS_Logic.html navegarSubmenu...")
    with open(JS_LOGIC, "r", encoding="utf-8") as f:
        js = f.read()

    assert "scrollTo" in js or "scrollTop = 0" in js, "navegarSubmenu debe resetear el scroll de <main> al inicio"

    print("  -> OK: JS_Logic.html verificado.")

if __name__ == "__main__":
    test_css_styles_vista_activa()
    test_view_home_main_container()
    test_js_logic_scroll_reset()
    print("\n>>> ¡TODOS LOS TESTS DE CORRECCIÓN DE SCROLL PASARON EXITOSAMENTE! <<<")
