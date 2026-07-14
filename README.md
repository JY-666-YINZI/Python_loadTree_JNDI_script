# Python_loadTree_JNDI_script
Due to improper permission checks on the app server, attackers can trigger JNDI injection via the "loadTree" interface to achieve RCE (requires lower JDK versions). Legacy vuln, patched in August. EAS is also affected with a different path.**应用服务器权限验证不当，导致攻击者可以向loadTree接口执行JNDI注入，造成远程代码执行漏洞。利用该漏洞需低版本JDK。（漏洞比较旧，8月份补丁已出，**EAS也存在类似漏洞，只是路径不一样）
