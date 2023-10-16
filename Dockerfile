FROM python
WORKDIR /app
COPY index.html .
ENTRYPOINT python -m http.server
