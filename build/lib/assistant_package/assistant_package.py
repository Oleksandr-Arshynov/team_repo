from assistant_package.assistant import PersonalAssistant


def main_function():
    assistant = PersonalAssistant()
    assistant.load()
    assistant.load_notes()
    assistant.run()
    return assistant


if __name__ == "__main__":
    assistant_instance = main_function()
    user_input = "example"
    assistant_instance.analyze_user_input(user_input)
