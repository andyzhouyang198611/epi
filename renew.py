import os
import time
from playwright.sync_api import sync_playwright

def renew():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 模拟真实的浏览器请求头，降低被拦截的风险
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("1. 正在访问登录页面...")
            page.goto("https://panel.epichost.pl/auth/login", wait_until="networkidle")
            
            print("2. 正在填写账号和密码...")
            page.fill('input[type="text"]', os.environ['PANEL_USER']) 
            page.fill('input[type="password"]', os.environ['PANEL_PASS'])
            
            # 使用更宽泛的匹配来点击登录按钮
            page.click("button:has-text('LOGOWANIE'), button[type='submit']")
            
            print("3. 等待登录跳转...")
            time.sleep(8)  # 给足够的缓冲时间让服务器写入 Cookie
            
            # -----------------------------------------------------------
            # 💡 核心改动：不再点击，登录后直接肉身翻墙进入目标控制台
            # -----------------------------------------------------------
            server_url = "https://panel.epichost.pl/server/b3a91d2a"
            print(f"4. 正在直接跨越到服务器控制台: {server_url}")
            page.goto(server_url, wait_until="networkidle")
            time.sleep(8)  # 翼龙面板加载后端数据较慢，多等会
            
            print("5. 正在寻找并点击续期按钮...")
            # 采用更精确的选择器，匹配包含 ADD 2 HOUR(S) 的按钮
            renew_btn = page.locator("button:has-text('ADD 2 HOUR(S)'), a:has-text('ADD 2 HOUR(S)')")
            
            if renew_btn.count() > 0:
                renew_btn.first.click()
                print("✅ 成功点击续期按钮！")
                time.sleep(2)  # 等待点击后的请求发送完毕
            else:
                raise Exception("在当前页面未找到带有 'ADD 2 HOUR(S)' 文本的按钮")
            
        except Exception as e:
            print("❌ 执行过程中出现错误:")
            print(e)
            # 强制保存截图
            page.screenshot(path="error.png")
            print("已将当前错误画面保存为 error.png")
            raise e  # 抛出异常让 GitHub Actions 捕获
            
        finally:
            browser.close()

if __name__ == "__main__":
    renew()
