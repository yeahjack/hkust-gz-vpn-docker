# HKUST-GZ-VPN

Bored of using Ivanti Secure Access outside of the campus and found that you couldn't visit ChatGPT or access your preferred sites due to global network restrictions? This Docker image is for you. It offers a flexible solution for selectively routing network traffic through your school's network while bypassing these restrictions, ensuring that you can access all your essential services **without compromise**.

## Usage

You need to edit the content of `config.env`:

```
USER=abc123
PASS=ABC123
URL=remote.hkust-gz.edu.cn
OC_ARGS=--protocol=nc --authgroup=Student
```
`USER` is the prefix before `@` within your HKUST(GZ) e-mail address.

For students, set `--authgroup=Student`, for staff, set `--authgroup=Staff`.

# Deplyment

```sh
# For X86_64 Users
docker run -d --name hkust-gz-vpn --env-file=config.env --privileged -p 11080:1080 yeahjack/hkust-gz-vpn:amd64
# For Mac M1 ARM64 Users
docker run -d --name hkust-gz-vpn --env-file=config.env --privileged -p 11080:1080 yeahjack/hkust-gz-vpn:m1_arm64

# If you want, You can also build the image locally
docker build -t hkust-gz-vpn .
docker run -d --name hkust-gz-vpn --env-file=config.env --privileged -p 11080:1080 hkust-gz-vpn
```

# Usage

## SSH

Access local port 11080 for a socks5 proxy, or use `nc` to forward ssh connection:

```sh
ssh -o ProxyCommand='nc -x 127.0.0.1:11080 %h %p' username@IP
```

You could refer to `sshConfigSwitch.py` for a more convenient way to add/remove `ProxyCommand` to your ssh config file **in batch**. 

Note that remember to check the `config_path` variable in the `.py` file!

## Web services

For website services, you could refer to [Proxy SwitchyOmega](https://chromewebstore.google.com/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif) extension and add a new profile with `SOCKS5` proxy type with `http://127.0.0.1:11080`.

# Credit
Thank you for repo [ocproxy-oci](https://github.com/thezzisu/ocproxy-oci), I just made a few modifications to make it work for HKUST(GZ) users.
