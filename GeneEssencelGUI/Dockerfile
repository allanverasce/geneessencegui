FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    default-jre \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-noto-core \
    fontconfig \
    xdg-utils \
    pcmanfm \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*


ENV EMAIL_SENDER="geneessencegui@gmail.com"
ENV EMAIL_PASSWORD="uulonjrgseiikjqn"
ENV XLIB_SKIP_ARGB_VISUALS=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "GeneEssenceGUI.py"]