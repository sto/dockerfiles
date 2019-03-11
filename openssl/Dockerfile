FROM alpine
LABEL maintainer="Sergio Talens-Oliag <sto@uv.es>"
RUN apk update && apk add --no-cache openssl && rm -rf /var/cache/apk/*
ENTRYPOINT ["openssl"]
