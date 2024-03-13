# HKUST-GZ-VPN

Bored of using Ivanti Secure Access outside of the campus and found that you couldn't visit ChatGPT or access your preferred sites due to global network restrictions? This Docker image is for you. It offers a flexible solution for selectively routing network traffic through your school's network while bypassing these restrictions, ensuring that you can access all your essential services without compromise.

## Usage

This image reads following environment variables:

| env          | required | description                                                                 |
| ------------ | -------- | --------------------------------------------------------------------------- |
| USER         | \*       | VPN username                                                                |
| PASS         | \*       | VPN password                                                                |
| URL          | \*       | VPN url                                                                     |
| OC_ARGS      |          | Additional arguments for openconnect                                        |

To use this image, simply set those envs.

## Examples

### HKUST-GZ-VPN

Content of config.env:

```
USER=abc123
PASS=ABC123
URL=remote.hkust-gz.edu.cn
OC_ARGS=--protocol=pulse --authgroup=Student
```
For students, set `--authgroup=Student`, for staff, set `--authgroup=Staff`.

Command:

```sh
# For X86_64 Users
docker run -d --name hkust-gz-vpn --env-file=config.env --privileged -p 11080:1080 yeahjack/hkust-gz-vpn:amd64
# For Mac M1 ARM64 Users
docker run -d --name hkust-gz-vpn --env-file=config.env --privileged -p 11080:1080 yeahjack/hkust-gz-vpn:m1_arm64
# You can also build the image locally
docker build -t hkust-gz-vpn .
docker run -d --name hkust-gz-vpn --env-file=config.env --privileged -p 11080:1080 hkust-gz-vpn
```

Access local port 11080 for a socks5 proxy, or use `nc` to forward ssh connection:

```sh
ssh -o ProxyCommand='nc -x 127.0.0.1:11080 %h %p' username@IP
```

# Credit
Thank you for repo [ocproxy-oci](https://github.com/thezzisu/ocproxy-oci), I could not make it without it.
