from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create users
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com'},
            {'username': 'spiderman', 'email': 'spidey@marvel.com'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com'},
            {'username': 'superman', 'email': 'superman@dc.com'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com'},
        ]
        users = []
        for hero in marvel_heroes + dc_heroes:
            user = User.objects.create(username=hero['username'], email=hero['email'])
            users.append(user)

        # Create teams
        marvel_team = Team.objects.create(name='Marvel')
        dc_team = Team.objects.create(name='DC')
        marvel_team.members.set(users[:3])
        dc_team.members.set(users[3:])

        # Create workouts
        workout1 = Workout.objects.create(name='Cardio Blast', description='High intensity cardio', difficulty='Medium')
        workout2 = Workout.objects.create(name='Strength Training', description='Full body strength', difficulty='Hard')

        # Create activities
        Activity.objects.create(user=users[0], activity_type='Running', duration=30, calories_burned=300, date=timezone.now().date())
        Activity.objects.create(user=users[3], activity_type='Cycling', duration=45, calories_burned=400, date=timezone.now().date())

        # Create leaderboard
        Leaderboard.objects.create(user=users[0], score=100, rank=1)
        Leaderboard.objects.create(user=users[3], score=90, rank=2)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
