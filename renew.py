import os
import time
import os.path
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
            # 模拟人类先点击输入框，再逐字敲击键盘，确保网页框架能100%感知到输入
            page.locator("input[type='text']").first.click()
            page.keyboard.type(user, delay=100)
            
            page.locator("input[type='password']").first.click()
            page.keyboard.type(password, delay=100)
            
            print("步骤 3：正在发送登录请求（模拟按下键盘回车键）...")
            page.keyboard.press("Enter")
            
            print("步骤 4：等待登录跳转并检查结果...")
            time.sleep(6) 
            print(f"当前完成登录尝试后的网址为: {page.url}")
            
            # 💡 核心诊断：如果还在登录页，说明账号密码不对或被拦截，在此处立刻截取第一现场！
            if "login" in page.url:
                page.screenshot(path="error.png")
                raise Exception("【登录失败】未能成功跳转！依旧停留在登录页面。请去 GitHub Actions 底部下载最新的 error.png，看看网页上冒出了什么红字提示。")
            
            # 只有成功通过登录，才会来到这一步
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
            # 如果是步骤5、6报错，且前面没生成过截图，则在这里补抓一张
            if not os.path.exists("error.png"):
                page.screenshot(path="error.png")
            print("错误画面已保存为 error.png")
            raise e
            
        finally:
            browser.close()

if __name__ == "__main__":
    renew()
