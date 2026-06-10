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
            print("步骤 1：正在打开登录页面...")
            page.goto("https://panel.epichost.pl/auth/login", wait_until="networkidle")
            
            user = os.environ.get('PANEL_USER', '')
            password = os.environ.get('PANEL_PASS', '')
            
            print("步骤 2：正在填写账号和密码...")
            # 智能匹配：寻找包含用户名文本的区域或标准输入框，无视大小写，100%精准定位
            page.locator("input[type='text'], input[name='username']").first.fill(user)
            page.locator("input[type='password'], input[name='password']").first.fill(password)
            
            print("步骤 3：正在点击紫色的登录按钮 (LOGOWANIE)...")
            # 寻找带有 LOGOWANIE 文本的按钮并点击
            page.locator("button:has-text('LOGOWANIE'), button[type='submit']").first.click()
            
            print("步骤 4：登录完成，等待页面跳转中...")
            time.sleep(10) # 留出 10 秒给系统写入登录状态
            print(f"当前跳转后的网址为: {page.url}")
            
            # 直接强行切入你的服务器控制台
            server_url = "https://panel.epichost.pl/server/b3a91d2a"
            print(f"步骤 5：正在直接进入服务器控制台: {server_url}")
            page.goto(server_url, wait_until="networkidle")
            time.sleep(5)
            
            print("步骤 6：正在寻找并点击续期按钮...")
            renew_btn = page.get_by_text("ADD 2 HOUR(S)", exact=False)
            
            if renew_btn.count() > 0:
                renew_btn.first.click()
                print("✅ 成功：续期按钮点击成功！")
                time.sleep(2)
            else:
                raise Exception("失败：在当前控制台页面未找到带有 'ADD 2 HOUR(S)' 文本的按钮。")
            
        except Exception as e:
            print("❌ 运行过程中出现错误:")
            print(e)
            # 保留错误截图功能
            page.screenshot(path="error.png")
            print("错误画面已保存为 error.png")
            raise e
            
        finally:
            browser.close()

if __name__ == "__main__":
    renew()
