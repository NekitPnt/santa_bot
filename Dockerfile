FROM python:3.9
# set work directory
WORKDIR /usr/src/santa_bot/
# copy project
COPY . /usr/src/santa_bot/
# install dependencies
#RUN pip install --upgrade pip
RUN pip install --user -r requirements.txt
# run app
CMD ["python", "-m", "santa_vk_bot.bot"]