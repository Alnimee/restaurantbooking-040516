from datetime import datetime

from schedule import Schedule
from communication import SmsSender
from communication import MailSender


class BookingScheduler:
    def __init__(self, capacity_per_hour):
        self.capacity_per_hour = capacity_per_hour # 한 타임당 허용인원
        self.schedules = [] # schedule 정보 등록
        self.sms_sender = SmsSender()
        self.mail_sender = MailSender()

    def add_schedule(self, schedule: Schedule): # 예외 발생의 경우 test 코드
        if schedule.get_date_time().minute != 0: # 1. 정각 아님
            raise ValueError("Booking should be on the hour.")

        numberOfPeople = schedule.get_number_of_people()
        for booked_schedule in self.schedules:
            if booked_schedule.get_date_time() == schedule.get_date_time():
                numberOfPeople += booked_schedule.get_number_of_people()
        if numberOfPeople > self.capacity_per_hour: # 2. 특정 예약 인원 초과
            raise ValueError("Number of people is over restaurant capacity per hour")

        # 일요일에는 시스템을 오픈하지 않는다. (나중에 주석 풀고 테스트 돌리기)
        now = self.get_now()  # 일요일 반환 정보로 수정
        if now.weekday() == 6:  # datetime 모듈에서 일요일은 6
            raise ValueError("Booking system is not available on Sunday")

        self.schedules.append(schedule)
        self.sms_sender.send(schedule)
        if schedule.get_customer().get_email():
            self.mail_sender.send_mail(schedule)

    def get_now(self):
        return datetime.now()

    def has_schedule(self, schedule):
        return schedule in self.schedules

    def set_sms_sender(self, sms_sender):
        self.sms_sender = sms_sender

    def set_mail_sender(self, mail_sender):
        self.mail_sender = mail_sender