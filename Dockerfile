FROM amsterdam/python:3.8-buster as tests
MAINTAINER datapunt@amsterdam.nl

WORKDIR /app_install
COPY requirements.txt .
RUN pip install -r requirements.txt

# setup folder before switching to user
RUN mkdir /app/.tox
RUN mkdir /app/.pyenv

WORKDIR /app

COPY setup.py .
COPY tox.ini .
COPY MANIFEST.in .
COPY README.md .

COPY src src
COPY tests tests

ENV PYTHONPATH=/app/src

RUN git clone https://github.com/pyenv/pyenv.git /app/.pyenv
ENV PYENV_ROOT=/app/.pyenv
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
ENV PYENV_SHELL="bash"
RUN pyenv install 3.8.6
RUN pyenv install 3.7.9
RUN pyenv install 3.6.12
RUN pyenv install 3.5.10
RUN pyenv local 3.5.10 3.6.12 3.7.9 3.8.6

RUN chown -R datapunt:datapunt /app

# Any process that requires to write in the home dir
# we write to /tmp since we have no home dir
ENV HOME /tmp

USER datapunt
RUN mkdir ~/.cache
RUN mkdir ~/.tox

CMD ["tox"]
