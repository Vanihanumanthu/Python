from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from main.models import Habit, PlannerTask
from datetime import date

class Command(BaseCommand):
    help = 'Send habit reminders and auto-renew tasks for users'

    def handle(self, *args, **kwargs):
        today = date.today()
        habits = Habit.objects.select_related('user').all()
        user_due_habits = {}
        user_created_tasks = {}

        for habit in habits:
            if habit.next_due_date() == today:
                # 🔁 Create planner task
                task = PlannerTask.objects.create(
                    user=habit.user,
                    task=habit.name,
                    date=today,
                    is_completed=False
                )

                user_created_tasks.setdefault(habit.user, []).append(task.task)
                user_due_habits.setdefault(habit.user, []).append(habit.name)

        # ✅ Send one grouped email per user
        for user, habits_list in user_due_habits.items():
            message = f"Hi {user.username},\n\nThese habits are due today:\n"
            message += "\n".join(f"- {habit}" for habit in habits_list)
            message += "\n\nThey’ve been added to your SmartShop planner.\n\nStay productive! 💪"

            send_mail(
                subject='🧠 SmartShop Habit Reminder',
                message=message,
                from_email='your_email@gmail.com',
                recipient_list=[user.email],  # 👈 this pulls from the user object
                fail_silently=False
            )

        # ✅ Console Output
        self.stdout.write("\n📋 Auto-Renewed Planner Tasks:")
        for user, tasks in user_created_tasks.items():
            self.stdout.write(self.style.SUCCESS(f"\n👤 {user.username}:"))
            for task in tasks:
                self.stdout.write(f"  - {task}")

        self.stdout.write(self.style.SUCCESS("\n✅ Emails sent and tasks renewed!"))
