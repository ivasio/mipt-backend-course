import pika
import smtplib
import config


def send_email(ch, method, properties, body):
	confirmation_link = body.decode("utf-8")
	reciever = confirmation_link.split('/')[-2]
	#message = f"Here's your confirmation link : <a href=\"{confirmation_link}\">{confirmation_link}</a>"
	message = f"Here's your confirmation link : {confirmation_link}"

	FROM = "confirmation@gmail.com"
	TO = "vanek.bboy@gmail.com"
	 
	body = "\r\n".join((
	    "From: %s" % FROM,
	    "To: %s" % TO,
	    "Subject: Confirmation email" ,
	    "",
	    message
	))
	 
	server = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT)
	server.sendmail(FROM, [TO], body)
	server.quit()


def main():
	with pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBITMQ_HOST, 
		port=config.RABBITMQ_PORT)) as connection:
		channel = connection.channel()
		channel.queue_declare(queue='mipt-backend-task')
		channel.basic_consume('mipt-backend-task', send_email, auto_ack=True)
		channel.start_consuming()


if __name__ == '__main__':
	main()