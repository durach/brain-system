import time, math
from pygame.locals import *
from pqGUI import *
from const import *
from midText import *

class dBrain(pqApp):

	timer_value			= 0
	system_status		= STATUS_WAITING
	snd_10sec_played	= False
	agent_list			= False

	def main(self, agent_list):

		# Agent
		self.agent_list = agent_list
		for agent in self.agent_list:
			agent.set_app(self)

		# GUI
		self.draw_gui()
		self.update_timer_label()
		
		#Events
		for agent in self.agent_list:
			agent.register_events()

		#Sounds
		self.init_sounds()
		
		#Lamps
		self.all_lamps_off()

	def draw_gui(self):
		self.btn_reset = Button(self, ((20, 15),(140, 50)), MSG[MSG_RESET], self.do_reset, STYLE_BUTTON)
		self.btn_reset.pack()

		self.btn_start60 = Button(self, ((20, 80), (140, 50)), MSG[MSG_START60], self.do_start60, STYLE_BUTTON)
		self.btn_start60.pack()

		self.btn_start20 = Button(self, ((20, 145), (140, 50)), MSG[MSG_START20], self.do_start20, STYLE_BUTTON)
		self.btn_start20.pack()

		Box(self, ((185, 21), (220, 75)), MSG[MSG_TIMER], STYLE_TIMER_BOX).pack()
		self.lb_timer_text = MidText(self, ((185, 21), (219, 74)), '', STYLE_TIMER_TEXT)
		self.lb_timer_text.pack()

		self.lb_status = MidText(self, ((185, 110), (220, 85)), MSG[MSG_WAITING], STYLE_STATUS)
		self.lb_status.pack()

		self.bind(DBRAIN_TIMER_EVENT, self.do_timer_tick)

	def init_sounds(self):
		self.snd_start 		= pygame.mixer.Sound(SOUND_START)
		self.snd_falsestart	= pygame.mixer.Sound(SOUND_FALSESTART)
		self.snd_win		= pygame.mixer.Sound(SOUND_WIN)
		self.snd_10sec		= pygame.mixer.Sound(SOUND_10SEC)
		self.snd_timeout	= pygame.mixer.Sound(SOUND_TIMEOUT)

	def do_reset(self, e):
		self.lb_status.style[BG_COLOR] = COLOR_GREEN
		self.lb_status.settext(MSG[MSG_WAITING])
		self.reset_timer()
		self.system_status = STATUS_WAITING
		self.snd_10sec_played = False
		self.all_lamps_off()

	def do_start60(self, e):
		if (self.system_status == STATUS_WAITING):
			self.timer_target_value 	= 60
			self.timestamp_start_value	= time.time()
			self.system_status = STATUS_STARTED
			self.start_timer()
			self.play_start()
			self.lamp_start_on()

	def do_start20(self, e):
		if (self.system_status == STATUS_WAITING):
			self.lb_status.style[BG_COLOR] = COLOR_GREEN
			self.lb_status.settext(MSG[MSG_WAITING])
			self.reset_timer()
			self.system_status = STATUS_WAITING
			self.snd_10sec_played = False
			self.all_lamps_off()



			self.timer_target_value 	= 20
			self.timestamp_start_value	= time.time()
			self.system_status = STATUS_STARTED
			self.start_timer()
			self.play_start()
			self.lamp_start_on()

	def start_timer(self):
		pygame.time.set_timer(DBRAIN_TIMER_EVENT, 5)
		self.lb_status.settext(MSG[MSG_STARTED])

	def stop_timer(self):
		pygame.time.set_timer(DBRAIN_TIMER_EVENT, 0)

	def reset_timer(self):
		pygame.time.set_timer(DBRAIN_TIMER_EVENT, 0)
		self.timer_value = 0
		self.update_timer_label()

	def finalize_timer(self):
		pygame.time.set_timer(DBRAIN_TIMER_EVENT, 0)
		self.timer_value = self.timer_target_value
		self.update_timer_label()

	def do_timer_tick(self, e):
		if (self.system_status == STATUS_WAITING):	# Sometimes timer can do one tick after reset_timer
			return
		
		timestamp_current_value		= time.time()
		self.timer_value 			= timestamp_current_value - self.timestamp_start_value
		if (0 < (self.timer_target_value - self.timer_value) <= 10) and (not self.snd_10sec_played):
			self.snd_10sec_played = True
			self.play_10sec()
		if ((self.timer_target_value - self.timer_value) < 0):
			self.lb_status.settext(MSG[MSG_TIMEOUT])
			self.system_status = STATUS_STOPPED
			self.finalize_timer()
			self.play_timeout()
		self.update_timer_label()

	def exit(self, event=None):
		for agent in self.agent_list:
			agent.all_lamps_off()
			agent.quit()
		pqApp.exit(self, event)

	def update_timer_label(self):
		if self.timer_value == 0:
			self.lb_timer_text.settext('00:00')
			self.lb_timer_text.style[TEXT_COLOR] = COLOR_BLACK
		else:
			(milliseconds, seconds) = math.modf(self.timer_value)
			if 0 < (self.timer_target_value - self.timer_value) <= 10:
				self.lb_timer_text.style[TEXT_COLOR] = COLOR_RED
			else:
				self.lb_timer_text.style[TEXT_COLOR] = COLOR_BLACK
			self.lb_timer_text.settext('%02d:%02d' % (seconds, milliseconds * 100))

	def table_pressed(self, table_no):
		if self.system_status == STATUS_STARTED:
			self.process_win(table_no)

		elif self.system_status == STATUS_WAITING:
			self.process_falsestart(table_no)
			self.system_status = STATUS_STOPPED

	def process_win(self, table_no):
		self.lb_status.style[BG_COLOR] = COLOR_RED
		self.lb_status.settext(MSG[MSG_PRESSED] % (table_no))
		self.system_status = STATUS_STOPPED
		self.stop_timer()
		self.play_win(table_no)
		self.lamp_table_on(table_no)

	def process_falsestart(self, table_no):
		self.lb_status.style[BG_COLOR] = COLOR_BLUE
		self.lb_status.settext(MSG[MSG_FALSESTART] % (table_no))
		self.system_status = STATUS_STOPPED
		self.play_falsestart(table_no)
		self.lamp_falsestart_on()
		self.lamp_table_on(table_no)

	# Sounds

	def play_start(self):
		self.snd_start.play()

	def play_falsestart(self, table_no):
		self.snd_falsestart.play()

	def play_win(self, table_no):
		self.snd_win.play()

	def play_10sec(self):
		self.snd_10sec.play()

	def play_timeout(self):
		self.snd_timeout.play()

	# Lamps

	def lamp_start_on(self):
		for agent in self.agent_list:
			agent.lamp_start_on()

	def lamp_falsestart_on(self):
		for agent in self.agent_list:
			agent.lamp_falsestart_on()

	def lamp_table_on(self, table_no):
		for agent in self.agent_list:
			agent.lamp_table_on(table_no)

	def all_lamps_off(self):
		for agent in self.agent_list:
			agent.all_lamps_off()
