import os
import time
from playwright.sync_api import sync_playwright

def renew():
    with sync_playwright() as p:
        # 从环境变量读取代理配置
        proxy_server = os.environ.get('PROXY_SERVER', '')
        
        # 组装 Playwright 的代理参数
        proxy_config = None
        if proxy_server:
            print(f"检测到代理配置，正在通过代理启动浏览器...")
            proxy_config = {"server": proxy_server}
        else:
            print("未检测到代理配置，将使用默认机房 IP 运行。")

        browser = p.chromium.launch(headless=True)
        
        # 将 proxy 传入 context
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            proxy=proxy_config
        )
        page = context.new_page()
        
        try:
            print("步骤 1：正在打开登录页面...")
            page.goto("https://panel.epichost.pl/auth/login", wait_until="networkidle")
            
            user = os.environ.get('PANEL_USER', '')
            password = os.environ.get('PANEL_PASS', '')
            
            print("步骤 2：正在填写账号和密码...")
            page.locator("input[type='text']").first.click()
            page.keyboard.type(user, delay=100)
            
            page.locator("input[type='password']").first.click()
            page.keyboard.type(password, delay=100)
            
            print("步骤 3：正在发送登录请求...")
            page.keyboard.press("Enter")
            
            print("步骤 4：等待登录跳转并检查结果...")
            time.sleep(8) 
            print(f"当前页面网址为: {page.url}")
            
            if "login" in page.url:
                page.screenshot(path="error.png")
                raise Exception("【登录失败】即使使用了代理，依然停留在登录页面。请检查账号密码或代理IP是否干净。")
            
            server_url = "https://panel.epichost.pl/server/b3a91d2a"
            print(f"步骤 5：正在直接进入服务器控制台: {server_url}")
            page.goto(server_url, wait_until="networkidle")
            time.sleep(5)
            
            print("步骤 6：正在寻找并点击续期按钮...")
            renew_btn = page.get_by_text("ADD 2 HOUR(S)", exact=False)
            
            if renew_btn.count() > 0:
                renew_btn.first.click()
                print("✅ 成功：续期按钮点击成功！通过代理完美绕过。")
                time.sleep(2)
            else:
                raise Exception("失败：在当前控制台页面未找到带有 'ADD 2 HOUR(S)' 文本的按钮。")
            
        except Exception as e:
            print("❌ 运行过程中出现错误:")
            print(e)
            page.screenshot(path="error.png")
            print("错误画面已保存为 error.png")
            raise e
            
        finally:
            browser.close()

if __name__ == "__main__":
    renew()
