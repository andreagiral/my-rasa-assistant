FROM rasa/rasa:3.6.10

WORKDIR /app
COPY . /app

USER root
RUN chmod +x /app/start.sh

EXPOSE 5005

# ─── train inside the container ──────────────────────────────────────────
RUN rasa train --no-prompt \
 && cp models/*.tar.gz models/latest_model.tar.gz
 
# Override the default ENTRYPOINT (which is `["rasa"]`)  
# and run your start.sh directly under bash
ENTRYPOINT ["bash", "/app/start.sh"]
