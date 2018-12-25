# Docker

**docker-compose.yml**
```yml
version: "3"

services:
  kotori:
    image: joshava/kotori
    ports:
      - 80:80
    environment:
      KOTORI_CONFIG: /app/config.yml
    volumes:
      - /opt/kotori/config.yml:/app/config.yml
      - /opt/kotori/image:/image
      - cache:/image-cache

volumes:
  cache:
```
`/image` and `/image-cache` are locations defined in the configuration.

`/image` is not needed if you are not using local storage.
`/image-cache` is not needed if you are not using cache. (Not recommended)