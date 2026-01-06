from groq import Groq
from lutils import config, log

if config["keys.groq"]:
    client = Groq(api_key=config["keys.groq"])
    groq_key: bool = True
    with open("system.md", "r") as system_file:
        system_prompt = system_file.read()
else:
    log("warn", "API Key for Groq Required. Continuing without AI.")
    groq_key: bool = False


def ask_ai(question: str) -> None:
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": f"{system_prompt}",
            },
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
                    "Leider hab ich dich nicht ganz verstanden, bitte versuche es nochmal."
                )


while __name__ == "__main__":
    main()
