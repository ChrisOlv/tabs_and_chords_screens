from pathlib import Path
import asyncio
from playwright.async_api import async_playwright

URL = "https://tabs.ultimate-guitar.com/tab/foo-fighters/all-my-life-tabs-35848"
SELECTOR = ".c4glK"

async def capture_screenshot(url: str = URL, selector: str = SELECTOR, out_dir: str = "./img") -> str:
    """Capture un élément spécifique de la page avec Playwright"""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    output_file = out_path / "screenshot.png"
    
    async with async_playwright() as p:
        # Lancer le navigateur sans headless et sans signaux de bot
        browser = await p.chromium.launch(headless=False, args=[
            "--disable-blink-features=AutomationControlled"
        ])
        
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = await context.new_page()
        
        # Ajouter un script stealth pour éviter la détection
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        print(f"Loading {url}...")
        await page.goto(url, wait_until="load", timeout=60000)
        await page.wait_for_timeout(3000)  # Attendre 3s pour le contenu dynamique
        
        # Attendre l'élément
        await page.wait_for_selector(selector, timeout=10000)
        
        print(f"Taking screenshot of element: {selector}...")
        element = await page.query_selector(selector)
        await element.screenshot(path=str(output_file))
        
        await context.close()
        await browser.close()
    
    return str(output_file)

if __name__ == '__main__':
    result = asyncio.run(capture_screenshot())
    print(f"✓ Screenshot saved to: {result}")
