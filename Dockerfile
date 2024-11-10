FROM alpine

RUN apk add --no-cache python3
RUN apk add --no-cache openssl

COPY start.sh /root

RUN chmod +x /root/start.sh

CMD root/start.sh
