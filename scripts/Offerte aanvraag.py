import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.keypro.nl/")
    page.get_by_text("Accepteren en doorgaan").click()
    page.get_by_role("link", name="Offerte aanvragen", exact=True).click()
    page.get_by_label("Type project").select_option("11")
    page.get_by_label("Type project").press("Tab")
    page.get_by_role("textbox", name="Voor- en achternaam*").fill("Josanne Test")
    page.get_by_role("textbox", name="Voor- en achternaam*").press("Tab")
    page.locator(".phone-form-field > .language-switch > .language-switch__languages").press("Tab")
    page.get_by_role("textbox", name="Telefoonnummer*").fill("06-test")
    page.get_by_role("textbox", name="Telefoonnummer*").press("Tab")
    page.get_by_role("textbox", name="E-mailadres*").fill("josanne.de.groot@keypro.nl")
    page.get_by_role("textbox", name="E-mailadres*").press("Tab")
    page.get_by_role("textbox", name="Bedrijfsnaam").fill("Test")
    page.get_by_role("textbox", name="Bedrijfsnaam").press("Tab")
    page.get_by_role("textbox", name="Kan je ons alvast iets").fill("Dit is een test of de offerte aanvraag op keypro.nl goed werkt. Test uitgevoerd door Josanne.")
    page.get_by_role("button", name="Offerte aanvragen").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

