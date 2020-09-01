FROM ubuntu:18.04

RUN apt update && apt install -y python3 python3-pip nginx python3-venv git curl supervisor
RUN pip3 install --user virtualenv

COPY ./backend /backend
COPY ./frontend /frontend

WORKDIR /frontend
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
RUN export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  && [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  && nvm install node && nvm install-latest-npm  && npm install && npm link @angular/cli@8.3.20


WORKDIR /backend/badbe/

RUN pip3 install -r requirements.txt
RUN python3 -m venv .venv

COPY badbe.nginx /etc/nginx/sites-enabled/default

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY start_frontend.sh /frontend/start_frontend.sh

CMD ["/usr/bin/supervisord"]
