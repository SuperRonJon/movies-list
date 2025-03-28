FROM node:23-alpine

RUN mkdir /frontend
WORKDIR /frontend
COPY package.json /frontend/

RUN npm install

COPY . /frontend/

EXPOSE 3000

RUN npm run build

CMD ["npm", "run", "preview", "--", "--port", "3000", "--host"]
