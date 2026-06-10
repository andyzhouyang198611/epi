import os
import time
from playwright.sync_api import sync_playwright

def renew():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            print("1. 正在访问登录页面...")
            page.goto("https://panel.epichost.pl/auth/login")
            page.wait_for_load_state('networkidle')
            
            print("2. 正在填写账号和密码...")
            page.fill('input[type="text"]', os.environ['PANEL_USER']) 
            page.fill('input[type="password"]', os.environ['PANEL_PASS'])
            page.click('button[type="submit"]')
            
            print("3. 等待登录完成，加载服务器列表 (Dashboard)...")
            page.wait_for_load_state('networkidle')
            time.sleep(5) 
            
            print("4. 正在点击服务器 ID 进入控制台...")
            # 模拟你的操作：点击带有该 ID 文本的元素
            page.click("text='b3a91d2a'") 
            page.wait_for_load_state('networkidle')
            time.sleep(5) 
            
            print("5. 查找并点击续期按钮...")
            # 此时页面已经跳转到具体的服务器控制台，直接点击续期
            page.click("text='ADD 2 HOUR(S)'", timeout=15000)
            print("✅ 成功点击续期按钮！")
            
        except Exception as e:
            print("❌ 执行过程中出现错误:")
            print(e)
            
            # 如果出错，保存截图以便在 Actions 日志中排查
            page.screenshot(path="error.png")
            print("已保存错误截图为 error.png")
            
        finally:
            browser.close()

if __name__ == "__main__":
    renew()
