from groq import Groq
from lutils import config, log, set_log_level
set_log_level("warn")

if config["keys.groq"]:
    client = Groq(api_key=config["keys.groq"])
    groq_key: bool = True
    with open("system.md", "r") as system_file:
        system_prompt = system_file.read()
else:
    log("warn", "API Key for Groq Required. Continuing without AI.")
    groq_key: bool = False


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
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages= messages,
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None,
    )
    full_response = ""
    for chunk in completion:
        delta = chunk.choices[0].delta.content
        print(delta or "", end="")
        full_response = full_response
        if delta:
            full_response += delta
    print("")
    return full_response


def mainloop() -> None:
    global messages
    while True:
        userinput = input("> ")
        match userinput:
            case "/quit":
                break
            case _:
                if groq_key:
                    messages = append_message(messages, userinput, "user")
                    response = ask_ai(messages)
                    messages = append_message(messages, response, "assistant")

                else:
                    log("warn", "AIas attempted to be triggered but no API Key was set.")
                    print(
                        "Leider hab ich dich nicht ganz verstanden, bitte versuche es nochmal."
                    )

messages: list
def main() -> None:
    global messages
    messages = [
            {
                "role": "system",
                "content": f"{system_prompt}",
            },
        ]
    print("Wie kann ich dir weiterhelfen?")
    mainloop()
    print("bye bye")
    


if __name__ == "__main__":
    main()
