FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

CMD ["fastapi", "run", "main.py", "--port", "8000"]

#para crear la imagen
# docker build backend .

#para correr el contenedor con esa imagen
#docker run -p 8000:8000 backend
#despues acceder al link http://localhost:8000/
# o
# docker run -p 192.168.50.169:8000:8000 backend
# despues acceder al link de  ip de su pc  http://ipsupc:8000/




#CMD ["fastapi", "run", "main.py","--host","0.0.0.0", "--port", "8000"]

#CMD ["fastapi", "run", "main.py","--host","127.0.0.1", "--port", "8000"]

#COPY . /code/

#RUN pip install -r requirements.txt

#COPY . .

#CMD ["fastapi", "run", "main.py","--host","127.0.0.1", "--port", "8000"]

#CMD ["fastapi", "run", "main.py", "--port", "8000"]