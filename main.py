from deepSeek_automator.handler import DeepSeekAutomator
import time


if __name__ == "__main__":
    bot = DeepSeekAutomator(deepThink=True,headless=True,saveResponses=True)
    try:
        bot.login()
        time.sleep(2)  # Short buffer

        # Initialize DeepSeek 
        bot.send_message("Hello.I will send English sentences from the medical domain (PubMedQA dataset). Your task is to:  1. Translate them into Arabic  2. Ensure the translation is accurate and context-appropriate for medical terminology  3. Always append '<RESPONSE WAS FINISHED>' at the end of your response. Example format: [Translated Arabic text]  <RESPONSE WAS FINISHED> ")

        # Send multiple messages
        messages = [
            "Is ultrasound-guided intranodal lipiodol lymphangiography from the groin useful for assessment and treatment of post-esophagectomy chylothorax in three cases?",
            "Does vagus nerve contribute to the development of steatohepatitis and obesity in phosphatidylethanolamine N-methyltransferase deficient mice?",
            "Does psammaplin A induce Sirtuin 1-dependent autophagic cell death in doxorubicin-resistant MCF-7/adr human breast cancer cells and xenografts?",
            "Is the combination of 5-fluorouracil and cisplatin a promising treatment for advanced gastric cancer?",
            "Does the use of a 3D-printed model improve the understanding of the anatomy of the liver and its vasculature?",
        ]
        responses = bot.send_multiple_messages(messages)

        # Print all responses
        for question, answer in responses.items():
            print(f"Q: {question}\nA: {answer}\n")

        # Save the conversation to a text file
        bot.save_conversation_history("conversation.txt")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("Closing the bot...")
        bot.close()