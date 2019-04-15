import pika
import smtplib
import config
import ssl


def send_email(ch, method, properties, body):
	confirmation_link = body.decode("utf-8")
	reciever = confirmation_link.split('/')[-2]
	message = f"Here's your confirmation link : {confirmation_link}"

	body = "\n".join((
		"From: %s" % config.SMTP_EMAIL,
		"To: %s" % reciever,
		"Subject: Confirmation email" ,
		"",
		message
	))

	context = ssl.create_default_context()
	try:
		with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT, context=context) as server:
			server.login(config.SMTP_EMAIL, os.environ['EMAILING_SERVICE_PASSWORD'])
			server.sendmail(config.SMTP_EMAIL, reciever, body)
	except Exception as e:
		print(e)


def main():
	with pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBITMQ_HOST, 
		port=config.RABBITMQ_PORT)) as connection:
		channel = connection.channel()
		channel.queue_declare(queue='mipt-backend-task')
		channel.basic_consume('mipt-backend-task', send_email, auto_ack=True)
		channel.start_consuming()


if __name__ == '__main__':
	main()