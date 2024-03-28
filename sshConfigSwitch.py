import os

# 读取SSH配置文件的路径
config_path = "~/.ssh/config"


def read_ssh_config(path):
    full_path = os.path.expanduser(path)
    with open(full_path, "r") as file:
        text = file.read()
    text_split = text.split("\n\n")
    return text_split


def write_ssh_config(path, text):
    full_path = os.path.expanduser(path)
    with open(full_path, "w") as file:
        file.write(text)


def parse_ssh_configs(ssh_configs):
    """解析SSH配置列表，返回包含字典的列表。

    参数:
    - ssh_configs: 包含SSH配置的字符串列表。

    返回:
    - 包含配置字典的列表。
    """
    configs_list = []
    for config in ssh_configs:
        # 将配置分割成单行，以进行解析
        lines = config.split("\n")
        config_dict = {}
        for line in lines:
            # 移除行首尾的空格
            line = line.strip()
            if line:
                # 分割关键字和值
                key, value = line.split(None, 1)
                config_dict[key] = value
        configs_list.append(config_dict)
    return configs_list


def getAllCampusHosts(configs_list):
    """从配置列表中提取所有校园IP地址。

    参数:
    - configs_list: 包含配置字典的列表。

    返回:
    - 包含校园IP地址的列表。
    """
    campus_hosts = []
    for config in configs_list:
        if "HostName" in config and config["HostName"].startswith("10."):
            campus_hosts.append(config)
    return campus_hosts


def checkIfAdded(campus_hosts):
    """检查是否所有的campus_ips是否有ProxyCommand项，只要有一个没有就是False。

    参数:
    - campus_ips: 包含校园IP地址的列表。

    返回:
    - Bool
    """
    all_have_proxy = True
    for campus_host in campus_hosts:
        if not "ProxyCommand" in campus_host:
            all_have_proxy = False
            break
    return all_have_proxy


def addProxyCommand(campus_hosts):
    """为campus_hosts中的所有IP地址添加ProxyCommand。

    参数:
    - campus_hosts: 包含校园IP地址的列表。
    """
    for campus_host in campus_hosts:
        campus_host["ProxyCommand"] = "nc -X 5 -x 127.0.0.1:11080 %h %p"
    return campus_hosts


def removeProxyCommand(campus_hosts):
    """为campus_hosts中的所有IP地址移除ProxyCommand。

    参数:
    - campus_hosts: 包含校园IP地址的列表。
    """
    for campus_host in campus_hosts:
        del campus_host["ProxyCommand"]
    return campus_hosts


def addOrRemove(campus_hosts):
    """根据campus_hosts中的IP地址是否有ProxyCommand项，添加或移除ProxyCommand。

    参数:
    - campus_hosts: 包含校园IP地址的列表。
    """
    if checkIfAdded(campus_hosts):
        print("remove")
        return removeProxyCommand(campus_hosts)
    else:
        print("add")
        return addProxyCommand(campus_hosts)


def getNonCampusHosts(configs_list, campus_hosts):
    """从配置列表中提取所有非校园IP地址。

    参数:
    - configs_list: 包含配置字典的列表。
    - campus_hosts: 包含校园IP地址的列表。

    返回:
    - 包含非校园IP地址的列表。
    """
    non_campus_hosts = []
    for config in configs_list:
        if config not in campus_hosts:
            non_campus_hosts.append(config)

    # 剔除{}
    non_campus_hosts = [x for x in non_campus_hosts if x != {}]
    return non_campus_hosts


def getAllHosts(non_campus_hosts, campus_hosts):
    """合并校园IP地址和非校园IP地址。

    参数:
    - non_campus_hosts: 包含非校园IP地址的列表。
    - campus_hosts: 包含校园IP地址的列表。

    返回:
    - 合并后的列表。
    """
    return non_campus_hosts + campus_hosts


def format_ssh_configs(configs_list):
    """格式化SSH配置字典列表为字符串。

    参数:
    - configs_list: 包含配置字典的列表。

    返回:
    - 格式化后的字符串。
    """
    formatted_configs = ""
    for config in configs_list:
        formatted_configs += f"Host {config['Host']}\n"
        for key, value in config.items():
            if key != "Host":
                formatted_configs += f"  {key} {value}\n"
        formatted_configs += "\n"
    return formatted_configs


def main():
    ssh_configs = read_ssh_config(config_path)
    configs_list = parse_ssh_configs(ssh_configs)
    campus_hosts = getAllCampusHosts(configs_list)
    campus_hosts = addOrRemove(campus_hosts)
    non_campus_hosts = getNonCampusHosts(configs_list, campus_hosts)
    all_hosts = getAllHosts(non_campus_hosts, campus_hosts)
    formatted_configs = format_ssh_configs(all_hosts)
    write_ssh_config(config_path, formatted_configs)


if __name__ == "__main__":
    main()
