import os
import time
from playwright.sync_api import sync_playwright

def renew():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("Step 1: Opening login page...")
            page.goto("https://panel.epichost.pl/auth/login", wait_until="networkidle")
            
            user = os.environ.get('PANEL_USER', '')
            password = os.environ.get('PANEL_PASS', '')
            
            # 💡 按照你的指示：直接根据网页上的波兰语文本寻找对应的输入框
            print("Step 2: Locating fields by exact visual Polish text...")
            
            # 找到文本 "NAZWA UŻYTKOWNIKA LUB ADRES E-MAIL" 紧跟其后的第一个输入框并填写
            page.locator("xpath=//*[contains(text(), 'NAZWA UŻYTKOWNIKA')]/following::input[1]").fill(user)
            
            # 找到文本 "HASŁO" 紧跟其后的第一个输入框并填写
            page.locator("xpath=//*[contains(text(), 'HASŁO')]/following::input[1]").fill(password)
            
            # 💡 按照你的指示：直接点击图片上显示的那个紫色 "LOGOWANIE" 按钮
            print("Step 3: Clicking the purple 'LOGOWANIE' button...")
            page.locator("xpath=//*[contains(text(), 'LOGOWANIE')]").click()
            
            print("Step 4: Waiting for session redirection...")
            time.sleep(10) # 留出 10 秒让登录后的跳转完全加载完毕
            print(f"Current URL after login: {page.url}")
            
            # 直接强行切入你的服务器控制台
            server_url = "https://panel.epichost.pl/server/b3a91d2a"
            print(f"Step 5: Navigating to server console: {server_url}")
            page.goto(server_url, wait_until="networkidle")
            time.sleep(5)
            
            print("Step 6: Locating and clicking renew button...")
            renew_btn = page.get_by_text("ADD 2 HOUR(S)", exact=False)
            
            if renew_btn.count() > 0:
                renew_btn.first.click()
                print("SUCCESS: Renew button clicked successfully!")
                time.sleep(2)
            else:
                raise Exception("FAILED: 'ADD 2 HOUR(S)' button not found on this page.")
            
        except Exception as e:
            print("ERROR: Something went wrong during execution:")
            print(e)
            # 依然保留错误截图功能，万一失败了方便看最新画面
            page.screenshot(path="error.png")
            print("Error screenshot saved as error.png")
            raise e
            
        finally:
            browser.close()

if __name__ == "__main__":
    renew()
