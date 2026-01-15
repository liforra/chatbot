from groq import Groq
from lutils import config, log, set_log_level, set_log_file, color
import sys


if config["log.level"]:
    set_log_level(config["log.level"])
else:
    set_log_level("warn")

if config["log.file"]:
    set_log_file(config["log.file"])
else:
    set_log_file(r"./chatbot.log")
if config["model.name"]:
    modelName: str = config["model.name"]
else:
    modelName: str = "openai/gpt-oss-120b"

if config["keys.groq"]:
    client = Groq(api_key=config["keys.groq"])
    groq_key: bool = True
    with open("system.md", "r") as system_file:
        system_prompt = system_file.read()
else:
    log("warn", "API Key for Groq Required. Continuing without AI.")
    groq_key: bool = False


if not sys.stdout.isatty():
    log(
        "warn",
        "Dieses Terminal unterstützt keine ANSI Codes. Falls diese Nachricht falsch ist, bitte kontaktieren sie den Developer von liforra-utils",
    )


def append_message(msg_list: list, message: str, role: str) -> list:
    log("debug", f"msg_list: {msg_list}")
    log("debug", f"message: {message}")
    log("debug", f"role: {role}")

    if role not in (("user", "assistant", "system")):
        log("fatal", "Role Must be Assistant, User or System.")
    message_dict = {
        "role": role,
        "content": message,
    }
    msg_list = msg_list + [message_dict]
    if not msg_list:
        raise Exception("Messages is now empty")
    return msg_list


def ask_ai(messages: list) -> list:
    global modelName
    completion: client = client.chat.completions.create(
        model=modelName,
        messages=messages,
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None,
    )
    full_response: str = ""
    for chunk in completion:
        delta = chunk.choices[0].delta.content
        # Falls GPT literal \\x1b liefert, konvertiere zu Escape-Zeichen
        if delta:
            delta_ansi = delta.replace("\\x1b", "\x1b")
            print(delta_ansi, end="", flush=True)
            full_response += delta_ansi
    print("")
    return full_response


first_question: bool = True


def mainloop() -> None:
    global messages, first_question, groq_key

    while True:
        # Prompt user
        userinput = input(color["cyan"] + "> " + color["reset"]).strip()
        if not userinput:
            continue

        # Commands
        if userinput.startswith("/"):
            args = userinput.removeprefix("/").split()
            match args[0]:
                case "quit":
                    print(color["yellow"] + "Beende Programm..." + color["reset"])
                    break
                case _:
                    log("warn", "Command not found.")
                    print(color["red"] + "Befehl nicht gefunden." + color["reset"])
            continue
        if not groq_key:
            first_question = True

        # Hardcoded response only on first question
        if first_question:
            first_question = False
            text = userinput.lower()
            handled = True
            hardcoded_response = ""

            match text:
                case _ if "geht nicht an" in text or "startet nicht" in text:
                    hardcoded_response = (
                        color["green"]
                        + "Schalten Sie das Geraät aus, prüfen Sie das Stromkabel und starten Sie es erneut. Sollte immer noch nichts passieren, trennen Sie alle Geräte und starten Sie nur das Gerät neu."
                        + color["reset"]
                    )

                case _ if "anmelden" in text or "login" in text:
                    hardcoded_response = (
                        color["green"]
                        + "Überprüfen Sie die Feststelltaste und stellen Sie sicher, dass Sie das richtige Passwort verwenden. Versuchen Sie danach, sich erneut anzumelden."
                        + color["reset"]
                    )

                case _ if "internet" in text:
                    hardcoded_response = (
                        color["green"]
                        + "Starten Sie den Router neu und prüfen Sie die Verbindung. Testen Sie danach, ob andere Webseiten erreichbar sind."
                        + color["reset"]
                    )

                case _ if "drucker" in text:
                    hardcoded_response = (
                        color["green"]
                        + "Prüfen Sie, ob der Drucker eingeschaltet ist, Papier vorhanden ist und die Verbindung zum Computer korrekt ist. Danach starten Sie einen Testdruck."
                        + color["reset"]
                    )

                case _ if "bildschirm" in text or "schwarz" in text:
                    hardcoded_response = (
                        color["green"]
                        + "Überprüfen Sie, ob der Bildschirm eingeschaltet ist und das Kabel fest sitzt. Testen Sie ggf. ein anderes Kabel oder einen anderen Anschluss."
                        + color["reset"]
                    )

                case _ if "kein ton" in text:
                    hardcoded_response = (
                        color["green"]
                        + "Überprüfen Sie, ob die Lautsprecher angeschaltet sind und die Lautstärke hoch genug ist. Prüfen Sie auch, ob der Ton am Computer nicht stummgeschaltet ist."
                        + color["reset"]
                    )

                case _ if "gelöscht" in text:
                    hardcoded_response = (
                        color["green"]
                        + "Falls Sie Dateien versehentlich gelöscht haben, prüfen Sie den Papierkorb. Wenn sie dort nicht sind, nutzen Sie ein Wiederherstellungsprogramm."
                        + color["reset"]
                    )

                case _ if "langsam" in text:
                    hardcoded_response = (
                        color["green"]
                        + "Starten Sie den Computer neu und schließen Sie unnötige Programme. Prüfen Sie, ob genügend Speicherplatz frei ist."
                        + color["reset"]
                    )

                case _:
                    handled = False

            if handled:
                print(hardcoded_response)
                if groq_key:
                    messages = append_message(messages, userinput, "user")
                    messages = append_message(messages, hardcoded_response, "assistant")
                
                continue

        # Fallback: AI response
        global response
        if groq_key:
            print(color["yellow"] + "Ralf schreibt..." + color["reset"])
            messages = append_message(messages, userinput, "user")
            try: 
                response = ask_ai(messages)
                messages = append_message(messages, response, "assistant")
            except Exception as e:
                log("warn", "No connection to Groq, Advanced AI features are turned off now.")
                groq_key = False

                
        else:
            log("warn", "AI was attempted to be triggered but no API Key was set, or Internet connection was lost.")
            print(
                color["red"]
                + "Leider habe ich Sie nicht ganz verstanden. Bitte versuchen Sie es noch einmal."
                + color["reset"]
            )


messages: list


def main() -> None:
    global messages
    if config["keys.groq"]:
        messages = [
            {
                "role": "system",
                "content": f"{system_prompt}",
            },
        ]
    print("Wie kann ich dir weiterhelfen?")
    try:
        mainloop()
    except KeyboardInterrupt:
        ...
    print("\nIch hoffe ich konnte ihnen helfen, bis zum nächsten mal.")


if __name__ == "__main__":
    main()
