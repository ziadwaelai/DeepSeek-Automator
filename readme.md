# **DeepSeek Automator**
**Automate interactions with DeepSeek AI using Selenium and Python.**  
This script logs into DeepSeek, sends messages, retrieves responses, and saves conversation history.

---

## **📌 Features**
✔ **Automated Login**: Logs into DeepSeek using stored credentials.  
✔ **DeepThink Mode**: Supports optional DeepThink (R1) mode.  
✔ **Message Automation**: Sends multiple messages and collects responses.  
✔ **Dynamic Response Handling**: Waits until the AI finishes responding.  
✔ **Response Saving**: Stores responses in a text file.  
✔ **Headless Mode Support**: Runs without a visible browser.  

---

## **⚙️ Installation**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/ziadwaelai/DeepSeek-Automator.git
cd deepseek-automator
```

### **2️⃣ Install Dependencies**
Ensure you have **Python 3.11+** installed. Then install required libraries:
```bash
pip install -r requirements.txt
```

### **3️⃣ Configure Credentials**
Create a `config.ini` file in the project root:
```ini
[credentials]
Email = your-email@example.com
Password = yourpassword
```

---

## **🚀 Usage**
### **Run the Bot**
```bash
python deepseek_automator.py
```

### **Python Usage**
```python
from deepSeek_automator.handler import DeepSeekAutomator

bot = DeepSeekAutomator(deepThink=True, headless=True, saveResponses=True)
bot.login()

response = bot.send_message("What is the capital of France?")
print(response)

bot.save_conversation_history("conversation.txt")
bot.close()
```

---

## **🔧 Configuration Options**
When initializing `DeepSeekAutomator`:

| Parameter       | Type    | Default | Description |
|----------------|--------|---------|-------------|
| `deepThink`    | `bool` | `False` | Enables DeepThink (R1) mode. |
| `uc`           | `bool` | `True`  | Uses undetectable Selenium mode. |
| `headless`     | `bool` | `False` | Runs browser in headless mode. |
| `saveResponses`| `bool` | `True`  | Saves responses to a file. |

---

## **🛠️ Features in Detail**
### ✅ **Automated Login**
- Loads credentials from `config.ini`.
- Handles login elements dynamically.

### ✅ **Message Automation**
- Sends messages to DeepSeek AI.
- Waits for the **full response** (`<RESPONSE WAS FINISHED>`).
- Saves responses automatically.

### ✅ **Conversation History Saving**
- Extracts **both user prompts & AI responses**.
- Saves conversations as:
  ```
  Q: What is AI?
  A: Artificial Intelligence (AI) is...
  ```

### ✅ **DeepThink Mode**
- Enables **DeepThink (R1)** with `deepThink=True`.

### ✅ **Headless Mode**
- Runs without opening a visible browser.

---

## **📄 Example Output**
```
Login successful
Message sent: What is the capital of France?
Current Response: The capital of France is Paris. <RESPONSE WAS FINISHED>
Full response detected!
Q: What is the capital of France?
A: The capital of France is Paris.

Conversation saved to conversation.txt
```

---

## **📌 Known Issues & Fixes**
❌ **Bot is stuck waiting for a response?**  
✔ Increase the timeout value in `wait_for_response()`.

❌ **DeepThink (R1) button is not clicking?**  
✔ Check if the button XPath has changed.

❌ **Wrong login credentials?**  
✔ Ensure `config.ini` is set up correctly.



## **📩 Contact**
For support, reach out to:  
📧 Email: `ziadwael142@gmail.com`  


---

### **🚀 Now You're Ready to Automate DeepSeek AI!**  
