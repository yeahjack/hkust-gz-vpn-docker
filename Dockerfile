FROM alpine as builder
WORKDIR /root
# Speedup for Chinese Mainland Users
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk add --no-cache git libevent-dev linux-headers autoconf automake build-base make bash \
  && git clone https://github.com/cernekee/ocproxy.git \
  && cd ocproxy \
  && ./autogen.sh \
  && ./configure \
  && make

FROM alpine
# Speedup for Chinese Mainland Users
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
LABEL maintainer="yeahjack <yxu409@connect.hkust-gz.edu.cn>"
LABEL description="This Docker image facilitates selective network routing for Ivanti-connected devices to a school's network, using port forwarding for enhanced access control."
RUN apk add libevent bash openconnect --no-cache
COPY --from=builder /root/ocproxy/ocproxy /usr/local/bin/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
STOPSIGNAL SIGTERM
CMD ["/entrypoint.sh"]