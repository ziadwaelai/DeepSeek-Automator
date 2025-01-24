import time
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import configparser

class DeepSeekAutomator:
    def __init__(self,deepThink=False,uc=True,headless=False,saveResponses=True):
        self.deepThink = deepThink
        self.uc = uc
        self.headless = headless
        self.saveResponses = saveResponses
        self.driver = Driver(uc=True, headless=headless)
        self.wait = WebDriverWait(self.driver, 15) 
        self.load_credentials()


    def load_credentials(self):
        """Load credentials from config file"""
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.email = config['credentials']['Email']
        self.password = config['credentials']['Password']

    def login(self):
        try:
            self.driver.get("https://chat.deepseek.com/")
            
            # Wait for login elements
            email_field = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[3]/div[1]/div/input')
            ))
            email_field.send_keys(self.email)
            
            password_field = self.driver.find_element(
                By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[4]/div[1]/div/input'
            )
            password_field.send_keys(self.password)
            
            # Handle checkbox
            checkbox = self.driver.find_element(
                By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[5]/div[1]/div/div[1]/div'
            )
            checkbox.click()
            
            # Login button
            login_btn = self.driver.find_element(
                By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[6]'
            )
            login_btn.click()
            
            # Wait for chat interface
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="chat-input"]')
            ))
            if self.deepThink:
                time.sleep(1)  # Short buffer
                self.click_deepThink_option()

            print("Login successful")
            
        except TimeoutException as e:
            print(f"Login failed: {str(e)}")
            self.driver.save_screenshot('login_error.png')
            raise

    def send_message(self, message):
        try:
            if not self.headless:
                self.driver.uc_gui_click_captcha()
            chat_input = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="chat-input"]')
            ))
            chat_input.send_keys(message)
            chat_input.send_keys(Keys.RETURN)
            print(f"Message sent: {message}")

            # Wait for response dynamically
            return self.wait_for_response()
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return None

    def wait_for_response(self):
        """Wait until the response contains '<RESPONSE WAS FINISHED>'"""
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ds-markdown')]")))

            # Keep track of how many responses exist before sending
            previous_responses = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'ds-markdown')]")
            response_index = len(previous_responses)  # Index of the new response
            
            timeout = 150  if self.deepThink else 100  # Longer timeout for DeepThink
            start_time = time.time()
            final_text = ""

            while time.time() - start_time < timeout:
                responses = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'ds-markdown')]")
                
                if len(responses) > response_index:  # Ensure a new response appeared
                    last_response = responses[-1]
                    current_text = last_response.text.strip()
                    print("Current Response:", current_text)  # Debugging

                    if "<RESPONSE WAS FINISHED>" in current_text:  
                        print("Full response detected!")
                        final_text = current_text.replace("<RESPONSE WAS FINISHED>", "").strip()
                        break
                
                time.sleep(2)  # Small delay to avoid excessive CPU usage

            return final_text if final_text else "Response timeout or incomplete response"

        except TimeoutException:
            print("Response timeout")
            return None

    def send_multiple_messages(self, messages):
        """Send multiple messages one by one and return all responses"""
        start_time = time.time()
        responses = {}
        for msg in messages:
            response = self.send_message(msg)
            responses[msg] = response
            self.save_response({msg: response}, "responses.txt") if self.saveResponses else None
            time.sleep(2)  # Small delay between messages
        print(f"Total time in hours: {(time.time() - start_time) / 3600:.2f}")
        return responses  # Return all responses
    

    def save_conversation_history(self, file_name):
        """Save conversation history correctly by distinguishing user prompts and AI responses"""
        
        # Identify user inputs (prompts)
        user_prompts = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'fbb737a4')]")
        
        # Identify AI responses
        ai_responses = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'ds-markdown')]")

        # Ensure there's something to save
        if not user_prompts or not ai_responses:
            print("No conversation found.")
            return

        with open(file_name, "w", encoding="utf-8") as file:
            for i in range(len(user_prompts)):  # Loop through user prompts
                prompt_text = user_prompts[i].text.strip() if i < len(user_prompts) else "N/A"
                response_text = ai_responses[i].text.strip() if i < len(ai_responses) else "N/A"

                response_text = response_text.replace("<RESPONSE WAS FINISHED>", "").strip()
                
                file.write(f"Q: {prompt_text}\nA: {response_text}\n\n")

        print(f"Conversation saved to {file_name}")


    
    def save_response(self, responses, file_name):
        """Append multiple responses to the file properly""" 
        with open(file_name, "a", encoding="utf-8") as file:
            for question, answer in responses.items():
                file.write(f"Q: {question}\nA: {answer}\n\n")
        print(f"Responses saved to {file_name}")


    def click_deepThink_option(self):
        """Clicks on the 'DeepThink (R1)' option button."""
        try:
            # Wait for the button containing 'DeepThink (R1)'
            deepseek_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'DeepThink (R1)')]")
            ))

            # Scroll to the button if necessary
            self.driver.execute_script("arguments[0].scrollIntoView();", deepseek_button)

            # Click the button
            deepseek_button.click()
            print("DeepSeek option 'DeepThink (R1)' clicked successfully!")

        except Exception as e:
            print(f"Error clicking DeepSeek option: {str(e)}")


    def close(self):
        self.driver.quit()
