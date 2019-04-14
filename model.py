import random
import string
import config
import redis
import pika


def check_user_is_registered(email):
	db = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
	return db.exists('user_' + email)


def register_user(email):
	token = ''.join(random.sample(string.ascii_letters + string.digits, 12))
	confirmation_link = f'http://{config.FLASK_HOST}:{config.FLASK_PORT}/confirm/{email}/{token}'

	db = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
	db.set('confirmation_' + email, token)

	with pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBITMQ_HOST, 
		port=config.RABBITMQ_PORT)) as connection:
		channel = connection.channel()
		channel.queue_declare(queue='mipt-backend-task')
		channel.basic_publish(exchange='', routing_key='mipt-backend-task',body=confirmation_link)


def confirm_email(email, token):
	db = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
	key = 'confirmation_' + email
	if db.exists(key) and db.get(key).decode('utf-8') == token:
		db.set('user_' + email, 1)
		db.delete(key)
		return email
	else:
		return None
