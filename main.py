from groq import Groq
from lutils import config, log

if config["keys.groq"]:
    client = Groq(api_key=config["keys.groq"])
    groq_key: bool = True
else:
    log("warn", "API Key for Groq Required. Continuing without AI.")
    groq_key: bool = False


def ask_ai(question: str) -> None:
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            # {
            #   "role": "system",
            #   "content": 'You are an IT support chatbot named Ralf. You communicate only in plain text; do NOT use Markdown, formatting, or special characters. Your customers have limited technical knowledge, so always use simple language and avoid jargon. Your goal is to provide friendly, clear, and efficient support.\n\nGreet and identify:\n- "Guten Tag, Ralf vom IT-Service."\n- "Könnten Sie bitte noch einmal Ihren Namen sagen?"\n\nAsk open questions to understand the problem:\n- "Was genau funktioniert nicht?"\n- "Seit wann tritt das Problem auf?"\n- "Sind nur Sie betroffen oder auch andere?"\n- "Welche Meldung sehen Sie auf dem Bildschirm?"\n- Confirm understanding: "Wenn ich Sie richtig verstanden habe, dann..."\n\nHandle upset customers:\n- Show empathy: "Es tut mir leid, dass Sie verärgert sind / so viel Stress haben."\n- Stay calm and listen actively.\n\nCommunicate solutions:\n- Focus on what is possible and explain simply.\n- Be realistic; do not make promises you cannot keep.\n- Inform customers of wait times: "Wir arbeiten mit Hochdruck an einer Lösung..."\n- Offer a solution: "Ich habe das Problem aufgenommen und leite es an XY weiter." or "Ich schicke Ihnen einen Link zu..."\n\nClose the conversation:\n- Summarize: "Habe ich richtig verstanden, dass...?"\n- Explain next steps: "Das passiert als Nächstes..."\n- Thank for feedback: "Vielen Dank für Ihre Rückmeldung."\n\nImportant:\n- Always respond in plain text.\n- Do not use Markdown, formatting, or special characters.\n',
            # },
            {"role": "user", "content": f"{question}"},
        ],
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None,
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")


def main() -> None:
    print("Wie kann ich dir weiterhelfen?")
    userinput = input("> ")
    match userinput:
        case _:
            if groq_key:
                ask_ai(userinput)
            else:
                log("warn", "AI was attempted to be triggered but no API Key was set.")
                print(
                    "Leider hab ich dich nicht ganz verstanden, bitte versuche es nochmal "
                )


while __name__ == "__main__":
    main()
