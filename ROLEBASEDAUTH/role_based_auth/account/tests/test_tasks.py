from account.tasks import weekly_reminder,add,send_email,daily_reminder,weekly_reminder_email,daily_reminder_email
from django.test import TestCase
from unittest.mock import patch

class TaskTestCase(TestCase):
    def test_add_task(self):
        result = add.delay(3,5)
        self.assertEqual(result.get(timeout=60), 8)
    
    def test_weekly_reminder_task(self):
        result = weekly_reminder.delay()
        self.assertIsNone(result.get(timeout=300))  
        
    # @patch("account.tasks.EmailMessage.send", return_value=1)
    def test_weekly_reminder_email_task(self):
        # First, create a test user
        from account.models import User
        test_user = User.objects.create_user(username='testuser', email='satishponkada@gmail.com', password='testpass')
        result = weekly_reminder_email.delay(test_user.id)
        self.assertTrue(result)
        
    def test_daily_reminder_task(self):
        result = daily_reminder.delay()
        self.assertIsNone(result.get(timeout=300))
        
    def test_daily_reminder_email_task(self):
        from account.models import User
        test_user = User.objects.create_user(username='dailyuser', email='satishponkada@gmail.com', password='testpass')
        result = daily_reminder_email.delay(test_user.id)
        self.assertIsNone(result.get(timeout=300))