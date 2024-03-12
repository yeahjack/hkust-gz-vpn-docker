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
# LABEL maintainer="thezzisu <thezzisu@gmail.com>"
# LABEL description=""
RUN apk add libevent bash openconnect --no-cache
COPY --from=builder /root/ocproxy/ocproxy /usr/local/bin/
COPY entrypoint.sh /entrypoint.sh
#COPY keep-alive.sh /keep-alive.sh
#COPY connect.sh /connect.sh
RUN chmod +x /entrypoint.sh
#RUN chmod +x /keep-alive.sh
STOPSIGNAL SIGTERM
CMD ["/entrypoint.sh"]
# CMD ["/keep-alive.sh"]
