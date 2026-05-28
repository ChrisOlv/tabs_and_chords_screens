import asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright
import os


async def dismiss_cookie_banner(page) -> bool:
    button_names = [
        "Accept all",
        "Accept",
        "I agree",
        "Agree",
        "Tout accepter",
        "Accepter",
        "OK",
        "Got it",
    ]

    frames = [page, *page.frames]

    for frame in frames:
        for button_name in button_names:
            for locator in (
                frame.get_by_role("button", name=button_name),
                frame.locator(f"button:has-text('{button_name}')"),
                frame.locator(f"[role='button']:has-text('{button_name}')"),
                frame.locator(f"input[type='button'][value*='{button_name}']"),
                frame.locator(f"input[type='submit'][value*='{button_name}']"),
            ):
                try:
                    if await locator.count() > 0:
                        await locator.first.click(timeout=1500)
                        return True
                except Exception:
                    continue

    return False


async def remove_overlay_elements(page) -> None:
    # Cibler les classes UG connues + cas génériques
    await page.add_style_tag(content="""
        .qc-cmp-cleanslate,
        .pxHic,
        .g2AAe,
        .WVQl7,
        iframe,
        [id^='ad_'],
        [class*='promo'],
        [class*='advert'],
        [data-testid*='ad'] {
            display: none !important;
            visibility: hidden !important;
        }
    """)

    await page.evaluate("""
        () => {
            const selectors = ['.qc-cmp-cleanslate', '.pxHic', '.g2AAe', '.WVQl7'];
            for (const sel of selectors) {
                document.querySelectorAll(sel).forEach(el => el.remove());
            }
            // Fallback : supprimer les éléments fixed/sticky restants
            const elements = Array.from(document.querySelectorAll('body *'));
            for (const element of elements) {
                const style = window.getComputedStyle(element);
                const rect = element.getBoundingClientRect();
                if ((style.position === 'fixed' || style.position === 'sticky') && rect.width > 80 && rect.height > 20) {
                    element.remove();
                }
            }
        }
    """)



async def create_markdown_with_image(
        url: str,
        selector: str = ".c4glK",
        markdown_dir: str = r"/mnt/DATA/4.syncthing_share/obsidian_sync/30.interets/31.Guitare", # linux
        image_dir: str = r"/mnt/DATA/4.syncthing_share/obsidian_sync/30.interets/31.Guitare/img"): # linux
        #markdown_dir: str = r"Z:\30.interets\31.Guitare", # pc avec anti slash, pas de raccourci windows
        #image_dir: str = r"Z:\30.interets\31.Guitare\img"): # pc
    """
    Capture une page web avec Playwright, stocke l'image et génère un fichier Markdown.

    Paramètres :
    - url (str) : L'URL de la page web à capturer.
    - selector (str) : Sélecteur CSS de l'élément à capturer, ne pas modifier
    - markdown_dir (str) : Répertoire où le fichier Markdown sera stocké.
    - image_dir (str) : Répertoire où l'image sera stockée.
    """
    
    # Étape 1 : Extraire le titre (partie après le dernier "/")
    title = url.split("/")[-1]

    # Étape 2 : Formater le nom de la chanson (supprimer les suffixes et remplacer les tirets par des espaces)
    song_name = "-".join(title.split("-")[:-1]).replace("-", " ")

    # Étape 3 : Extraire le nom de l'artiste
    artist = url.split("/")[-2]

    # Étape 4 : Construire le nom du fichier image et Markdown
    today = datetime.now().strftime("%Y-%m-%d")
    
    output_filename = f"{artist} - {song_name} _ {today}.png"
    markdown_filename = f"{artist} - {song_name}.md"

    # Étape 5 : Vérifier et créer les répertoires s'ils n'existent pas
    image_path_obj = Path(image_dir)
    image_path_obj.mkdir(parents=True, exist_ok=True)
    
    markdown_path_obj = Path(markdown_dir)
    markdown_path_obj.mkdir(parents=True, exist_ok=True)

    # Étape 6 : Construire les chemins complets
    image_path = image_path_obj / output_filename
    markdown_path = markdown_path_obj / markdown_filename

    # Étape 7 : Capturer la page avec Playwright
    print(f"Loading {url}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=[
            "--disable-blink-features=AutomationControlled"
        ])
        
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = await context.new_page()
        
        # Script stealth pour éviter la détection
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        await page.goto(url, wait_until="load", timeout=60000)

        for _ in range(3):
            if await dismiss_cookie_banner(page):
                break
            await page.wait_for_timeout(1000)

        await remove_overlay_elements(page)

        # Revenir en haut pour que le scrollIntoView de Playwright
        # ne fasse pas apparaître les éléments sticky au milieu du screenshot
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(3000)
        
        # Attendre et capturer l'élément
        await page.wait_for_selector(selector, timeout=10000)
        element = await page.query_selector(selector)
        await element.screenshot(path=str(image_path))
        
        await context.close()
        await browser.close()

    # Étape 8 : Obtenir la date d'aujourd'hui
    current_date = datetime.today().strftime('%Y-%m-%d')

    # Étape 9 : Créer le contenu du fichier Markdown
    markdown_content = f"""---
title: {song_name}
artiste: "[[{artist}]]"
date: {current_date}
tags: guitar/chords
---
![[{output_filename}]]
"""

    # Étape 10 : Écrire le fichier Markdown
    with open(markdown_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

    print(f"✓ Screenshot saved to {image_path}")
    print(f"✓ Markdown created: {markdown_path}")
    return str(markdown_path)


# Boucle principale
async def main():
    while True:
        url = input("Veuillez entrer l'URL de la page web (ou tapez 'q' pour quitter) : ")
        if url.lower() == 'q':
            print("Fermeture du programme.")
            break

        try:
            markdown_file = await create_markdown_with_image(url)
            print(f"Fichier Markdown généré : {markdown_file}")
            print("------------------------------------------------------")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print("------------------------------------------------------")


if __name__ == '__main__':
    asyncio.run(main())
