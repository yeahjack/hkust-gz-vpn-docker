#!/bin/bash

# 获取环境变量
user=$USER
pass=$PASS
url=$URL
oc_args=$OC_ARGS

# 检查必要的环境变量
if [ -z "$user" ] || [ -z "$pass" ]; then
  echo "Must provide USER and PASS env"
  exit 1
fi

if [ -z "$url" ]; then
  echo "Must provide URL env"
  exit 1
fi

# 将 OC_ARGS 拆分成单独的参数
IFS=' ' read -ra oc_args_list <<< "$oc_args"

# 定义一个启动 openconnect 的函数
function start_openconnect {
  echo $pass | openconnect --passwd-on-stdin "${oc_args_list[@]}" --script-tun --script "ocproxy -D 1080 -g" --user $user $url
}

# 定义一个标志,用于指示是否继续循环
keep_running=true

# 定义一个函数,用于在接收到 SIGINT 或 SIGTERM 时设置标志
function stop_running {
  keep_running=false
}

# 设置信号处理程序
trap stop_running SIGINT SIGTERM

# 循环,重新启动 openconnect 如果它退出,直到标志被设置为 false
while $keep_running; do
  start_openconnect
  echo "openconnect exited with status $?"
done

echo "Script stopped"