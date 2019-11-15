FROM alpine:edge
LABEL maintainer="Sergio Talens-Oliag <sto@iti.es>"
RUN apk update && apk add --no-cache openssl && rm -rf /var/cache/apk/*
ENTRYPOINT ["openssl"]
