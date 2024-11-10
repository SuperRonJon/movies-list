FROM node:18

RUN mkdir /frontend
WORKDIR /frontend
COPY package.json /frontend/

ENV PUBLIC_BASE_URL=""

RUN npm install

COPY . /frontend/

EXPOSE 3000

RUN npm run build

CMD ["npm", "run", "preview", "--", "--port", "3000", "--host"]