import os
import time
from playwright.sync_api import sync_playwright

def renew():
    with sync_playwright() as p:
        proxy_server = os.environ.get('PROXY_SERVER', '')
        proxy_config = {"server": proxy_server} if proxy_server else None

        if proxy_config:
            print("【系统提示】检测到本地 HY2 代理，正在通过加密隧道启动伪装浏览器...")
        else:
            print("【系统提示】未检测到代理，将使用默认网络...")

        # 💡 核心改动：注入谷歌浏览器官方的防检测内核参数，抹除 navigator.webdriver 痕迹
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled', # 禁用自动化控制特征（关键）
                '--no-sandbox',
                '--disable-infobars',
                '--window-size=1280,720'
            ]
        )
        
        # 伪装完整的语言、时区和请求头，不给 CF 留下任何机房环境的破绽
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720},
            locale="en-US",
            timezone_id="America/New_York",
            proxy=proxy_config
        )
        page = context.new_page()
        
        try:
            print("步骤 1：正在通过 HY2 节点秘密接近登录页面...")
            page.goto("https://panel.epichost.pl/auth/login", wait_until="networkidle")
            time.sleep(3) # 故意滑稽地停顿一下，模仿人类观察网页
            
            user = os.environ.get('PANEL_USER', '')
            password = os.environ.get('PANEL_PASS', '')
            
            print("步骤 2：正在模拟人类键盘敲击习惯录入凭证...")
            page.locator("input[type='text']").first.click()
            page.keyboard.type(user, delay=120) # 模拟人类每个字母敲击间隔 120 毫秒
            time.sleep(0.5)
            
            page.locator("input[type='password']").first.click()
            page.keyboard.type(password, delay=150)
            time.sleep(0.8)
            
            print("步骤 3：正在敲击键盘回车发送登录请求...")
            page.keyboard.press("Enter")
            
            print("步骤 4：正在等待服务器处理登录状态变更...")
            time.sleep(10) 
            print(f"当前完成登录尝试后的网址为: {page.url}")
            
            if "login" in page.url:
                page.screenshot(path="error.png")
                raise Exception("【登录失败】即使使用了 HY2 + 浏览器伪装，依旧被卡在登录页。请下载 error.png 确认是否依然弹出了图形验证码。")
            
            server_url = "https://panel.epichost.pl/server/b3a91d2a"
            print(f"步骤 5：无感通过防线！正在直奔目标控制台: {server_url}")
            page.goto(server_url, wait_until="networkidle")
            time.sleep(6)
            
            print("步骤 6：正在执行最后一击（寻找续期按钮）...")
            renew_btn = page.get_by_text("ADD 2 HOUR(S)", exact=False)
            
            if renew_btn.count() > 0:
                renew_btn.first.click()
                print("✅ 成功：续期按钮点击成功！本次全链路对抗完美胜利。")
                time.sleep(2)
            else:
                raise Exception("失败：已成功进入控制台，但页面上没找到可点的 'ADD 2 HOUR(S)' 按钮。")
            
        except Exception as e:
            print("❌ 运行过程中出现错误:")
            print(e)
            page.screenshot(path="error.png")
            print("最新错误画面已截取保存为 error.png")
            raise e
            
        finally:
            browser.close()

if __name__ == "__main__":
    renew()
