FROM python:3.10
ADD /main.py .
ADD /requirements.txt .
ADD /key.txt .
ADD /puuid.json .
ADD /unique_matchid.json .
ADD /summoner_names0.json .
ADD /extraction.py .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]