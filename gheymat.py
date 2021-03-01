from bs4 import BeautifulSoup
import database
import telebot
import requests
import jdatetime
from telebot import types
#your bot token
bot=telebot.TeleBot("your bot token")
#id of admin
id_admin=#adminid
hide=types.ReplyKeyboardRemove()
print('bot is ready use')
markupmain = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
markupmain.add("💵قیمت ارز دیجیتال")
markupmain.add("💸قیمت ارز و طلا")
markupmain.add("✉️ارتباط با پشتیبانی")
@bot.message_handler(commands=['start'])
def send_welcome(message):
	try:
		database.createdatabase()
		database.addchatid(message.chat.id)
		welcome_message=bot.send_message(message.chat.id,'به ربات قیمت آنلاین ارز و طلا خوش آمدید برای دریافت لیست قیمت ها از دکمه های زیر استفاده کنید.',reply_markup=markupmain)
		bot.register_next_step_handler(welcome_message,getprice_step)
	except Exception as error:
		print("error in send_welcome func")
		print(error)
@bot.message_handler(commands=['admin'])
def admin_panel(message):
	try:
		replymarkup_admin=types.ReplyKeyboardMarkup(one_time_keyboard=True)
		replymarkup_admin.add('آمار کاربران')
		replymarkup_admin.add('پیام همگانی')
		replymarkup_admin.add('پیام به کاربر')
		replymarkup_admin.add('خروج از پنل')
		if message.chat.id==id_admin:
			msgpanel=bot.send_message(message.chat.id,text="پنل مدیریت:",reply_markup=replymarkup_admin)
			bot.register_next_step_handler(msgpanel,admin_panel_handle)
		else:
			bot.send_message(message.chat.id,"شما به پنل مدیریت دسترسی ندارید.",reply_markup=hide)
	except Exception as error:
		print("error in admin_panel func")
		print(error)
def admin_panel_handle(message):
	global payam
	try:
		if message.text=="آمار کاربران":
			bot.send_message(message.chat.id,database.lenall())
		elif message.text=="پیام همگانی":
			msg=bot.send_message(message.chat.id,"پیامی که میخوای بفرستی رو وارد کن",reply_markup=hide)
			
			bot.register_next_step_handler(msg,send_message_to_all)
		elif message.text=="پیام به کاربر":
			msg=bot.send_message(message.chat.id,"پیام خود را وارد کنید:",reply_markup=hide)
			bot.register_next_step_handler(msg,handle_sendmessage_to_user_0)
		elif message.text=="خروج از پنل":
			bot.send_message(message.chat.id,text="از پنل خارج شدی",reply_markup=hide)
		else:
			bot.send_message(message.chat.id,text="درخواست شما درست نیست",reply_markup=hide)
	except Exception as error:
		print("error in admin_panel_handle func")
		print(error)
def handle_sendmessage_to_user_0(message):
	try:
		global payam
		payam=message.text
		msg=bot.send_message(message.chat.id,"ایدی عددی کاربر را وارد کنید:")
		bot.register_next_step_handler(msg,handle_sendmessage_to_user_1)
	except Exception as error:
		print("error in handle_sendmessage_to_user_0 func")
		print(error)
def handle_sendmessage_to_user_1(message):
	try:
		chatid=int(message.text)
		bot.send_message(chatid,payam)
		bot.send_message(message.chat.id,"پیام شما به کاربر ارسال شد")
	except Exception as error:
		print("error in handle_sendmessage_to_user_1 func")
		print(error)
def send_message_to_all(message):
	try:
		users=database.getalluser()
		for i in users:
			bot.send_message(int(i),message.text)
	except Exception as error:
		print("error in send_message_to_all func")
		print(error)
def getprice_step(message):
	try:
		if message.text=="💵قیمت ارز دیجیتال":
			bot.send_message(message.chat.id,"⌛️منتظر بمانید",reply_markup=hide)
			bot.send_message(message.chat.id,getcoinprice())
		elif message.text=="💸قیمت ارز و طلا":
			bot.send_message(message.chat.id,"⌛️منتظر بمانید",reply_markup=hide)
			bot.send_message(message.chat.id,gheymat_arz())
		elif message.text=="✉️ارتباط با پشتیبانی":
			msg=bot.send_message(message.chat.id,"پیام خود را بفرستید.",reply_markup=hide)
			bot.register_next_step_handler(msg,msgtoadmin)
		else:
			bot.send_message(message.chat.id,'درخواست شما درست نیست',reply_markup=hide)
	except Exception as error:
		print("error in getprice_step func")
		print(error)
def msgtoadmin(message):
	try:
		yourmessage=f"📥payam jadidi darid\n🆔chatid:{message.chat.id}\n👤username:@{message.chat.username}\nmessage:\n📝{message.text}"
		bot.send_message(id_admin,yourmessage)
		bot.send_message(message.chat.id,"📤پیام شما فرستاده شد")
	except Exception as error:
		print("error in msgtoadmin func")
		print(error)
def getcoinprice():
	try:
		mysite=requests.get('https://www.coinlandexchange.com/live-price')
		soup=BeautifulSoup(mysite.content,'html.parser')
		#############################get list of coin
		mycoinlist=[]
		allmessage=""
		info=soup.select('tbody tr')
		for i in info:
			mycoinlist.append(i['class'][0])
		mycoinlist.remove('0x')
		#############################
		date=jdatetime.datetime.now()
		allmessage+="📅"+date.strftime("%Y/%m/%d")+"\n"
		allmessage+="⏰"+date.strftime("%H:%M:%S")+"\n"
		for i in mycoinlist:
			# if i=='0x':
			# 	continue
			info=soup.select(f'tr.{i} span.BTC')
			allmessage+="💰"+soup.select(f'tr.{i} span.name')[0].text+"\n"
			for i in range(0,3):
				if i==0:
					vahed="دلار"
					# emoj=":🇺🇸:"
				if i==1:
					vahed="لیر"
					# emoj=":🇹🇷:"
				elif i==2:
					vahed="تومان"
					# emoj=":🇮🇷:"
				allmessage+=info[i].text+vahed+"\n"
		return allmessage
	except Exception as error:
		print("error in getcoinprice func")
		print(error)
def gheymat_arz():
	try:
		mysite=requests.get('https://www.tasnimnews.com/fa/currency')
		soup=BeautifulSoup(mysite.content,'html.parser')
		select=soup.select('tr td')
		msg=""
		######this number is for finding our tr and td
		a=5
		b=6
		######
		date=jdatetime.datetime.now()
		msg+="📅"+date.strftime("%Y/%m/%d")+"\n"
		msg+="⏰"+date.strftime("%H:%M:%S")+"\n"
		while b<143:
			msg+="💳"+select[b].text+":"+select[a].text+"ریال\n"
			a+=3
			b+=3
		return msg
	except Exception as error:
		print("error in gheymat_arz func")
		print(error)
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()