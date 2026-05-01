import ctypes
import sys

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable,
        " ".join(f'"{a}"' for a in sys.argv), None, 1
    )
    sys.exit(0)

import bot
import capture_templates
import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

ASCII_ART = r"""
   ___         __        ____
  / _ | __ __ / /_ ___  / __/___ _______ _
 / __ |/ // // __// _ \/ _/ / _ `/ __/  ' \
/_/ |_|\_,_/ \__/ \___/_/   \_,_/_/ /_/_/_/
"""


def show_header():
    console.print(Panel(
        f"[bold cyan]{ASCII_ART}[/bold cyan]",
        subtitle="[dim]Ctrl+C pour quitter[/dim]",
        expand=False,
        border_style="cyan",
    ))


def run_menu():
    while True:
        console.clear()
        show_header()

        choice = questionary.select(
            "Que veux-tu faire ?",
            choices=[
                questionary.Choice("Calibrer les templates", value="calibrate"),
                questionary.Choice("Lancer le bot", value="run"),
                questionary.Separator(),
                questionary.Choice("Quitter", value="quit"),
            ],
            pointer="»",
        ).ask()

        if choice is None or choice == "quit":
            console.print("[dim]À bientôt.[/dim]")
            break

        if choice == "run":
            console.print("[bold green]Lancement du bot...[/bold green]")
            try:
                bot.main()
            except KeyboardInterrupt:
                pass
            console.print("[yellow]Bot arrêté. Retour au menu...[/yellow]")
            questionary.press_any_key_to_continue(
                "Appuie sur une touche pour revenir au menu."
            ).ask()

        elif choice == "calibrate":
            console.print("[bold blue]Lancement de la calibration...[/bold blue]")
            try:
                capture_templates.main()
            except KeyboardInterrupt:
                pass
            console.print("[yellow]Calibration terminée. Retour au menu...[/yellow]")
            questionary.press_any_key_to_continue(
                "Appuie sur une touche pour revenir au menu."
            ).ask()


if __name__ == "__main__":
    run_menu()
