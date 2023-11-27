"""Build template with mustache"""

import os
import sys
import time
import tomllib
import datetime
from playwright.sync_api import sync_playwright
import chevron
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

TEMPLATE_PATH = "invoice.html.template"
TOML_PATH = "invoice.toml"
OUTPUT_FOLDER = "build"


def load_template(path: str) -> str:
    """Load template"""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def load_toml(path: str) -> dict:
    """Load toml"""
    with open(path, "rb") as file:
        return tomllib.load(file)


def parse_template(template: str, data: dict) -> str:
    """Parse template"""

    def upper(text, render):
        """Upper filter"""
        result = render(text)
        return result.upper()

    def verboseDate(text, render):
        """Make a date into words
        i.e., "2023-11-30" -> Thu Nov 30, 2023
        """
        result = render(text)
        date = datetime.datetime.strptime(result, "%Y-%m-%d")
        return date.strftime("%a %b %d, %Y")

    data["upper"] = upper
    data["verboseDate"] = verboseDate

    return chevron.render(template, data)


def save_html(html: str, output_path: str):
    """Save html"""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html)
    # copy /static to build
    static_path = "static"
    if os.path.exists(static_path):
        os.system(f"cp -r {static_path} {OUTPUT_FOLDER}")
    print(f"🚀 Built html! The html is in {output_path}")


def save_pdf(html_fpath: str, output_path: str):
    """Make pdf from html"""
    print("🔧 Building pdf...")
    # open browser on html_file
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_fpath}")
        page.pdf(path=output_path, format="a4")
        browser.close()
    print(f"🚀 Built pdf! The pdf is in {output_path}")


def main():
    """Main"""
    template = load_template(TEMPLATE_PATH)
    invoice = load_toml(TOML_PATH)
    print(invoice)
    invoice_id = invoice["id"]
    html = parse_template(template, invoice)

    html_output_path = os.path.join(OUTPUT_FOLDER, f"invoice_{invoice_id}.html")
    pdf_output_path = os.path.join(OUTPUT_FOLDER, f"invoice_{invoice_id}.pdf")

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    save_html(html, html_output_path)
    html_path = os.path.abspath(html_output_path)
    save_pdf(html_path, pdf_output_path)


class EventHandler(FileSystemEventHandler):
    """Event handler for watching file system changes"""

    def on_modified(self, event):
        """On modified"""
        modify_path = os.path.abspath(event.src_path)
        if modify_path in [os.path.abspath(TEMPLATE_PATH), os.path.abspath(TOML_PATH)]:
            # wait for toml file to settle
            time.sleep(0.01)
            main()


def hot_reload_route():
    """Hot reload"""
    print("🔥 Hot reload... watching changes to invoice.html.template and invoice.toml")
    observer = Observer()
    observer.schedule(EventHandler(), ".")
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--hot":
        main()
        hot_reload_route()
    else:
        main()
